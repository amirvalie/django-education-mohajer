from django.contrib import admin
from .models import Course, CourseCategory, Video, CourseTag
from account_app.models import User


# Register your models here.

class VideoCourseInlines(admin.StackedInline):
    model = Video
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = User.objects.filter(is_teacher=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ['title', 'get_teacher_name', 'show_image_in_admin', 'price', 'discount', 'total_price',
                    'category_to_str', 'total_time', 'is_finish', 'count_of_student', 'jalali_time', 'status']
    list_filter = ['status', 'is_finish']
    search_fields = ['title', 'categories__title', 'tags__title', 'teacher__username', 'teacher__first_name',
                     'teacher__last_name']
    inlines = [VideoCourseInlines]

    class meta:
        model = Course


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'position']
    list_editable = ['position', 'status']
    list_filter = ['status', 'create_time']
    search_fields = ['title']

    class meta:
        model = CourseCategory


class CourseTagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_editable = ['status']
    list_filter = ['status', 'create_time']
    search_fields = ['title']

    class meta:
        model = CourseTag


class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'video', 'course', 'time', 'publish_time', 'status']
    list_filter = ['status', 'publish_time']
    search_fields = ['title', 'course__title']

    class meta:
        model = Video



admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(CourseTag, CourseTagAdmin)
admin.site.register(Video, VideoAdmin)
