from django.test import TestCase
from .models import Blog, BlogTag
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.
class TestBlogTag(TestCase):
    @classmethod
    def setUpTestData(cls):
        BlogTag.objects.create(title="tag2", status=True)

    def test_create_blog_tag_model_object(self):
        obj = BlogTag.objects.create(title="tag1", status=True)
        self.assertEquals(obj.title, "tag1")
        self.assertEquals(obj.status, True)

    def test_title_max_length(self):
        obj = BlogTag.objects.get(id=1)
        max_length = obj._meta.get_field("title").max_length
        self.assertEquals(max_length, 200)

    def test_title_label(self):
        obj = BlogTag.objects.get(id=1)
        label = obj._meta.get_field("title").verbose_name
        self.assertEquals(label, "عنوان برچسب")

    def test_status_label(self):
        obj = BlogTag.objects.get(id=1)
        label = obj._meta.get_field("status").verbose_name
        self.assertEquals(label, "فعال/غیرفعال")


class TestBlog(TestCase):
    def setUp(self) -> None:
        pass

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username="Nilofar",
            email="nilofar@gmail.com",
            is_teacher=True,
        )
        Blog.objects.create(
            author=user,
            title="Python course",
            slug="Python-course",
            description="Python-course",
            image="/home/amir/Pictures/test.png",
            status=True,
        )

    def test_title_label(self):
        obj = Blog.objects.get(id=1)
        label = obj._meta.get_field("title").verbose_name
        self.assertEquals(label, "عنوان مقاله")

    def test_status_label(self):
        obj = Blog.objects.get(id=1)
        label = obj._meta.get_field("status").verbose_name
        self.assertEquals(label, "وضعیت انتشار")

    def test_slug_label(self):
        obj = Blog.objects.get(id=1)
        label = obj._meta.get_field("slug").verbose_name
        self.assertEquals(label, "عنوان در url")
