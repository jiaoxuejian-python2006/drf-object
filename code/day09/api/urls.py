from django.urls import path

from api import views

urlpatterns = [
    path("books/",views.BookAPIView.as_view()),
    path("books/<str:id>/", views.BookAPIView.as_view()),

    path("v2/books/",views.BookAPIViewV2.as_view()),
    path("v2/books/<str:id>/", views.BookAPIViewV2.as_view()),

    path("gen/", views.BookGenericAPIView.as_view()),
    path("gen/<str:pk>/", views.BookGenericAPIView.as_view()),

    path("v3/", views.BookGenericAPIViewV2.as_view()),
    path("v3/<str:id>/", views.BookGenericAPIViewV2.as_view()),

    path("set/", views.BookViewSetView.as_view({"get":"user_login","post":"regist"})),
    path("set/<str:id>/", views.BookViewSetView.as_view({"get":"user_login","post":"regist"})),
]