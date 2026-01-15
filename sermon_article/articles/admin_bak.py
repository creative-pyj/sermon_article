from datetime import datetime 
from django.contrib import admin
from .models import SermonArticle 
from django.urls import path 
from django. shortcuts import render
from django.utils.html import format_html 
from django.urls import re_path

class SermonAiticleInline(admin.TabularInline):
    model = SermonArticle
    extra = 3

class SermonArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        ("讲道内容", {"fields": ["language","content_title", "sermon_at", "content_summary", "content_scripture", "content_sermon_original", "content_sermon_translate", "content_tips"]}),
    )
    #inlines = [SermonArticleInline]
    list_display = ["content_title", "sermon_at", "created_at"]
    list_filter = ["content_title"]
    search_fields = ["content_title"]

# 1.すでに登録されている場合は、一度解除する
# try:
#admin.site. unregister(SermonArticle)
# except admin.sites. NotRegistered:
#
#pass
# @admin.register(SermonArticle)
# class MyModelAdmin(admin.ModelAdmin):

    # プレビュー用のURLを管理画面に追加
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/preview/', self.admin_site.admin_view(self.preview_view), name='myapp_mymodel_preview'),
            path('<id>/change/preview/',self.admin_site.admin_view(self.preview_view),name='myapp_mymodel_preview'),
            # re_path(r*^ self.admin_site.admin_view(self.preview_view),name="myapp_mymode]_preview"),
        ]
        return custom_urls + urls

    # プレビュー表示用の一時View
    def preview_view(self, request,id=None):
        #保存前のPOSTデータをモデルインスタンスにマッピング（保存はしない）
        req_sermon_at_0 =request.POST.get('sermon_at_0')
        req_sermon_at_1 =request.POST.get('sermon_at_1')
        obj = self.model(
            # id=request.POST.get ('id'),
            content_title=request.POST.get('content_title'),
            sermon_at = datetime.strptime(f"{request.POST.get('sermon_at_0')} {request.POST.get('sermon_at_1')}", "%Y-%m-%d %H:%M:%S"),
            content_summary=request.POST.get('content_summary'), 
            content_scripture=request.POST.get('content_scripture'), 
            content_sermon_original=request.POST.get('content_sermon_original'),
            content_sermon_translate=request.POST.get('content_sermon_translate'),
            content_tips=request.POST.get('content_tips'),
            )

        return render(request, 'admin/preview.html', {'obj': obj})

# 編集画面に「プレビュー」ボタンを追加するためのJS
    class Media:
        js = ('admin/js/preview.js',)

admin.site.register(SermonArticle,SermonArticleAdmin)