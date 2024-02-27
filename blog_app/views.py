from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Blog, BlogTag
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.urls import reverse


# Create your views here.
class BlogList(ListView):
    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if search is not None:
            return Blog.objects.search(search)
        return Blog.objects.get_publish_blog()

    template_name = 'blog/blog-list.html'
    paginate_by = 8


class BlogDetail(DetailView):
    def get_object(self, **kwargs):
        blog = get_object_or_404(Blog.objects.get_publish_blog(), pk=self.kwargs.get('pk'),
                                 slug=self.kwargs.get('slug'))
        ip_address = self.request.user.ip_address
        if ip_address not in blog.hits.all():
            blog.hits.add(ip_address)
        return blog

    template_name = 'blog/blog-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def sidebar_blog(request):
    blogs = Blog.objects.get_publish_blog()[:6]
    tags = BlogTag.objects.get_active_tag()[:20]
    context = {
        'blogs': blogs,
        'tags': tags,
    }
    return render(request, 'blog/sidebar-blog.html', context)
