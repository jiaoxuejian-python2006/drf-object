from django.urls import path

from cart import views

urlpatterns=[
    path("cart/",views.CartViewSet.as_view({"post":"add_cart", "get": "list_cart","delete":"change_selected","put":"change_expire"})),
    path("order/",views.CartViewSet.as_view({"get": "get_select_course"}))
]