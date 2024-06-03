from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.quote_list, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('authors/', views.author_list, name='author_list'),
    path('quotes/', views.quote_list, name='quote_list'),
    path('tags/<str:tag_name>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('top_tags/', views.top_tags, name='top_tags'),
    path('scrape/', views.scrape_quotes, name='scrape_quotes'),
]
