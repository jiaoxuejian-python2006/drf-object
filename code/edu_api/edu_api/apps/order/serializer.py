from datetime import datetime

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from course.models import Course, CourseExpire
from order.models import Order, OrderDetail


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "order_number", "pay_type")

        extra_kwargs = {
            "id": {"read_only": True},
            "order_number": {"read_only": True},
            "pay_type": {"write_only": True},
        }

    def validate(self, attrs):
        """钩子函数  对数据进行校验"""
        pay_type = attrs.get("pay_type")

        try:
            Order.pay_choices[pay_type]
        except Order.DoesNotExist:
            raise serializers.ValidationError("您当前的支付方式不被允许")
        return attrs

    def create(self, validated_data):
        """创建订单  创建订单详情"""
        # TODO 1.需要获取当前订单所需的课程数据
        redis_connection = get_redis_connection("cart")
        # 获取到当前登录的用户
        # user_id = self.context['request'].user.id
        user_id = self.context['request'].data.get("user_id")
        # 将redis中的key中储存的值加一 如果key不存在则将其置为0再执行incr操作
        # 该值在redis中以字符串形式保存
        incr = redis_connection.incr("number")

        # TODO 2.生成唯一的订单号  时间戳+用户id+随机字符串
        order_num = datetime.now().strftime("%Y%m%d%H%M%S") + "%06d" % user_id + "%06d" % incr

        # TODO 3.订单的生成
        order = Order.objects.create(
            order_title="太理商城订单",
            total_price=0,
            real_price=0,
            order_number=order_num,
            pay_type=validated_data.get("pay_type"),
            credit=0,
            coupon=0,
            order_desc="你不会后悔的选择",
            user_id=user_id,
        )

        cart_list = redis_connection.hgetall("cart_%s" % user_id)
        select_list = redis_connection.smembers("selected_%s" % user_id)
        """
        
        """
        for course_id_byte, expire_id_byte in cart_list.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            # 判断商品是否被勾选
            if course_id_byte in select_list:
                # id被勾选则获取该课程的所有信息
                try:
                    course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                except Course.DoesNotExist:
                    raise serializers.ValidationError("对不起，您所购买的商品已然下架")
                # 如果课程的有效期id大于0,则需要重新计算商品优惠后的价格，id等于0则为永久有效
                origin_price = course.price
                expire_text = "永久有效"
                # cart中value大于0 则说明该商品选择的不是永久有效
                if expire_id > 0:
                    course_expire = CourseExpire.objects.get(pk=expire_id)
                    origin_price = course_expire.price
                    expire_text = course_expire.expire_text
                    # 将不同有效期对应的价格对course中的price进行修改 计算出该price的对应的打折后的价格
                    course.price = origin_price

                final_price = course.real_price()

                try:
                    OrderDetail.objects.create(
                        order=order,
                        course=course,
                        expire=expire_id,
                        price=origin_price,
                        real_price=final_price,
                        discount_name=course.discount_name
                    )
                except:
                    raise serializers.ValidationError("订单生成失败")

                # 计算订单的总价 原价
                order.total_price += float(origin_price)
                order.real_price += float(final_price)
            order.save()

            # TODO 5.如果商品已经成功生成了订单 需要将该商品从购物车中移除

        return order
