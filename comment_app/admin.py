from django.contrib import admin
from .models import Comment


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_user_name', 'get_message', 'get_parent_user', 'jalali_time', 'active']
    list_filter = ['active', 'created']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'parent__message',
                     'parent__user__username', 'parent__user__first_name', 'parent__user__last_name', 'message']

    class meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)
