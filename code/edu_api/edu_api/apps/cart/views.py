from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django_redis import get_redis_connection

from course.models import Course, CourseExpire
from edu_api.utils import contastnt


class CartViewSet(ViewSet):
    # 判断 只有登录成功的用户才可以访问此接口
    # permission_classes = [AllowAny, ]
    def add_cart(self, request):
        course_id = request.data.get("course_id")
        print(request.user)
        user_id = request.data.get("user_id")
        # user_id = request.user.id
        # 是否勾选
        select = True
        # 有效期
        expire = 0
        # 校验前端参数
        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，课程不存在"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            # 获取数据库连接
            redis_connection = get_redis_connection("cart")

            # 将数据保存到redis  使用redis管道
            pipeline = redis_connection.pipeline()
            # 保存的是商品的信息以及对应的有效期
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            # 商品的勾选状态
            pipeline.sadd("selected_%s" % user_id, course_id)

            # 执行命令
            pipeline.execute()

            # 获取购物车中商品的总数据量
            course_len = redis_connection.hlen("cart_%s" % user_id)
        except:
            return Response({"message": "参数有误，购物车添加失败"},
                            status=status.HTTP_507_INSUFFICIENT_STORAGE)
        return Response({"message": "购物车添加成功", "cart_length": course_len})

    def list_cart(self, request):
        """展示购物车"""
        # user_id = request.user.id
        user_id = request.GET.get("user_id")
        # print(request.user)
        # print(user_id)
        redis_connection = get_redis_connection("cart")
        # hgetall获取所有的键值对  hash字典
        cart_list_bytes = redis_connection.hgetall("cart_%s" % user_id)
        # smembers显示集合中所有的元素 集合
        selected_list_bytes = redis_connection.smembers("selected_%s" % user_id)

        # 获取当前所需的商品信息
        data = []
        for course_id_byte, expire_id_byte in cart_list_bytes.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            try:
                # 循环找到所有的课程信息
                course = Course.objects.get(is_show=True,pk=course_id,is_delete=False)
            except Course.DoesNotExist:
                continue
            #检查该课程的状态
            courser_expire = CourseExpire.objects.filter(course_id=course_id, pk=expire_id, is_show=True,
                                                             is_delete=False).first()
            if courser_expire:
                course.price = course.price = str(courser_expire.price)

                #将前端所需的信息返回

            data.append({
                "selected":True if course_id_byte in selected_list_bytes else False,
                "course_img": contastnt.IMG_SRC+course.course_img.url,
                "name":course.name,
                "price":course.real_price(),
                "id":course.id,
                "expire_list": course.expire_text,
                "expire_id": expire_id,
            })
        return Response(data)

    # 修改状态
    def change_selected(self,request):
        # 获取delete_course参数 判断是删除还是修改
        delete_course = request.data.get("delete_course")
        # 获取delete_all参数，判断是删除一个还是删除所有
        delete_all = request.data.get("delete_all")
        # 获取id和courser_id
        courser_id = request.data.get("courser_id")
        user_id = request.data.get("user_id")
        # 判断是否有delete_course这个参数 如果有则是删除course 否则删除状态
        if delete_course:
            redis_connection = get_redis_connection("cart")
            #查询cart中所有的键值对
            cart_list_bytes = redis_connection.hgetall("cart_%s" % user_id)
            #查询selected中所有的结果
            selected_list_bytes = redis_connection.smembers("selected_%s" % user_id)
            if delete_all:
                for i in selected_list_bytes:
                    #根据选中状态来删除选中的键值对
                    if redis_connection.hexists("cart_%s" % user_id,i):
                        #根据key获取car中对应的值
                        value = redis_connection.hget("cart_%s" % user_id, i)
                        redis_connection.hdel("cart_%s" % user_id, i, value)
                        redis_connection.srem("selected_%s" % user_id, i)
                # for i, j in cart_list_bytes.items():
                #     redis_connection.hdel("cart_%s" % user_id, i, j)
                #     redis_connection.srem("selected_%s" % user_id, i)
                course_len = redis_connection.hlen("cart_%s" % user_id)
                return Response({"message": "清空购物车成功","cart_length": course_len})
            else:
                selected_list_bytes = redis_connection.smembers("selected_%s" % user_id)

                # 获取购物车中商品的总数据量
                for i,j in cart_list_bytes.items():
                    if int(i)==int(courser_id):
                        redis_connection.hdel("cart_%s" % user_id,i,j)
                        redis_connection.srem("selected_%s" % user_id, i)
                course_len = redis_connection.hlen("cart_%s" % user_id)
                return Response({"message": "数据删除成功","cart_length": course_len})
        else:
            delete = False
            #连接数据库并
            redis_connection = get_redis_connection("cart")
            selected_list_bytes = redis_connection.smembers("selected_%s" % user_id)
            try:
                for i in selected_list_bytes:
                    if int(i) == int(courser_id):
                        delete = True
                        break
                if delete:
                    redis_connection.srem("selected_%s" % user_id, courser_id)
                    return Response({"message": "数据删除成功", })
                else:
                    redis_connection.sadd("selected_%s" % user_id, courser_id)
                    return Response({"message": "数据添加成功", })
            except:
                return Response({"message": "参数有误，删除失败"},
                                status=status.HTTP_507_INSUFFICIENT_STORAGE)

    #修改每个商品对应的状态  一个月 两个月 半年
    def change_expire(self,request,*args, **kwargs):
        courser_id = request.data.get("courser_id")
        expire_id = request.data.get("expire_id")
        user_id = request.data.get("user_id")

        redis_connection = get_redis_connection("cart")
        cart_list_bytes = redis_connection.hgetall("cart_%s" % user_id)
        #修改数据中的状态
        for course_id_byte, expire_id_byte in cart_list_bytes.items():
            if int(course_id_byte) == courser_id:
                redis_connection.hset("cart_%s" % user_id,courser_id,expire_id)

        course = Course.objects.get(is_show=True, pk=courser_id, is_delete=False)
        courser_expire =CourseExpire.objects.filter(course_id=courser_id,pk=expire_id,is_show=True,is_delete=False).first()
        if courser_expire:
            course.price = str(courser_expire.price)

        return Response({
            "price": course.real_price(),
            "courser_id": course.id
        })

    # 获取购物车中选中的课程
    def get_select_course(self, request):
        """
        获取购物车中选中的课程
        """
        user_id = request.GET.get("user_id")
        # user_id = 1
        redis_connection = get_redis_connection("cart")

        # 获取当前登录用户的购物车数据
        cart_list = redis_connection.hgetall("cart_%s" % user_id)
        select_list = redis_connection.smembers("selected_%s" % user_id)

        # 商品总价
        total_price = 0
        data = []

        for course_id_byte, expire_id_byte in cart_list.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            # 判断商品是否被勾选
            if course_id_byte in select_list:
                # 获取课程的所有信息
                try:
                    course = Course.objects.get(is_delete=False, is_show=True, pk=course_id)
                except Course.DoesNotExist:
                    continue

                # TODO 计算商品最终的总价格
                # 如果课程的有效期id大于0，则需要重新计算商品的价格，id不大于0则是永久有效
                origin_price = course.price
                expire_text = "永久有效"

                if expire_id > 0:
                    course_expire = CourseExpire.objects.get(pk=expire_id)
                    # 获取有效期对应的原价
                    origin_price = course_expire.price
                    expire_text = course_expire.expire_text

                # TODO 根据已勾选的客户课程对应 的有效期的的价格计算最终价格
                course.price = origin_price
                final_price = course.real_price()  # 如果是有效期  需要传递id

                # 将订单结算页的所需的数据返回
                data.append({
                    "course_img": contastnt.IMG_SRC + course.course_img.url,
                    "name": course.name,
                    # 最终的价格  参与过活动  有效期的价格
                    "final_price": course.real_price(),
                    "id": course.id,
                    "expire_text": expire_text,
                    "price": origin_price
                })

                # 商品的总价
                total_price += float(final_price)

        return Response({"course_list": data, "total_price": total_price, "message": "获取成功"})
