from datetime import datetime 
from django.contrib import admin
from .models import SermonArticle, Member # Memberをインポート
from django.urls import path 
from django.shortcuts import render
from django.utils.html import format_html 
from django.urls import re_path

class SermonArticleAdmin(admin.ModelAdmin):
    # フォームの並び順定義
    fieldsets = (
        ("基本情報", {"fields": ["member", "language", "content_title", "sermon_at"]}),
        ("内容", {"fields": ["content_summary", "content_scripture", "content_sermon_original", "content_sermon_translate", "content_tips"]}),
    )
    
    list_display = ["content_title", "sermon_at", "get_member_name", "created_at"]
    list_filter = ["content_title"]
    search_fields = ["content_title"]

    def get_member_name(self, obj):
        return obj.member.name if obj.member else "-"
    get_member_name.short_description = "説教者"

    # プレビュー用のURLを管理画面に追加
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/preview/', self.admin_site.admin_view(self.preview_view), name='myapp_mymodel_preview'),
            path('<id>/change/preview/',self.admin_site.admin_view(self.preview_view),name='myapp_mymodel_preview'),
        ]
        return custom_urls + urls

    # プレビュー表示用の一時View
    def preview_view(self, request, id=None):
        # フォームから送信されたメンバーIDを取得
        member_id = request.POST.get('member')
        member_obj = None
        if member_id:
            try:
                member_obj = Member.objects.get(pk=member_id)
            except Member.DoesNotExist:
                member_obj = None

        # 日時データの結合処理 (Django Adminの日付ウィジェットの仕様に合わせる)
        date_str = request.POST.get('sermon_at_0') # YYYY-MM-DD
        time_str = request.POST.get('sermon_at_1') # HH:MM:SS
        
        sermon_datetime = None
        if date_str and time_str:
            try:
                sermon_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass

        # 保存前のPOSTデータをモデルインスタンスにマッピング（保存はしない）
        obj = self.model(
            content_title=request.POST.get('content_title'),
            sermon_at=sermon_datetime,
            content_summary=request.POST.get('content_summary'), 
            content_scripture=request.POST.get('content_scripture'), 
            content_sermon_original=request.POST.get('content_sermon_original'),
            content_sermon_translate=request.POST.get('content_sermon_translate'),
            content_tips=request.POST.get('content_tips'),
            language=request.POST.get('language'),
        )
        
        # 取得したメンバーオブジェクトをセット（これがないとtemplateで member.image などが使えない）
        obj.member = member_obj

        return render(request, 'admin/preview.html', {'obj': obj})

    class Media:
        js = ('admin/js/preview.js',)

admin.site.register(SermonArticle, SermonArticleAdmin)