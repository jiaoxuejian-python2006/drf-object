import xadmin

from user.models import UserInfo


class UserInfoDetail(object):
    list_display = ['username', 'phone', 'email']


# xadmin.site.register(UserInfo, UserInfoDetail)
xadmin.site.unregister(UserInfo)
xadmin.site.register(UserInfo, UserInfoDetail)