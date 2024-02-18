# ps_calendar/models.py
from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

# GeoPy libraries
from geopy.geocoders import Nominatim
from decimal import Decimal


class CalendarSubmission(models.Model):
    project_title = models.CharField(
        max_length=255, verbose_name="Title", help_text="Required *", blank=False
    )
    subtitle = models.CharField(
        max_length=255, verbose_name="Subtitle", blank=True
    )
    event_type = models.CharField(
        verbose_name="Type",
        help_text="Required *",
        choices=[("Exhibition", "Exhibition"), ("Performance", "Performance"), ("Screening", "Screening"), ("Other", "Other")],
        default="Exhibition",
        max_length=500,
        blank=False
    )
    artists = models.CharField(
        max_length=255, verbose_name="Artist(s)", help_text="Required *<br/><br/>Divide multiple artists with comma (,)", blank=False
    )
    curators = models.CharField(
        max_length=255, verbose_name="Curator(s)", help_text="Required *<br/><br/>Divide multiple curators with comma (,)", blank=False
    )
    location = models.CharField(
        max_length=255, verbose_name="Location name", help_text="Required *", blank=False
    )
    link_to_location = models.URLField(verbose_name="Location link/URL", help_text="URL e.g., https://ladder.dk", blank=True)
    location_address = models.CharField(
        max_length=1000, verbose_name="Location Address", help_text="Required *<br/><br/>Format:<br/>[street name] [street number], [town/city], [postcode], Denmark<br/><br/>Example:<br/>Halmtorvet 11D, København V, 1700, Denmark", blank=False, null=True
    )
    latitude = models.DecimalField(verbose_name="Latitude", max_digits=18, decimal_places=10, null=True)
    longitude = models.DecimalField(verbose_name="Longitude", max_digits=18, decimal_places=10, null=True)
    opening_hours = models.TextField(
        verbose_name="Opening Hours", help_text="Required *<br/><br/>Format:<br/>[weekday(s) and interval]: [timeslot]<br/><br/>Examples:<br/>- Wednesday-Saturday, except Thursday: 16:00-20:00<br/>- Thursday, Friday: 19:00-22:00<br/>- By appointment, Saturday: 12:00-16:00<br/>- Wednesday-Friday: 16:00-20:00,<br/>  Saturday: 12:00-17:00,<br/>  Sunday: 12:00-14:00,<br/>  Closed from 30.12.23 until 06.01.24", blank=False, null=True
    )
    admission = models.CharField(
        max_length=255, verbose_name="Admission", help_text="Required *<br/><br/>Format:<br/>[value] [valuta] or free<br/><br/>Examples:<br/>- 80 DKK<br/>- Free", blank=False, null=True
    )
    exhibition_opening = models.DateField(
        verbose_name="Exhibition Opening", help_text="Required*<br/><br/>e.g., 14/10/2023", blank=False
    )
    exhibition_end = models.DateField(
        verbose_name="Exhibition End",  help_text="Required*<br/><br/>e.g., 16/10/2023", blank=False
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
        # Only override for new events
        if self._state.adding is True:
            # Generate latitude longitude coordinates for the map when saving the object
            self.latitude, self.longitude = geocoder(self.location_address)

        # Generate a slug when saving the object
        self.slug = slugify(self.project_title)

        super().save(*args, **kwargs)

        # Only clear cache from admin
        if self._state.adding is False:
            # Clear cache
            cache.clear()
        
    def __str__(self):
        return self.project_title

    def clean(self):
        if self.exhibition_end < self.exhibition_opening:
            raise ValidationError(
                _("Exhibition end date should not be before the opening date")
            )

def geocoder(address):
    geolocator = Nominatim(user_agent="ursuppe-geocoder")
    
    try:
        place, (lat, lng) = geolocator.geocode(address, country_codes=["dk"], exactly_one=True)
    except:
        # print("Error: geocode failed on input %s with message %s"%(a, error_message))
        # Instead of catching and printing the error, just set lat, lng to 0 and set later in admin
        lat, lng = (0,0)
        pass

    return Decimal(lat), Decimal(lng)

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
