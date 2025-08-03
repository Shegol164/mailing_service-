from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from mailing.models import Mailing, Message, MailingAttempt
from mailing.forms import MailingForm, MessageForm
from clients.models import Client


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        if self.request.user.is_staff:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner or self.request.user.is_staff


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner or self.request.user.is_staff


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner or self.request.user.is_staff


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt

    def get_queryset(self):
        if self.request.user.is_staff:
            return MailingAttempt.objects.all()
        return MailingAttempt.objects.filter(mailing__owner=self.request.user)
