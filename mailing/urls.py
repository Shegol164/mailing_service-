from django.urls import path
from mailing.views import (MailingListView, MailingCreateView, MailingUpdateView,
                         MailingDeleteView, MailingDetailView, MailingAttemptListView)

app_name = 'mailing'

urlpatterns = [
    path('', MailingListView.as_view(), name='list'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>/', MailingDetailView.as_view(), name='detail'),
    path('attempts/', MailingAttemptListView.as_view(), name='attempts'),
]
