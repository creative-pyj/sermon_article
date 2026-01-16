"""
URL configuration for sermon_article project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls
from articles import views

urlpatterns = [
    path('adminpyj/', admin.site.urls),
    path('', include('articles.urls')),
]
# +debug_toolbar_urls()

# ▼▼▼ 以下を追加：エラーハンドラの上書き ▼▼▼
handler404 = 'articles.views.custom_page_not_found_view'
handler500 = 'articles.views.custom_server_error_view'
handler403 = 'articles.views.custom_permission_denied_view'
handler400 = 'articles.views.custom_bad_request_view'