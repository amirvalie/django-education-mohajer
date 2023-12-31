from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from .forms import CommentForm
from django.contrib.contenttypes.fields import ContentType
from django.contrib import messages
from django.urls import reverse


class PostComment(CreateView):
    form_class = CommentForm
    content_type = None
    content_object = None

    def post(self, request, *args, **kwargs):
        self.content_type = get_object_or_404(
            ContentType, id=kwargs.get("content_type_id")
        )
        model_class = self.content_type.model_class()
        self.content_object = get_object_or_404(model_class, id=kwargs.get("object_id"))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        if self.content_type.model == "course":
            return reverse(
                "course:course_detail",
                kwargs={"pk": self.content_object.pk, "slug": self.content_object.slug},
            )
        return reverse(
            "blog:blog_detail",
            kwargs={"pk": self.content_object.pk, "slug": self.content_object.slug},
        )

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.content_type = self.content_type
            obj.object_id = self.content_object.id
            try:
                obj.parent_id = int(self.request.POST.get("parent_id"))
            except:
                obj.parent_id = None
            messages.success(
                self.request, "دیدگاه شما با موفقیت ثبت شد. منتظر تایید باشید"
            )
            obj.save()
        return super(PostComment, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "عملیات ناموفق بود. دوباره تلاش کنید", extra_tags="error"
        )
        return super(PostComment, self).form_invalid(form)
