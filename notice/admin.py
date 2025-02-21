from django.contrib import admin
from django_ckeditor_5.fields import CKEditor5Field
from django_ckeditor_5.widgets import CKEditor5Widget

from notice.models import Notice


# Register your models here.
class NoticeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        CKEditor5Field: {'widget': CKEditor5Widget(config_name='default')},
    }


admin.site.register(Notice, NoticeAdmin)
