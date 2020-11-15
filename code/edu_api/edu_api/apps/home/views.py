from rest_framework.generics import ListAPIView

# Create your views here.
from home.models import Banner, Nav
from home.serializer import BannerModelSerializer, NavModelSerializer
from rest_framework import settings



class BannerListAPIView(ListAPIView):

    queryset = Banner.objects.filter(is_delete=False,is_show=True).order_by("-orders")
    serializer_class = BannerModelSerializer

class HeaderListAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_delete=False,is_show=True,position=1).order_by("orders")
    serializer_class = NavModelSerializer

class FooterListAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_delete=False,is_show=True,position=2).order_by("orders")
    serializer_class = NavModelSerializer

