from django.contrib import admin
from .models import Blog, BlogTag
from django.contrib.auth import get_user_model

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = get_user_model().objects.filter(is_teacher=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    list_display = ['title','get_author_name','show_image_in_admin','get_description','get_jalali_date_for_url','count_of_hints','status']
    list_filter = ['status','publish_time']
    search_fields = ['title','description','tags__title','author__username','author__first_name','author__last_name']

    class meta:
        model = Blog

class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['title','status']
    list_filter = ['status','create_time']
    list_editable = ['status']
    search_fields = ['title']

    class meta:
        model = BlogTag

admin.site.register(Blog,BlogAdmin)
admin.site.register(BlogTag,BlogTagAdmin)
