from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Post
from .serializers import GetPostSerializer


class HomeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Получить список постов на нужном языке",
        responses={200: GetPostSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                "lang",
                openapi.IN_QUERY,
                description="Язык ответа (например: en, ru, uz). "
                            "По умолчанию определяется по URL (/ru/home/).",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def list(self, request):
        lang = request.LANGUAGE_CODE
        posts = Post.objects.all()
        serializer = GetPostSerializer(posts, many=True, context={"lang": lang})
        return Response(serializer.data)



from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import ContactSerializer
from .tasks import send_contact_email

class ContactViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            # запускаем задачу Celery
            send_contact_email.delay(contact.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# django-admin makemessages -l ru
# django-admin makemessages -l uz
# django-admin compilemessages