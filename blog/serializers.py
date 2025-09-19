from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title_en', 'title_ru', 'title_uz',
            'text_en', 'text_ru', 'text_uz'
        ]



class GetPostSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'text']

    def get_title(self, obj):
        lang = self.context.get("lang", "en")
        return getattr(obj, f"title_{lang}", obj.title_en)

    def get_text(self, obj):
        lang = self.context.get("lang", "en")
        return getattr(obj, f"text_{lang}", obj.text_en)


from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)   # обязательное поле
    email = serializers.EmailField(required=True) # проверка email
    message = serializers.CharField(required=True)

    class Meta:
        model = Contact
        fields = ["id", "name", "email", "message", "created_at"]
        read_only_fields = ["id", "created_at"]
