# ps_submission/models.py
from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _


class ExhibitionSubmission(models.Model):
    project_title = models.CharField(
        max_length=255, verbose_name="Title", help_text="Required *", blank=False
    )
    subtitle = models.CharField(
        max_length=255, verbose_name="Subtitle", blank=True
    )
    event_type = models.CharField(
        verbose_name="Type",
        help_text="Required *",
        choices=[("Exhibition", "Exhibition"), ("Performance", "Performance"), ("Screening", "Screening"), ("Fundraiser", "Fundraiser"), ("Other", "Other")],
        default="Exhibition",
        max_length=500,
        blank=False
    )
    artists = models.TextField(
        verbose_name="Artist(s)", help_text="Required *<br/><br/>Divide multiple artists with comma (,)", blank=False
    )
    curators = models.CharField(
        max_length=255, verbose_name="Curator(s)", help_text="Divide multiple curators with comma (,)", blank=True
    )
    location = models.CharField(
        max_length=255, verbose_name="Location name", help_text="Required *", blank=False
    )
    link_to_location = models.URLField(verbose_name="Location link/URL", help_text="URL e.g., https://ladder.dk", blank=True)
    exhibition_opening = models.DateField(
        verbose_name="Activity opening", help_text="Required*<br/><br/>e.g., 14/10/2023", blank=False
    )
    exhibition_end = models.DateField(
        verbose_name="Activity end", help_text="Required*<br/><br/>e.g., 16/10/2023", blank=False
    )
    description = models.TextField(
        verbose_name="Text/description/press release", help_text="Required *", blank=False
    )
    text_author = models.CharField(
        max_length=255, verbose_name="Text author", help_text="Required *", blank=False
    )
    photographer = models.CharField(
        max_length=255, verbose_name="Photographer", help_text="Required *<br/><br/>Divide multiple photographers with comma (,)", blank=False
    )
    link_to_video = models.URLField(verbose_name="Link to video", blank=True)
    social_media_info = models.TextField(verbose_name="Social media info", blank=True)
    email = models.EmailField(
        verbose_name="E-mail",
        help_text="Required *",
        validators=[EmailValidator(message="Enter a valid email address.")],
        blank=False,
    )
    consent_to_collect_info = models.BooleanField(
        verbose_name="Do you consent to having collected the submitted names, information, and e-mail?",
        help_text="Required *",
        choices=[(True, "Yes"), (False, "No")],
    )
    published = models.BooleanField(default=False, help_text='Check this box to publish')
    highlight = models.BooleanField(default=False, help_text='Check this box to highlight')

    slug = models.SlugField(max_length=255, unique=False, blank=True)

    def save(self, *args, **kwargs):
        # Generate a slug when saving the object
        self.slug = slugify(self.project_title)
        super().save(*args, **kwargs)
        
        # Only clear cache from admin
        if self._state.adding is False:
            # Clear cache
            cache.clear()

    def __str__(self):
        return self.project_title

    # def clean(self):
    #     if self.exhibition_end < self.exhibition_opening:
    #         raise ValidationError(_("Exhibition end date should not be before the opening date"))


def get_image_filename(instance, filename):
    exhibition_title = instance.exhibition.project_title 
    slug = slugify(exhibition_title)
    return f"exhibition_images/{slug}-{filename}"

def validate_image_size(value):
    # Limit image size to 3MB
    limit = 3 * 1024 * 1024  # 3MB in bytes
    if value.size > limit:
        raise ValidationError("Filesize is too large. Maximum image filesize is 3 MB.")

def validate_image_extension(value):
    valid_extensions = ['png', 'jpg', 'jpeg', 'webp']
    extension = value.name.split('.')[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError("Invalid file extension. Allowed image file extensions are: png, jpg, jpeg, webp.")


# Image Model
class ExhibitionImages(models.Model):
    exhibition = models.ForeignKey(
        ExhibitionSubmission, on_delete=models.CASCADE, related_name="images", blank=True
    )
    image = models.ImageField(
        upload_to=get_image_filename, 
        verbose_name="Activity Image",
        validators=[validate_image_size, validate_image_extension],
        max_length=500
    )
    caption = models.CharField(max_length=1000, verbose_name='Image Caption', help_text='Caption for the image', blank=False)
    cover_image = models.BooleanField(default=False, help_text='Check this box to set as cover image', blank=True)
