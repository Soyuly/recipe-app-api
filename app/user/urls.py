"""
URL mappiungs for the user API>
"""
from django.urls import path

from user import views

# reverse에서 쓰는데, 앱 이름이 필요로하다.
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name="me")
]