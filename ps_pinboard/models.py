# ps_pinboard/models.py
from django.db import models
from django.template.defaultfilters import slugify
from django.core.cache import cache


class PinBoard(models.Model):
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(
        max_length=255, verbose_name="Title", help_text="Required *", blank=False
    )
    category = models.CharField(
        verbose_name="Category",
        help_text="Required *",
        choices=[("open-call", "Open call"),
                 ("news", "News"),
                 ("education", "Education"),
                 ("residency", "Residency"),
                 ("job", "Job"),
                 ("funding", "Funding"),
                 ("studio", "Studio"),
                 ("trade", "Trade"),
                 ("other", "Other")],
        default="Exhibition",
        max_length=500,
        blank=False
    ) 
    location = models.CharField(
        max_length=255, verbose_name="Location", help_text="Required *. E.g. city name or region", blank=False
    )
    description = models.TextField(
        verbose_name="Description", help_text="Required *", blank=False
    )
    contact_information = models.TextField(
        verbose_name="Preferred contact information",
        help_text="Required *. E.g., phone number or/and e-mail. Be aware this will be exposed on the pinboard",
        blank=False,
    )
    consent_to_collect_info = models.BooleanField(
        verbose_name="Do you consent to having collected and expose your contact information?",
        help_text="Required *",
        choices=[(True, "Yes"), (False, "No")],
    )
    published = models.BooleanField(default=False, help_text='Check this box to publish')
    expiration_date = models.DateField(
        verbose_name="Expiration date", help_text="Required *. The post will be removed after the expiration date<br/><br/>e.g., 14/10/2023", blank=False, null=True
    )
    slug = models.SlugField(max_length=255, unique=False, blank=True)

    def save(self, *args, **kwargs):
        # Generate a slug when saving the object
        self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        # Only clear cache from admin
        if self._state.adding is False:
            # Clear cache
            cache.clear()

    def __str__(self):
        return self.title