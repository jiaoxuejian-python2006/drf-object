import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from user.models import UserInfo
from user.utils import get_user_by_account


class UserModelSerializer(ModelSerializer):

    token = serializers.CharField(max_length=1024,read_only=True,help_text="用户token")
    code = serializers.CharField(write_only=True,help_text="手机验证码")
    class Meta:
        model = UserInfo
        fields = ('phone','password',"id","username","token","code")

        extra_kwargs = {
            'phone':{
                'write_only':True
            },
            'password': {
                'write_only': True
            },
            'username': {
                'read_only': True
            },
            'id': {
                'read_only': True
            },
        }

    #全局钩子 完成用户数据校验
    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")
        sms_code = attrs.get("code")
        if not re.match(r'^1[3-9]\d{9}',phone):
            raise serializers.ValidationError("手机号格式错误")

        #验证手机是否被注册
        try:
            user = get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user=None
        if user:
            raise serializers.ValidationError("当前手机号已被注册")
        #TODO 检验密码的格式
        if len(password)<6:
            raise serializers.ValidationError("密码长度小于六位")

        #TODO 检验验证码是否一致
        redis_connection = get_redis_connection("sms_code")
        mobile_code = redis_connection.get("mobile_%s" % phone)
        if mobile_code.decode() != sms_code:
            # 验证码有误
            raise serializers.ValidationError("验证码不一致")

        return attrs

    def create(self, validated_data):
        """用户默认信息设置"""
        #获取密码 对密码进行加密
        password = validated_data.get("password")
        hash_password = make_password(password)

        #处理用户名的默认值  随机字符串 手机号
        username = validated_data.get("phone")

        #保存数据
        user = UserInfo.objects.create(
            phone=username,
            username=username,
            password=hash_password
        )

        #为注册的用户手动生成token
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        print(user)
        return user
