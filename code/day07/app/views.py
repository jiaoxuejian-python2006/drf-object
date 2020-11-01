from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect


# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import User


@csrf_exempt
# @csrf_protect
def user(request):
    if request.method == 'GET':
        username = request.GET.get("username")
        print(username)
        print("GET 查询 ")
        return HttpResponse("GET OK")
    if request.method == 'POST':
        print("POST 新增")
        return HttpResponse("POST OK")
    if request.method == 'PUT':
        print("PUT 修改")
        return HttpResponse("PUT OK")
    if request.method == 'DELETE':
        print("DELETE 删除")
        return HttpResponse("DELETE OK")


"""
    函数视图: function view 基于函数定义的视图
    类视图: class view   基于类定义的视图
"""


@method_decorator(csrf_exempt, name="dispatch")
# @method_decorator(csrf_protect,name="dispatch")
class UserView(View):

    def get(self, request, *args, **kwargs):
        """"
            提供查询单个用户以及多个用户的接口
        """
        user_id=kwargs.get("id")
        if user_id:
            user_value = User.objects.filter(pk=user_id).values("username","password","gender").first()
            if user_value:
                #如果有用户信息，则返回到前端
                return JsonResponse({
                    "status":200,
                    "message":"查询单个用户成功",
                    "result":user_value
                })
            print("GET 查询 ")
        else:
            #用户id不存在 则查询所有的用户
            user_object_all=User.objects.all().values("username","password","gender")
            if user_object_all:
                return JsonResponse({
                    "status":200,
                    "message":"查询所有用户成功",
                    "results":list(user_object_all)
                })
        return JsonResponse({
            "status": 400,
            "message": "查询用户失败",
        })

    def post(self, request, *args, **kwargs):
        """
        新增单个用户 接受前端传递的参数
        """
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        try:
            user_obj=User.objects.create(username=username,password=pwd)
            return JsonResponse({
                "status":200,
                "message":"新增单个用户成功",
                "results":{"username":user_obj.username,"gender":user_obj.gender}
            })
        except:
            return JsonResponse({
                "status":400,
                "message":"添加失败",
            })

    def put(self, request, *args, **kwargs):
        print("PUT 修改")
        return HttpResponse("PUT OK")

    def delete(self, request, *args, **kwargs):
        del_id = kwargs.get("id")
        print(del_id)
        try:
            del_user = User.objects.get(pk=del_id)
            del_user.delete()
            return JsonResponse({
                "status":200,
                "message":"删除成功"
            })
        except:
            return JsonResponse({
                "status":400,
                "message":"删除失败"
            })


class StudentAPIView(APIView):
    def get(self,request,*args,**kwargs):
        print("Get Success")
        # WSGI request
        # print(request.__request.GET.get("email"))
        #restframework.views.Request
        print(request.GET.get("email"))
        #通过DRF扩展的方式来获取参数
        print(request.query_params.get("pwd"))
        return Response("GET OK")

    def post(self,request,*args,**kwargs):
        print("post sucessful")
        print(request._request.POST.get("email"))
        print(request.POST.get("email"))
        # 可以获得前端传递各种类型的参数，DRF扩展的 兼容性最强
        data = request.data
        print(data.get("email"))
        print(data)
        # print(request.data)

        return Response("POST OK")
