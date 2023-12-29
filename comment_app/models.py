from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.contenttypes.fields import ContentType
from django.contrib.auth import get_user_model
from extensions.utils import jalali_converter
from extensions.send_mail import SendMail

User = get_user_model()

# Create your models here.


class CommentManager(models.Manager):
    def get_active_comment(self):
        return self.get_queryset().filter(active=True, parent__isnull=True)

    def get_active_reply(self):
        return self.get_queryset().filter(active=True, parent__isnull=False)


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="blog_comments",
        verbose_name="کاربر",
    )
    message = models.TextField(verbose_name="نظر")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="replies",
        verbose_name="پاسخ",
    )
    active = models.BooleanField(default=False, verbose_name="تایید شده / نشده")
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    updated = models.DateTimeField(auto_now=True, verbose_name="زمان ویرایش")
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="انتخاب مدل",
    )
    object_id = models.PositiveIntegerField(verbose_name="ای دی شیء")
    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )
    objects = CommentManager()

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ["-created"]

    def save(self):
        if self.pk:
            self.old_object = Comment.objects.get(id=self.pk)
            if self.active == True and self.old_object.active == False:
                mail = SendMail(self)
                mail.send_email()
        super().save()

    def __str__(self):
        return f"{str(self.user)} | {self.message[0:70]}"

    def get_user_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        else:
            return self.user

    get_user_name.short_description = "نویسنده"

    def get_message(self):
        return self.message[:100]

    get_message.short_description = "دیدگاه"

    def jalali_time(self):
        return jalali_converter(self.created)

    jalali_time.short_description = "زمان ثبت"

    def get_parent_user(self):
        if self.parent:
            return self.parent.user.username
        return ""

    get_parent_user.short_description = "پاسخ به کاربر"


# def send_comment_email(obj):
#     if obj.pk:
#         old = Comment.objects.get(pk=obj.pk)
#         if obj.active == True and old.active == False:
#                     # send email
#         author_email = obj.blog.author.email
#         user_email = obj.user.email
#         if author_email == user_email:
#             author_email = False
#             user_email = False
#         parent_email = False
#         if obj.parent:
#             parent_email = obj.parent.user.email
#             if parent_email in [author_email, user_email]:
#                 parent_email = False
#         current_site = '127.0.0.1:8000'
#         blog_url = f"{current_site}{reverse('blog:blog_detail', kwargs={'pk': obj.blog.pk, 'slug': obj.blog.slug})}"
#         blog_title = obj.blog.title
#         if author_email:
#             subject = f'برای مقاله شما {blog_title} دیدگاه جدیدی ثبت شد'
#             message = f'برای مقاله {blog_title} شما دیدگاه جدیدی توسط {obj.user} ثبت شده است.\n'
#             EmailService.send_email(subject, [author_email], 'email/blog-comment.html',
#                                     {'head_title': subject, 'message': message, 'blog_url': blog_url,
#                                      'blog_title': blog_title})
#         if parent_email:
#             subject = f'کابر {obj.user} به دیدگاه شما در مقاله {obj.parent.blog.title} پاسخ داد'
#             message = f'کابر {obj.user} به دیدگاه شما در مقاله {obj.parent.blog.title} پاسخ داد'
#             EmailService.send_email(subject, [parent_email], 'email/blog-comment.html',
#                                     {'head_title': subject, 'message': message, 'blog_url': blog_url,
#                                      'blog_title': blog_title})
