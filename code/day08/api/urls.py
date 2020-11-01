from django.urls import path
from api import views

urlpatterns = [
    # path("users/",views.user),
    # # 类视图的url定义
    # path("user_view/<str:id>/",views.UserView.as_view()),
    # path("user_view/",views.UserView.as_view()),
    path("student_view/",views.StudentAPIView.as_view()),
    path("emp/",views.EmployeeAPIView.as_view()),
    path("emp/<str:id>/",views.EmployeeAPIView.as_view()),
]