from abc import ABC, abstractmethod
from blog_app.models import Blog
from django.contrib.contenttypes.fields import ContentType
from course_app.models import Course
from blog_app.models import Blog
from django.urls import reverse
from .email_service import EmailService


class SendMail:
    def __init__(self, new_object) -> None:
        self.new_object = new_object
        self.current_site = "127.0.0.1:8000"
        if self.new_object.content_type.model == "course":
            self.url = f"{self.current_site}{reverse('course:course_detail',kwargs={'pk':new_object.content_object.pk,'slug':new_object.content_object.slug})}"
            self.creator_email = self.new_object.content_object.teacher.email
            self.template_name = "email/course-comment.html"
        else:
            self.url = f"{self.current_site}{reverse('blog:blog_detail',kwargs={'pk': new_object.content_object.pk,'slug': new_object.content_object.slug})}"
            self.creator_email = self.new_object.content_object.author.email
            self.template_name = "email/blog-comment.html"
        self.title = self.new_object.content_object.title
        self.current_site = "127.0.0.1:8000"
        self.user_email = new_object.user.email

    def send_mail_to_creator(self) -> None:
        subject = f"برای {self.title} دیدگاه جدیدی ثبت شد"
        message = f"برای {self.title} شما دیدگاه جدیدی توسط {self.title} ثبت شده است.\n"
        EmailService.send_email(
            subject,
            [self.creator_email],
            self.template_name,
            {
                "head_title": subject,
                "message": message,
                "course_url": self.url,
                "course_title": self.title,
            },
        )

    def send_mail_to_parent(self, parent_email: str) -> None:
        subject = (
            f"کابر {self.new_object.user}"
            f"به دیدگاه شما در {self.new_object.parent.content_object.title} پاسخ داد"
        )
        message = f"متن پیام:{self.new_object.message}"
        EmailService.send_email(
            subject,
            [parent_email],
            self.template_name,
            {
                "head_title": subject,
                "message": message,
                "course_url": self.url,
                "course_title": self.title,
            },
        )

    def send_email(self):
        # send email
        if self.creator_email != self.user_email:
            self.send_mail_to_creator()
        if self.new_object.parent:
            parent_email = self.new_object.parent.user.email
            if parent_email != self.user_email:
                self.send_mail_to_parent(parent_email)


# class CourseSendEmail:
#     def send_email(self, new_object):
#         old_object = Comment.objects.get(pk=new_object.pk)
#         if new_object.active == True and old_object.active == False:
#             # send email
#             current_site = '127.0.0.1:8000'
#             course_url = f"{current_site}{reverse(
#                 'course:course_detail'
#                 ,kwargs={'pk':new_object.course.pk,'slug':new_object.course.slug})}"
#             course_title = new_object.course.title
#             teacher_email = new_object.course.teacher.email
#             user_email = new_object.user.email
#             if teacher_email != user_email:
#                     subject = f'برای دوره شما {course_title} دیدگاه جدیدی ثبت شد'
#                     message = f'برای دوره {course_title} شما دیدگاه جدیدی توسط {new_object.user} ثبت شده است.\n'
#                     EmailService.send_email(
#                         subject,
#                         [teacher_email],
#                         'email/course-comment.html',
#                         {'head_title':subject,
#                          'message':message,
#                          'course_url':course_url,
#                          'course_title':course_title
#                     })
#             if new_object.parent:
#                 parent_email = new_object.parent.user.email
#                 if not parent_email in [teacher_email, user_email]:
#                     subject = f'کابر {new_object.user} به دیدگاه شما در دوره {new_object.parent.course.title} پاسخ داد'
#                     message = f'کابر {new_object.user} به دیدگاه شما در دوره {new_object.parent.course.title} پاسخ داد'
#                     EmailService.send_email(
#                         subject,
#                         [parent_email],
#                         'email/course-comment.html',
#                         {'head_title':subject,
#                          'message':message,
#                          'course_url':course_url,
#                          'course_title':course_title
#                     })


# class BlogCourseEmail:
#     def send_email(self, new_object):
#         old_object = Comment.objects.get(pk=new_object.pk)
#         if new_object.active == True and old_object.active == False:
#             # send email
#             current_site = '127.0.0.1:8000'
#             blog_url = f"{current_site}{reverse('blog:blog_detail',
#                      kwargs={'pk': new_object.blog.pk,
#                               'slug': new_object.blog.slug})}"
#             blog_title = new_object.blog.title
#             author_email = new_object.blog.author.email
#             user_email = new_object.user.email
#             if author_email != user_email:
#                     subject = f'برای مقاله شما {blog_title} دیدگاه جدیدی ثبت شد'
#                     message = f'برای مقاله {blog_title} شما دیدگاه جدیدی توسط {new_object.user} ثبت شده است.\n'
#                     EmailService.send_email(subject, [author_email], 'email/blog-comment.html',
#                                             {'head_title': subject, 'message': message, 'blog_url': blog_url,
#                                              'blog_title': blog_title})
#             if new_object.parent:
#                 parent_email = new_object.parent.user.email
#                 if not parent_email in [author_email, user_email]:
#                     subject = f'کابر {new_object.user} به دیدگاه شما در مقاله {new_object.parent.blog.title} پاسخ داد'
#                     message = f'کابر {new_object.user} به دیدگاه شما در مقاله {new_object.parent.blog.title} پاسخ داد'
#                     EmailService.send_email(
#                         subject, [parent_email],
#                         'email/blog-comment.html',
#                         {'head_title': subject, 'message': message, 'blog_url': blog_url}
#                     )
