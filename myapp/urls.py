from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.HomeView.as_view(), name='home'),
    path('news/detail/<int:id>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('about/', views.AboutView.as_view(), name='about'),

    # Category
    path('create-category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('update-category/<int:id>/', views.UpdateCategoryView.as_view(), name='update_category'),
    path('delete-category/<int:id>/', views.DeleteCategoryView.as_view(), name='delete_category'),

    # News
    path('create-news/', views.CreateNewsView.as_view(), name='create_news'),
    path('update-news/<int:id>/', views.UpdateNewsView.as_view(), name='update_news'),
    path('delete-news/<int:id>/', views.DeleteNewsView.as_view(), name='delete_news'),

    # Signin/Signup
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]