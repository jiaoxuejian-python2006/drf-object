from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django_redis import get_redis_connection
from rest_framework import serializers

from user.models import UserInfo


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "user": user.username,
        "user_id": user.id
    }


def get_user_by_account(account):
    """根据条件获取用户"""
    try:
        user = UserInfo.objects.filter(Q(username=account) | Q(email=account) | Q(phone=account)).first()
    except UserInfo.DoesNotExist:
        return None
    else:
        return user

def check_code(user,code):
    redis_connection = get_redis_connection("sms_code")
    mobile_code = redis_connection.get("mobile_%s" % user)
    if mobile_code.decode() != code:
        # 验证码有误
        raise serializers.ValidationError("验证码不一致")

    return user

class UserAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs,):
        """
        根据账号来获取用户登陆方式   手机号  邮箱  用户名
        :return:  查询出的用户
        """
        user = get_user_by_account(username)
        if user and user.check_password(password) and user.is_authenticated:
            return user
        elif user and check_code(user,password):
            return user
        else:
            return None