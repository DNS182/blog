from django.contrib import admin
from .models import Profile

# Register your models here.
admin.site.register(Profile)





# You can clear Recent Actions of Django Admin.

# python manage.py shell
# from django.contrib.admin.models import LogEntry
# LogEntry.objects.all().delete()