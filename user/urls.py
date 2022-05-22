from django.urls import path, re_path
from .views import UserAPIView, UserLoginAPIView

urlpatterns = [
    # path('change/password/', ChangePasswordAPIView.as_view()),

    path('login/', UserLoginAPIView.as_view()),

    re_path(r'(?P<pk>[0-9]+)', UserAPIView.as_view()),
    re_path(r'', UserAPIView.as_view()),
]