from django.contrib import admin
from . import models

from .models import Profile

admin.site.register(Profile)
