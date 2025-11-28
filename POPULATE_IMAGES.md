# How to Populate All Image URLs from Gallery

## Quick Fix - Replace ALL Images

Run this command to replace ALL image URLs (including Unsplash/dummy ones) with your gallery images:

```bash
cd myProject
python manage.py populate_image_urls --replace-all
```

## Preview First (Recommended)

See what will be changed before applying:

```bash
python manage.py populate_image_urls --replace-all --dry-run
```

## What It Does

- Replaces ALL image URLs throughout the website with URLs from your MediaAsset gallery
- Updates:
  - Navigation logo
  - Hero images (all pages)
  - Service images
  - Portfolio images
  - About page images
  - FAQ page images
  - Contact page images
  - All service items
  - All portfolio projects

## Other Useful Commands

```bash
# List all available URLs from gallery
python manage.py populate_image_urls --list

# Generate detailed report
python manage.py populate_image_urls --report

# Only populate empty fields (not replace existing)
python manage.py populate_image_urls --populate
```

## After Running

After you run `--replace-all`, all images will use your gallery URLs instead of dummy/Unsplash URLs.

The templates now have fallbacks, so even if a field is empty, it will try to use images from your gallery automatically.

