from common.models import BaseModel

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserProfile(BaseModel):
    """
    Extended user profile information.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name=_("User")
    )
    profile_picture = models.URLField(
        verbose_name=_("Profile Picture"), max_length=500, blank=True, null=True
    )

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return f"{self.user.username}'s profile"
