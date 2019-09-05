from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', posts_list, name='post_list_url'),
    path('post/create/', PostCreate.as_view(), name='post_create_url'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('post/<str:slug>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('post/<str:slug>/delete/', PostDelete.as_view(), name='post_delete_url'),
    path('post/<str:slug>/list_comment', Leave_comment.as_view(), name='post_detail_url_comment'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<str:slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('tag/<str:slug>/delete/', TagDelete.as_view(), name='tag_delete_url'),
    path('identification/', LoginUser.as_view(), name='login_user_url'),
    path('logout/', user_logout, name='logout_url'),
    path('adduz/', AddUz.as_view(), name='adduz_url'),
]
