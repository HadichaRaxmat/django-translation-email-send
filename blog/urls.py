from django.urls import path
from .views import HomeViewSet, ContactViewSet

urlpatterns = [
    path('home/', HomeViewSet.as_view({'get': 'list'}), name='home'),
    path("contact/", ContactViewSet.as_view({'post': 'create'}), name="contact"),

]
