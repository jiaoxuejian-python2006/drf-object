from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

# Create your views here.
from api.models import Book
from api.models import User
from api.serializers import BookModelSerializer, BookDeModelSerializer, BookModelSerializerV2, BookModelSerializerV3


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):

        book_id = kwargs.get("id")

        if book_id:
            book = Book.objects.get(pk=book_id)
            data = BookModelSerializer(book).data

            return Response({
                "status": 200,
                "message": "查询单个图书成功",
                "results": data,
            })
        else:
            book_object_all = Book.objects.all()
            book_ser = BookModelSerializer(book_object_all, many=True).data
            return Response({
                "status": 200,
                "message": "查询所有图书成功",
                "results": book_ser,
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data

        serializer = BookModelSerializerV2(data=request_data)

        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()
        return Response({
            "status": 200,
            "message": "添加成功",
            "results": BookModelSerializer(book_obj).data,
        })


class BookAPIViewV2(APIView):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            book = Book.objects.get(pk=book_id, is_delete=False)
            data = BookModelSerializerV2(book).data
            print(BookModelSerializerV2(book))
            return Response({
                "status": 200,
                "message": "查询单个图书成功",
                "results": data,
            })
        else:
            book = Book.objects.filter(is_delete=False)
            book_all = BookModelSerializerV2(book,many=True).data
            return Response({
                "status": 200,
                "message": "查询单个图书成功",
                "results": book_all,
            })


    def post(self,request,*args,**kwargs):
        """
        增加单个:传递参数时字典
        增加多个:[{},{},{}]列表中嵌套的是一个个图书对象
        """
        request_data = request.data
        if isinstance(request_data,dict):
            many = False
        elif isinstance(request_data,list):
            many = True
        else:
            return Response({
                "status": 400,
                "message": "参数格式有误",
            })

        serializer = BookModelSerializerV2(data=request_data,many=many)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()
        return Response({
            "status": 200,
            "message": "添加图书成功",
            "results": BookModelSerializerV2(book_obj, many=many).data,
        })


    def delete(self,request,*args,**kwargs):
        """
        删除单个，删除多个
        单个删除：通过url传递单个删除的id
        多个删除：有多个id{ids:[1,2,3]}
        """
        book_id = kwargs.get("id")
        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get("ids")
        print(ids)
        response = Book.objects.filter(pk__in=ids,is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": 200,
                "message": '删除成功'
            })

        return Response({
            "status": 400,
            "message": '删除失败或者图书存在'
        })

    #修改一个对象的所有数据
    def put(self,request,*args,**kwargs):
        request_data = request.data
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.filter(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status":400,
                "message":"图书不存在"
            })

        #更新要对前端传递的数据进行安全校验
        #更新时需要指定关键字data
        #TODO 如果是修改 需要自定关键字参数instance 指定你要修改的实例对象是哪一个
        #raise_exception=True
        #下面属性中 只有data属性 则是创建一个对象
        #下面属性中 有data和instance属性 则是修改整体的属性
        #下面属性中 有data、instance和partial属性 则是修改整体中的某一个属性
        serializer = BookModelSerializerV2(data=request_data,instance=book_obj)
        serializer.is_valid(raise_exception=True)

        return Response({
            "status": 200,
            "message": '修改成功',
            "results": BookModelSerializerV2(book_obj).data
        })

    #修改一个对象的部分数据
    # def patch(self,request,*args,**kwargs):
    #     request_data = request.data
    #     book_id = kwargs.get("id")
    #     try:
    #         book_obj = Book.objects.get(pk=book_id)
    #     except Book.DoesNotExist:
    #         return Response({
    #             "status": 400,
    #             "message": '图书不存在'
    #         })
    #
    #     serializer = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 经过序列化器对   全局钩子与局部钩子校验后  开始更新
    #     serializer.save()
    #
    #     return Response({
    #         "status": 200,
    #         "message": '修改成功',
    #         "results": BookModelSerializerV2(book_obj).data
    #     })


    def patch(self,request,*args,**kwargs):
        request_data = request.data
        book_id = kwargs.get("id")

        #如果id存在且传递的request.data格式是字典 则是单个修改。转成群体修改一个
        if book_id and isinstance(request_data,dict):
            book_ids = [book_id]
            request_data = [request_data]
        elif not book_id and isinstance(request_data,list):
            book_ids = []
            #将多有要修改的图书的id取出 放入 book_ids当中
            for dic in request_data:
                pk = dic.pop("id", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status":status.HTTP_400_BAD_REQUEST,
                        "message":"PK不存在",
                    })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "参数格式有误",
            })
        # print(request_data)
        # print(book_ids)
        # TODO 需要判断传递过来的id对应的图书是否存在，对bool_id以及request_data进行筛选
        # TODO 如果id对应的图书不存在，则移除id以及对应的request_data
        book_list = [] #所有要修改的图书对象
        new_data = [] #图书对象对应的要修改的值
        for index,pk in enumerate(book_ids):
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                new_data.append(request_data[index])
            except Book.DoesNotExist:
                continue

        book_ser = BookModelSerializerV2(data=new_data,instance=book_list,partial=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status":status.HTTP_200_OK,
            "message":"修改成功",
            "data":BookModelSerializerV2().data
        })


#GenericAPIView 继承了APIView 两者完全兼容
# GenericAPIView在APIView上多了哪些东西
class BookGenericAPIView(GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin
                         ):

    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializerV2
    # lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def delete(self,request,*args,**kwargs):
        self.destroy(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    # def get(self, request, *args, **kwargs):
    #     book_id = kwargs.get("pk")
    #     if book_id:
    #         book_obj = self.get_object()
    #         serializer = self.get_serializer(book_obj).data
    #         return Response({
    #             "status": 200,
    #             "message": "查询单个数据成功",
    #             "results": serializer,
    #         })
    #     else:
    #         #获取book模型中的所有数据
    #         # queryset = Book.objects.filter(is_delete=False)
    #         book_list = self.get_queryset()
    #
    #         #获取序列化器
    #         #data = BookModelSerializerV2(book_list).data
    #         serializer = self.get_serializer(book_list,many = True)
    #         serializer_data = serializer.data
    #         return Response({
    #             "status":200,
    #             "message":"查询所有数据成功",
    #             "results":serializer_data,
    #         })


class BookGenericAPIViewV2(generics.RetrieveUpdateDestroyAPIView,
                           # generics.ListAPIView,
                           # generics.RetrieveAPIView
                           ):
    lookup_field = "id"
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializerV2

"""
发起一个post请求 不想执行标准的http操作 想完成登录
允许开发者自定义方法函数
"""

class BookViewSetView(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = BookModelSerializerV3

    def user_login(self,request,*args,**kwargs):
        #在此完成登陆的逻辑
        user_name = request.data.get("user_name")
        pwd = request.data.get("password")
        check_user = User.objects.filter(user_name=user_name)
        check_pwd = User.objects.filter(password=pwd)
        if check_user:
            if check_pwd:
                return Response({
                    "status":200,
                    "message":"登陆成功",
                    "result":user_name
                })
            else:
                return Response({
                    "status": 400,
                    "message": "密码错误",
                    "result": user_name
                })

        else:
            return Response({
                "status": 400,
                "message": "用户名不存在",
                "result": user_name
            })

    def get_user_count(self,request,*args,**kwargs):
        #完成获取用户数量的逻辑
        return self.list(request,*args,**kwargs)

    def regist(self,request,*args,**kwargs):
        user_name = request.data.get("user_name")
        is_regist = User.objects.filter(user_name=user_name)
        if is_regist:
            return Response({
                "status": 400,
                "message": "用户名已存在",
                "result": user_name
            })
        return self.create(request, *args, **kwargs)
