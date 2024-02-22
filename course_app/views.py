from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from course_app.models import Course, CourseCategory
from django.http import Http404
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.urls import reverse


# Create your views here.

class CourseList(ListView):
    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if search is not None:
            return Course.objects.search(search)
        category = request.GET.get('categories')
        if category is not None:
            return Course.objects.get_course_by_category(category)
        return Course.objects.get_publish_course()

    template_name = 'course/course-list.html'
    paginate_by = 9


class CourseDetail(DetailView):
    template_name = 'course/course-detail.html'
    context_object_name = 'object'

    def get_object(self):
        course = get_object_or_404(Course.objects.get_publish_course(), pk=self.kwargs.get('pk'),
                                   slug=self.kwargs.get('slug'))
        return course


def sidebar_course_list(request):
    categories = CourseCategory.objects.get_active_category()
    courses = Course.objects.get_publish_course()[:3]
    context = {
        'categories': categories,
        'courses': courses
    }
    return render(request, 'course/sidebar-course-list.html', context)
