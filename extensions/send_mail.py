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
        self.user_email = new_object.user.email

    def send_mail_to_creator(self) -> None:
        subject = f"برای {self.title} دیدگاه جدیدی ثبت شد"
        message = (
            f"برای {self.title} شما دیدگاه جدیدی توسط {self.user_email} ثبت شده است.\n"
        )
        EmailService.send_email(
            subject,
            [self.creator_email],
            self.template_name,
            {
                "head_title": subject,
                "message": message,
                "blog_url": self.url,
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
