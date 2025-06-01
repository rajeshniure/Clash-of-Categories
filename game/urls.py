from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('game-board/', views.game_board, name='game_board'),
    path('reveal-card/<int:card_id>/', views.reveal_card, name='reveal_card'),
    path('reset-card/<int:card_id>/', views.reset_card, name='reset_card'),
    path('timer/', views.timer_page, name='timer'),
    path('scoring/', views.scoring_page, name='scoring'),
    path('add-team/', views.add_team, name='add_team'),
    path('delete-team/', views.delete_team, name='delete_team'),
    path('reset-points/', views.reset_points, name='reset_points'),
] 