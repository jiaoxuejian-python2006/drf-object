from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from api.models import Book
from api.serializers import BookModelSerializer, BookDeModelSerializer, BookModelSerializerV2


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


    def patch(self,request,*args,**kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 400,
                "message": '图书不存在'
            })

        serializer = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
        serializer.is_valid(raise_exception=True)

        # 经过序列化器对   全局钩子与局部钩子校验后  开始更新
        serializer.save()

        return Response({
            "status": 200,
            "message": '修改成功',
            "results": BookModelSerializerV2(book_obj).data
        })