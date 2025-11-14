import io
import os
from pathlib import Path
from PIL import Image, ImageOps
import cloudinary
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError
from django.conf import settings

MAX_BYTES = 10 * 1024 * 1024  # 10MB
TARGET_BYTES = int(MAX_BYTES * 0.93)  # 9.3MB target


def smart_compress_to_bytes(src_file) -> bytes:
    """
    Compress image to target size with WebP conversion.
    Accepts file-like object or file path.
    Returns compressed bytes.
    """
    if isinstance(src_file, (str, Path)):
        im = Image.open(src_file)
    else:
        im = Image.open(src_file)

    with im:
        # Auto-rotate based on EXIF
        im = ImageOps.exif_transpose(im)
        
        # Determine format
        fmt = (im.format or "JPEG").upper()
        prefer_webp = fmt in ("PNG", "TIFF")
        out_fmt = "WEBP" if prefer_webp else ("JPEG" if fmt != "WEBP" else "WEBP")
        
        # Cap extreme dimensions
        max_w = 5000
        if im.width > max_w:
            im = im.resize((max_w, int(im.height * (max_w / im.width))), Image.LANCZOS)
        
        # Iterative quality reduction
        q = 82
        min_q = 50 if out_fmt == "JPEG" else 45
        step = 4
        
        while True:
            buf = io.BytesIO()
            if out_fmt == "JPEG":
                im.save(buf, format="JPEG", quality=q, optimize=True, 
                       progressive=True, subsampling="4:2:0")
            else:
                im.save(buf, format="WEBP", quality=q, method=6)
            
            data = buf.getvalue()
            if len(data) <= TARGET_BYTES or q <= min_q:
                return data
            q = max(min_q, q - step)


def upload_to_cloudinary(file_bytes: bytes, folder: str, public_id: str, tags=None):
    """
    Upload image to Cloudinary and return URLs.
    
    Args:
        file_bytes: Compressed image bytes
        folder: Cloudinary folder (e.g., "madrid_marble/uploads")
        public_id: Unique identifier (e.g., "hero-image")
        tags: List of tags (e.g., ["hero", "homepage"])
    
    Returns:
        tuple: (result_dict, web_url, thumb_url)
    """
    try:
        result = cloudinary.uploader.upload(
            file=io.BytesIO(file_bytes),
            resource_type="image",
            folder=folder or "madrid_marble/uploads",
            public_id=public_id,
            overwrite=True,
            unique_filename=False,
            use_filename=False,
            eager=[{
                "format": "webp",
                "quality": "auto",
                "fetch_format": "auto",
                "crop": "limit",
                "width": 2400
            }],
            tags=(tags or []),
            timeout=120,
        )
        
        secure_url = result.get("secure_url", "")
        
        # Generate URL variants
        if "/upload/" in secure_url:
            web_url = secure_url.replace("/upload/", "/upload/f_auto,q_auto/")
            thumb_url = secure_url.replace("/upload/", "/upload/c_fill,g_face,w_480,h_320/")
        else:
            web_url = secure_url
            thumb_url = secure_url
        
        return result, web_url, thumb_url
    
    except CloudinaryError as e:
        raise Exception(f"Cloudinary upload error: {str(e)}")
    except Exception as e:
        raise Exception(f"Upload error: {str(e)}")


