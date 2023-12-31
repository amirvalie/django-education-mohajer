from django.shortcuts import reverse, redirect, render
from django.http import Http404
from order_app.models import Order
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from cart_app.models import Cart

# Create your views here.


@login_required()
def go_to_gateway_view(request):
    if not str(request.META.get("HTTP_REFERER"))[-17:] in [
        "account/checkout/",
        "/account/checkout",
    ]:
        raise Http404("previous page")
    user = request.user
    cart = Cart.objects.get(user_id=user.id)
    cart_items = cart.items.all()
    if not cart_items:
        raise Http404()
    order = Order.objects.create(
        user_id=user.id, status="w", is_free=False, coupon_code=cart.coupon_code
    )
    for item in cart_items:
        order.items.create(course=item.course, price=item.price, discount=item.discount)
    order_items = order.items.all()
    if order.get_total_price() == 0 and order_items:
        order.is_free = True
        order.save()
    return redirect(reverse("order:call_back", kwargs={"order_id": order.id}))


@login_required()
def callback_gateway_view(request, *args, **kwargs):
    user = request.user
    cart = Cart.objects.get(user_id=user.id)
    order = Order.objects.get(id=kwargs["order_id"])
    items = order.items.all()
    order.status = "s"
    order.payment_date = timezone.now()
    order.save()
    for item in items:
        item.course.student.add(order.user)
    if not user.is_student:
        user.is_student = True
        user.save()
    for item in cart.items.all():
        item.delete()
    cart.coupon_code = None
    cart.save()
    return render(request, "payment/payment-success.html", {"order_id": order.id})
