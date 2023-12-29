from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from account_app.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
import random
import os
from extensions.utils import (
    jalali_converter_year,
    jalali_converter_month,
    jalali_converter_day,
    jalali_converter,
)
from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html, strip_tags, html_safe


# generate image name
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    random_num = random.randint(1, 999)
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.get_jalali_date_for_url()}/{instance.title.replace(' ', '-')}-{random_num}{ext}"
    return f"blog/img/{final_name}"


# model managers
class BlogManager(models.Manager):
    def get_publish_blog(self):
        return self.get_queryset().filter(status=True)

    def search(self, query):
        lookup = (
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(tags__title__icontains=query)
        )
        return self.get_queryset().filter(lookup, status=True).distinct()


class BlogTagManager(models.Manager):
    def get_active_tag(self):
        return self.get_queryset().filter(status=True)


class BlogTag(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="عنوان برچسب")
    status = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    update_time = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    objects = BlogTagManager()

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"
        ordering = ["-create_time"]

    def __str__(self):
        return self.title


class Blog(models.Model):
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="blogs",
        verbose_name="نویسنده",
    )
    title = models.CharField(max_length=300, verbose_name="عنوان مقاله")
    slug = models.CharField(max_length=300, verbose_name="عنوان در url", blank=True)
    description = RichTextUploadingField(verbose_name="محتوا")
    image = models.ImageField(upload_to=upload_image_path, verbose_name="تصویر مقاله")
    tags = models.ManyToManyField(
        BlogTag, related_name="blogs", blank=True, verbose_name="تگ ها / برچسب ها"
    )
    hits = models.ManyToManyField(
        "IpAddress", blank=True, related_name="articles", verbose_name="بازید"
    )
    status = models.BooleanField(default=False, verbose_name="وضعیت انتشار")
    publish_time = models.DateTimeField(
        default=timezone.now, verbose_name="زمان انتشار"
    )
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    comments = GenericRelation("comment_app.Comment")
    objects = BlogManager()

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ["-publish_time"]

    def save(self):
        if self.pk:
            old = Blog.objects.get(pk=self.pk)
            if self.status == True and old.status == False:
                # sned email
                users = User.objects.filter(send_email=True)
                users_email = [user.email for user in users]
                current_site = "127.0.0.1:8000"
                blog_url = f"{current_site}{reverse('blog:blog_detail', kwargs={'pk': self.pk, 'slug': self.slug})}"
                blog_title = self.title
                blog_author = self.get_author_name()
                if users_email:
                    subject = f"ایجوکمپ | مقاله جدیدی با عنوان {blog_title} انتشار یافت"
                    message = f"مقاله جدیدی با عنوان {blog_title} توسط {blog_author} انتشار یافت روی لینک زیر کلیلک کنید و آن را مطالعه کنید."
                    EmailService.send_email(
                        subject,
                        users_email,
                        "email/blog-create.html",
                        {
                            "head_title": subject,
                            "message": message,
                            "blog_url": blog_url,
                            "blog_title": blog_title,
                        },
                    )
                # end send email
        super(Blog, self).save()

    def __str__(self):
        return self.title

    def get_author_name(self):
        if self.author.get_full_name():
            return self.author.get_full_name()
        else:
            return self.author

    get_author_name.short_description = "نویسنده"

    def get_jalali_date_for_url(self):
        return f"{jalali_converter_year(self.publish_time)}/{jalali_converter_month(self.publish_time)}/{jalali_converter_day(self.publish_time)}"

    get_jalali_date_for_url.short_description = "تاریخ انتشار"

    def get_description(self):
        return strip_tags(self.description[:130])

    get_description.short_description = "توضیحات"

    def count_of_hints(self):
        return self.hits.all().count()

    count_of_hints.short_description = "تعداد بازدید"

    def show_image_in_admin(self):
        if self.image:
            return format_html(
                "<img width=100px height=75px  src='{}' >".format(self.image.url)
            )
        else:
            return ""

    show_image_in_admin.short_description = "تصویر"


class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="آی پی آدرس")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    class Meta:
        verbose_name = "آی پی آدرس"
        verbose_name_plural = "آی پی آدرس ها"

    def __str__(self):
        return self.ip_address

    def jtime(self):
        return jalali_converter(self.create_time)

    jtime.short_description = "زمان ثبت"


def set_blog_slug(sender, instance, *args, **kwargs):
    instance.slug = instance.title.replace(" ", "-")


def send_blog_email(sender, instance, created, *args, **kwargs):
    if created and instance.status == True:
        # sned email
        users = User.objects.filter(send_email=True)
        users_email = [user.email for user in users]
        current_site = "127.0.0.1:8000"
        blog_url = f"{current_site}{reverse('blog:blog_detail', kwargs={'pk': instance.pk, 'slug': instance.slug})}"
        blog_title = instance.title
        blog_author = instance.get_author_name()
        if users_email:
            subject = f"ایجوکمپ | مقاله جدیدی با عنوان {blog_title} انتشار یافت"
            message = f"مقاله جدیدی با عنوان {blog_title} توسط {blog_author} انتشار یافت روی لینک زیر کلیلک کنید و آن را مطالعه کنید."
            EmailService.send_email(
                subject,
                users_email,
                "email/blog-create.html",
                {
                    "head_title": subject,
                    "message": message,
                    "blog_url": blog_url,
                    "blog_title": blog_title,
                },
            )
        # end send email


pre_save.connect(set_blog_slug, Blog)
post_save.connect(send_blog_email, Blog)
