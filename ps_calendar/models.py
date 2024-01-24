# ps_calendar/models.py
from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class CalendarSubmission(models.Model):
    project_title = models.CharField(
        max_length=255, verbose_name="Title", help_text="Required *", blank=False
    )
    subtitle = models.CharField(
        max_length=255, verbose_name="Subtitle", blank=True
    )
    artists = models.CharField(
        max_length=255, verbose_name="Artist(s)", help_text="Required *", blank=False
    )
    curators = models.CharField(
        max_length=255, verbose_name="Curator(s)", help_text="Required *", blank=False
    )
    location = models.CharField(
        max_length=255, verbose_name="Location", help_text="Required *", blank=False
    )
    link_to_location = models.URLField(verbose_name="Link to Location", blank=True)
    location_address = models.TextField(
        verbose_name="Location Address", help_text="Required *<br/><br/>Format:<br/>[street name] [street number], [town/city], [postcode], Denmark<br/><br/>Example:<br/>Halmtorvet 11D, København V, 1700, Denmark", blank=False
    )
    exhibition_opening = models.DateField(
        verbose_name="Exhibition Opening", help_text="eg. 2024-01-01 Required *", blank=False
    )
    exhibition_end = models.DateField(
        verbose_name="Exhibition End",  help_text="eg. 2024-01-02 Required *", blank=False
    )
    description = models.TextField(
        verbose_name="Text/Description/Press Release", help_text="Required *", blank=False
    )
    social_media_info = models.TextField(verbose_name="Social Media Info", blank=True)
    email = models.EmailField(
        verbose_name="E-mail",
        help_text="Required",
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
        
    def __str__(self):
        return self.project_title

    def clean(self):
        if self.exhibition_end < self.exhibition_opening:
            raise ValidationError(
                _("Exhibition end date should not be before the opening date")
            )


def get_image_filename(instance, filename):
    calendar_title = instance.calendar.project_title
    slug = slugify(calendar_title)
    return f"calendar_images/{slug}-{filename}"

def validate_image_size(value):
    # Limit image size to 3MB
    limit = 3 * 1024 * 1024  # 3MB in bytes
    if value.size > limit:
        raise ValidationError("File size too large. Max size is 3 MB.")

def validate_image_extension(value):
    valid_extensions = ['png', 'jpg', 'jpeg', 'webp']
    extension = value.name.split('.')[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError("Invalid file extension. Allowed extensions are: png, jpg, jpeg, webp.")


class CalendarImages(models.Model):
    calendar = models.ForeignKey(
        CalendarSubmission, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to=get_image_filename, 
        verbose_name="Event Image",
        validators=[validate_image_size, validate_image_extension]
    )
    caption = models.CharField(max_length=255, verbose_name='Image Caption', help_text='')
