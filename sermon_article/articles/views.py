from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import SermonArticle, Member
from django.contrib import admin
from django.utils.html import strip_tags
from django.utils import timezone

@admin.display( 
    boolean=True,
    description="讲道标题"
)
def index(request):
    # Memberテーブルの情報も使うため select_related を使用して高速化
    articles = SermonArticle.objects.select_related('member').all().order_by('-created_at')
    return render(request, 'index.html', {'articles': articles})

def search_articles(request):
    query = request.GET.get('q','')
    results = SermonArticle.objects.select_related('member').filter(
        Q(content_title__icontains=query) | Q(content_summary__icontains=query) |
        Q(content_scripture__icontains=query) | Q(content_sermon_translate__icontains=query)
        | Q(sermon_at__icontains=query) | Q(content_tips__icontains=query)
    ).order_by('-created_at')

    data = []
    for a in results:
        # --- スニペット生成処理 (変更なし) ---
        all_text = f"{a.content_title} {a.content_summary} {a.content_scripture} {a.content_sermon_translate} {a.content_tips}"
        plain_text = strip_tags(all_text)
        id_loc = plain_text.find(query) # idという変数名は組み込み関数と被るため変更推奨
        start = max(0, id_loc - 20)
        rt_text = plain_text[start:start+50]
        idx2 = rt_text.find(query)
        len_query = len(query)
        
        snippet = "..."+ rt_text[:idx2] + "<strong><span style='color: purple; text-decoration: underline;'>"+ rt_text[idx2:idx2+len_query] + "</span></strong>" + rt_text[idx2+len_query:] + "..." if idx2 != -1 else all_text[:50]
        
        # --- 日付フォーマット ---
        if a.sermon_at:
            local_date = timezone.localtime(a.sermon_at)
            formatted_date = local_date.strftime('%Y年%m月%d日%H:%M')
        else:
            formatted_date = ""

        # --- メンバー情報の取得 ---
        # メンバーが紐づいていない場合のエラー回避
        if a.member:
            member_name = a.member.name
            member_kana = a.member.kana if a.member.kana else ""
            member_role = a.member.get_role_display() # "pastor"ではなく"牧師"を取得
            # 画像がある場合はそのURL、なければ空文字またはデフォルト画像
            member_image_url = a.member.image.url if a.member.image else "" 
        else:
            member_name = "ゲスト"
            member_kana = ""
            member_role = ""
            member_image_url = ""

        data.append({
            'id': a.id,
            'sermon_at': formatted_date,
            'content_title': a.content_title,
            'snippet': snippet,
            # フロントエンド表示用のデータを追加
            'member_name': member_name,
            'member_kana': member_kana,
            'member_role': member_role,
            'member_image': member_image_url,
        })
        
    return JsonResponse({'results': data})

def get_detail(request, pk):
    a = get_object_or_404(SermonArticle, pk=pk)
    return JsonResponse({
        'content_title': a.content_title, 
        'content_summary': a.content_summary,
        'content_scripture': a.content_scripture,
        'content_sermon_translate': a.content_sermon_translate,
        'content_tips': a.content_tips,
    })