from django.contrib import admin
from .models import TrackerModel,TrackerTitles
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin


class TrackerModelAdmin(admin.ModelAdmin):
    list_filter = (
        ('datetime', JDateFieldListFilter),
    )


admin.site.register(TrackerModel, TrackerModelAdmin)
