from django.contrib import admin
from users.models import Info
from users.models import Setting
from users.models import Friendship


class InfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'first_name', 'last_name')
admin.site.register(Info, InfoAdmin)


class SettingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'need_permission_to_listen', 'need_permission_to_message')
admin.site.register(Setting, SettingAdmin)


class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('followed', 'follower',
                    'is_active', 'is_confirm', 'dateline')
admin.site.register(Friendship, FriendshipAdmin)
