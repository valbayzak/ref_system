from django.urls import path, include
from . import views
urlpatterns = [
    path('register/', views.register_user),
    path('db_invite/', include('oper.views.check_invite(phone)'),  name='check_number')
]