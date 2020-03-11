from django.urls import path
from poll import views

urlpatterns = [
    path('', views.index, name='index'),
    path('poll/add/', views.poll_add, name='poll_add'),
    path('poll/detail/<int:poll_id>/', views.detail, name='detail'),
    path('poll/mine/', views.mine, name='mine'),
    path('poll/mine/del/<int:poll_id>/', views.poll_delete, name='poll_delete'),
    path('poll/edit/<int:poll_id>/', views.edit, name='edit'),
    path('poll/edit/vote/save/<int:poll_id>/', views.choice_save, name='vote_save'),
    path('poll/edit/delete/<int:poll_id>/<int:choice_id>/', views.choice_delete, name='choice_delete'),
    path('poll/edit/add/<int:poll_id>/', views.choice_add, name='choice_add'),
    path('poll/detail/vote/<int:poll_id>/', views.vote, name='vote'),
]
