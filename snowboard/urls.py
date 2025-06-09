from django.urls import path

from .views import PostSnowView, PostCreateView

app_name = 'snowboard'

urlpatterns = [
    path('', PostSnowView.as_view(), name='snowboarding'),
    path('snowboarding/create/', PostCreateView.as_view(), name='post_create'),
]