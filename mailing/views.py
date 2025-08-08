from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Mailing, Message, MailingAttempt
from .tasks import send_mailing_task
from django.db.models import Count


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user).annotate(
            attempts_count=Count('mailingattempt')
        ).select_related('message').prefetch_related('clients')


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'message', 'clients']
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
        form.fields['clients'].queryset = self.request.user.client_set.all()
        return form


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'message', 'clients']
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
        form.fields['clients'].queryset = self.request.user.client_set.all()
        return form


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class SendMailingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = Mailing.objects.filter(owner=request.user, pk=pk).first()
        if mailing:
            send_mailing_task.delay(mailing.id)
        return redirect('mailing:mailing_detail', pk=pk)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/attempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        return MailingAttempt.objects.filter(
            mailing__owner=self.request.user
        ).select_related('mailing', 'mailing__message')