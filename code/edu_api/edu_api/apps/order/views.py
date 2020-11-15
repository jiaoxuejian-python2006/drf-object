from django.shortcuts import render
from rest_framework.generics import CreateAPIView
# Create your views here.
from order.models import Order
from order.serializer import OrderModelSerializer


class OrderAPIView(CreateAPIView):
    queryset = Order.objects.filter(is_delete=False,is_show=True)
    serializer_class = OrderModelSerializer
