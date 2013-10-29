from django.contrib import admin
from yap.models import Yap


class YapAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'path', 'dateline')
admin.site.register(Yap, YapAdmin)
