"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

# user_profile = [0,0,0,0,0]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', home),
    path('home/', home),
    path('closet/',closet),
    path('closet/add/',add_item),
    path('mix/', mixnmatch),
    path('about/', about),
    path('delete-item/<int:item_id>', delete_item),
    path('update-item/<int:item_id>', update_item),
    path('do-update-item/<int:item_id>', do_update),
    path('outfits/', outfits),
    path('signup/', signup, name='signup'),
    path('sign_out/', sign_out, name='sign_out'),
    path('login/', user_login, name='login'),
    path('toggle-like-outfit/<int:outfit_id>/', toggle_like_outfit, name='toggle_like_outfit'),
    path('toggle-like-items/<int:item_id>/', toggle_like_items, name='toggle_like_items'),
    path('scrape_items/', scrape_items, name='scrape_items'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
