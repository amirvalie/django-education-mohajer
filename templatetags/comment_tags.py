from django import template
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.db.models import Count
from comment_app.models import Comment
from comment_app.forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/comment.html', takes_context=True)
def comment(context, obj):
    return {
        'object': obj,
        'comments': obj.comments.get_active_comment().order_by('-created'),
        'request': context['request'],
    }


@register.simple_tag(takes_context=True)
def comment_form(context):
    form = CommentForm()
    return form


@register.filter
def comments_count(obj):
    return obj.comments.get_active_comment().count()


@register.simple_tag
def comment_target(obj):
    return reverse('comment:post_comment', args=(
        ContentType.objects.get_for_model(obj).id,
        obj.id,
    ))
