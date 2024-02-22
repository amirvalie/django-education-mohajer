from django.test import TestCase
from .models import Course, CourseCategory, CourseTag

# Create your tests here.


class TestCourseModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        course_category = CourseCategory.objects.create(title="Programming")
        course_tag = CourseTag.objects.create(title="python")
        course = Course.objects.create(
            title="Python course",
            slug="python-course",
            image="/home/amir/Pictures/test.png",
            description="Python is a programming language",
            price=1000000,
            level="b",
            language="fa",
            is_finish=True,
            status=True,
        )
        course.categories.set([course_category])
        course.tags.set([course_tag])

    def test_title_label(self):
        obj = Course.objects.get(id=1)
        label = obj._meta.get_field("title").verbose_name
        self.assertEqual(label, "عنوان دوره")

    def test_slug_label(self):
        obj = Course.objects.get(id=1)
        label = obj._meta.get_field("slug").verbose_name
        self.assertEquals(label, "عنوان در url")

    def test_status_label(self):
        obj = Course.objects.get(id=1)
        label = obj._meta.get_field("status").verbose_name
        self.assertEquals(label, "آیا نمایش داده شود؟")

    def test_get_absolute_url(self):
        obj = Course.objects.get(id=1)
        self.assertEqual(obj.get_absolute_url(), f"/courses/{obj.pk}/{obj.slug}/")
