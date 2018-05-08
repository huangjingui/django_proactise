from django.contrib import admin
from proactise import models

admin.site.register(models.User)


admin.site.register(models.ConfirmString)