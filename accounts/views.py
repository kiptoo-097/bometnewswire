from django.shortcuts import render, get_object_or_404
from .models import NewsArticle, Epaper

def home_view(request):
    latest_trending_news = NewsArticle.objects.filter(trending=True).order_by('-date_published').first()
    latest_news = NewsArticle.objects.exclude(pk=latest_trending_news.pk).order_by('-date_published')[:5] if latest_trending_news else []
    trending_news = NewsArticle.objects.filter(trending=True).order_by('-date_published')[1:5] if latest_trending_news else []
    additional_news = NewsArticle.objects.exclude(pk=latest_trending_news.pk).order_by('-date_published')[1:10] if latest_trending_news else []

    latest_epaper = Epaper.objects.latest('date_uploaded') if Epaper.objects.exists() else None
    latest_epapers = Epaper.objects.all().order_by('-date_uploaded')[:3] if Epaper.objects.exists() else []
    
    context = {
        'main_news': latest_trending_news,
        'latest_news': latest_news,
        'trending_news': trending_news,
        'additional_news': additional_news,
        'latest_epaper': latest_epaper,
        'latest_epapers': latest_epapers,
    }
    return render(request, 'accounts/home.html', context)

def news_detail(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    return render(request, 'accounts/news_detail.html', {'article': article})


def category_view(request, category):
    articles = NewsArticle.objects.filter(category=category).order_by('-date_published')
    paginator = Paginator(articles, 6)  # 6 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/category.html', {'category': category, 'page_obj': page_obj})


def article_detail_view(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    return render(request, 'accounts/article_detail.html', {'article': article})

def search_view(request):
    query = request.GET.get('q')
    if query:
        results = NewsArticle.objects.filter(title__icontains=query)
    else:
        results = NewsArticle.objects.none()
    
    return render(request, 'accounts/search_results.html', {'results': results, 'query': query})

from django.core.paginator import Paginator

def all_news_view(request):
    all_articles = NewsArticle.objects.order_by('-date_published')
    paginator = Paginator(all_articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/all_news.html', {'page_obj': page_obj})

from .models import Epaper
from django.core.paginator import Paginator

def epaper_list_view(request):
    epapers = Epaper.objects.all().order_by('-date_uploaded')
    paginator = Paginator(epapers, 6)  # Show 6 epapers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'epaper/epaper_list.html', {'page_obj': page_obj})

def epaper_detail_view(request, pk):
    epaper = get_object_or_404(Epaper, pk=pk)
    return render(request, 'epaper/epaper_detail.html', {'epaper': epaper})