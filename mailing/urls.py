from django.urls import path
from . import views

app_name = 'mailing'

urlpatterns = [
    # Работа с рассылками
    path('', views.MailingListView.as_view(), name='mailing_list'),
    path('create/', views.MailingCreateView.as_view(), name='mailing_create'),

    # Просмотр попыток рассылок
    path('attempts/', views.MailingAttemptListView.as_view(), name='attempt_list'),
]