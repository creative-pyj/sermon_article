from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import SermonArticle,Member
from django.contrib import admin
from django.utils.html import strip_tags
from django.utils import timezone

@admin.display( 
    boolean=True,
    # ordering="title",
    #description="Published recently?",
    description="讲道标题"
    )

def index(request):
    articles = SermonArticle.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'articles': articles})

def search_articles(request):
    query = request.GET.get('q','')
    results = SermonArticle.objects.filter(
        Q(content_title__icontains=query) | Q(content_summary__icontains=query) |
        Q(content_scripture__icontains=query) | Q(content_sermon_translate__icontains=query)
        | Q(sermon_at__icontains=query) | Q(content_tips__icontains=query)
    ).order_by('-created_at')

    data = []
    for a in results:
        # 各エリアを結合してキーワード周辺を抜粋
        all_text = f"{a.content_title} {a.content_summary} {a.content_scripture} {a.content_sermon_translate} {a.content_tips}"
        plain_text = strip_tags(all_text)
        id = plain_text.find(query)
        start = max(0, id - 20)
        rt_text = plain_text[start:start+50]
        idx2 = rt_text.find(query)
        len_query = len(query)
        print(f"plain_text:{plain_text}")
        print(f"id:{id}")
        print(f"start:{start}")
        print(f"rt_text:{rt_text}")
        print(f"idx2:{idx2}")
        print(f"len_query:{len_query}")
        # 日付の変換処理
        # UTC(01:00) を ローカル時間(10:00) に変換し、指定の書式文字列にする
        if a.sermon_at:
            local_date = timezone.localtime(a.sermon_at)
            formatted_date = local_date.strftime('%Y年%m月%d日%H:%M')
        else:
            formatted_date = ""
        # snippet = ".    + all_text[start: start+50] + "..." if idx 1= -1 else all_text[:50]
        snippet = "..."+ rt_text[:idx2] + "<strong><span style='color: purple; text-decoration: underline;'>"+ rt_text[idx2:idx2+len_query] + "</span></strong>" + rt_text[idx2+len_query:] + "..." if idx2 != -1 else all_text[:50]
        data.append({'id':a.id,'sermon_at':formatted_date,'content_title': a.content_title,'snippet': snippet})
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