from django.conf import settings
from rest_framework import serializers,exceptions

from api.models import Employee


class EmployeeSerializer(serializers.Serializer):
    # 定义序列化器类 需要为每个model编写对应的序列化器类

    username = serializers.CharField()
    password = serializers.CharField()
    # gender = serializers.IntegerField()
    # pic = serializers.ImageField()
    phone = serializers.CharField()

    # 自定义字段  使用来完成自定义
    aaa = serializers.SerializerMethodField()

    # 为自定义字段提供值的方法
    # 自定义字段的属性名随意 但是为字段提供的方法必须是get_字段名
    # self是当前序列化器对象 obj是当前被序列化的对象
    def get_aaa(self, obj):
        return "jxj"

    gender = serializers.SerializerMethodField()

    def get_gender(self, obj):
        # gender 值是choices类型  get_字段名_display直接访问
        return obj.get_gender_display()

    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        print(obj.pic)
        # http://127.0.0.1:8000/media/pic/2.png/
        print("http://127.0.0.1:8000/" + settings.MEDIA_URL + str(obj.pic))
        return "%s%s%s" % ("http://127.0.0.1:8000/", settings.MEDIA_URL, str(obj.pic))


class EmployeeDeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=3,
        min_length=2,
        error_messages={
            "max_length": "长度太长了",
            "min_length": "长度太短了"
        }
    )
    password = serializers.CharField()
    phone = serializers.CharField()

    re_pwd = serializers.CharField()

    # TODO 钩子函数 在create方法执行之前，DRF提供了两个钩子函数来对数据进行校验
    # 全局钩子 获取所有需要序列化的字段
    def validate(self, attrs):
        # 验证两次密码是否一致
        print(attrs)
        pwd = attrs.get("password")
        re_pwd = attrs.pop("re_pwd")
        if pwd!=re_pwd:
            print(1111)
            raise exceptions.ValidationError("两次密码不一致")
        return attrs

    # 完成对象的新增 必须重写create方法
    def create(self, validated_data):
        # print(self)
        print(validated_data)
        Employee.objects.create(**validated_data)
        return Employee.objects.create(**validated_data)
