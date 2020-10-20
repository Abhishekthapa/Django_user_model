
from django.urls import path, include
from blog.views import (
    create_blog_view,
    detail_blog_view,
    edit_blog_view,
)

# whenever urls.py is created in an app
# this should be done
app_name = 'blog'

urlpatterns = [
    path('create/', create_blog_view, name='create'),
    path('<slug>/', detail_blog_view, name='detail'),
    path('<slug>/edit', edit_blog_view, name='edit'),

]
