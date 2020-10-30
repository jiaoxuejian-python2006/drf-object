from rest_framework import serializers

from api.models import Book, Press


class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Press
        fields=["press_name","pic","address"]



class BookModelSerializer(serializers.ModelSerializer):
    #自定义参数
    # aaa = serializers.SerializerMethodField()
    # def get_aaa(self,obj):
    #     return "aaa"

    #TODO 自定义连表查询 查询图书可以将图书对应的出版社信息查询出来
    #在一个序列化器内可以嵌套另外一个序列化器类来完成多表查询
    #必须时当前模型对应的外键名
    publish = PressModelSerializer()
    class Meta:
        # 指定当前序列化器要序列化的模型
        model = Book
        # 指定我需要的字段
        fields = ("book_name","price","press_name","author_list","publish")

        # 可以直接序列化所有字段
        # fields = "__all__"

        #指定不展示的字段
        # exclude = ("is_delete","status","create_time")

        #指定查询的深度
        # depth = 1


class BookDeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name","price","publish","authors")

        extra_kwargs={
            "book_name":{
                "required": True,  # 必填字段
                "min_length": 2,
                "error_messages": {
                    "required": "图书名必须提供",
                    "min_length": "图书名不能少于两个字符",
                }
            },

        }
    def validate(self, attrs):
        print(attrs)
        return attrs

#序列化与反序列化整合

class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors", "pic")

        extra_kwargs = {
            "book_name":{
                "required":True, #必填字段
                "min_length": 2,
                "error_messages":{
                    "required": "图书名必须提供",
                    "min_length": "图书名不能少于两个字符",
                }
            },
            # 指定某个字段只参与序列化
            "pic": {
                "read_only": True
            },
            # 指定某个字段只参与反序列化
            "publish": {
                "write_only": True
            },
            "authors": {
                "write_only": True
            },
        }