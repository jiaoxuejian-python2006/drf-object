from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from api.models import Employee
from api.serializers import EmployeeSerializer, EmployeeDeSerializer


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
        # print("post sucessful")
        # print(request._request.POST.get("email"))
        # print(request.POST.get("email"))
        # 可以获得前端传递各种类型的参数，DRF扩展的 兼容性最强
        data = request.data
        print(data.get("email"))
        print(data)
        # print(request.data)

        return Response("POST OK")

class EmployeeAPIView(APIView):
    def get(self,request,*args,**kwargs):
        emp_id = kwargs.get("id")
        if emp_id:
            emp_obj = Employee.objects.get(pk=emp_id)
            # 使用序列化器完成对象的序列化
            employee_serializer=EmployeeSerializer(emp_obj).data
            print(employee_serializer)
            return Response({
                "status":200,
                "message":"查询所有用户成功",
                "results":employee_serializer
            })
        else:
            employee_objects_all = Employee.objects.all()
            emp_data=EmployeeSerializer(employee_objects_all,many=True).data
            print(emp_data)
            return Response({
                "status": 400,
                "message": "查询失败",
                "results":emp_data
            })

    def post(self,request,*args,**kwargs):
        # 获取前端传递的参数
        request_data = request.data
        # print(request_data)

        #前端传递的数据进行入库时，需要判断数据的格式是否合法
        if not isinstance(request_data,dict) or request_data=={}:
            return Response({
                "status": 400,
                "message": "参数有误",
            })
#         使用序列化器完成数据库的反序列化
#         在数据进行反序列化的时候需要指定关键字data
        serializer = EmployeeDeSerializer(data=request_data)
        if serializer.is_valid():
            # 进行数据保存
            # 调用save()方法进行数据库的保存 必须重写create()方法
            save = serializer.save()
            return Response({
                "status": 200,
                "message": "员工添加成功",
                "results": EmployeeSerializer(save).data
            })
        else:

            return Response({
                "status": 400,
                "message": "员工添加失败",
            })
