"""
Management command to fix Cloudinary image access mode
Changes existing private images to public access
"""
from django.core.management.base import BaseCommand
from myApp.models import MediaAsset
import cloudinary
import cloudinary.api
from cloudinary.exceptions import Error as CloudinaryError


class Command(BaseCommand):
    help = 'Fix Cloudinary image access mode - make all images public'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without actually changing it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.SUCCESS('Checking Cloudinary images...'))
        
        assets = MediaAsset.objects.filter(is_active=True)
        total = assets.count()
        fixed = 0
        errors = 0
        
        for asset in assets:
            try:
                # Get resource info from Cloudinary
                resource = cloudinary.api.resource(
                    asset.public_id,
                    resource_type='image'
                )
                
                # Check if it's private
                access_mode = resource.get('access_mode', 'public')
                
                if access_mode != 'public':
                    if dry_run:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Would fix: {asset.title} (currently {access_mode})'
                            )
                        )
                    else:
                        # Update access mode to public
                        cloudinary.uploader.explicit(
                            asset.public_id,
                            resource_type='image',
                            type='upload',
                            access_mode='public',
                            invalidate=True
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Fixed: {asset.title}')
                        )
                    fixed += 1
                else:
                    if not dry_run:
                        self.stdout.write(f'  Already public: {asset.title}')
                        
            except CloudinaryError as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error with {asset.title}: {str(e)}')
                )
                errors += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Unexpected error with {asset.title}: {str(e)}')
                )
                errors += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Summary:'))
        self.stdout.write(f'   Total images: {total}')
        if dry_run:
            self.stdout.write(f'   Would fix: {fixed}')
        else:
            self.stdout.write(f'   Fixed: {fixed}')
        self.stdout.write(f'   Errors: {errors}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\n💡 Run without --dry-run to apply changes'))

