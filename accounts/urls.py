from django.urls import path
# from . views import register_view, login_view, logout_view
from . views import home_view,all_news_view, epaper_list_view, epaper_detail_view
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home_view, name='home'),
    path('search/', views.search_view, name='search'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('category/<str:category>/', views.category_view, name='category'),
    path('article/<int:pk>/', views.article_detail_view, name='article_detail'),
    path('all-news/', views.all_news_view, name='all_news'),  # New URL for all news
    path('epapers/', epaper_list_view, name='epaper_list'),
    path('epaper/<int:pk>/', epaper_detail_view, name='epaper_detail'),


    # path('register/', register_view, name='register'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

