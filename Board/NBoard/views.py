from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.core.mail import send_mail
import random
import string
from django.contrib.auth import login, authenticate

@login_required
def accept(request, pk):
    Response.objects.filter(response_to_id=pk).update(accepted=True)

    instance = Response.objects.filter(response_to_id=pk)
    post_author = list(instance.values_list('response_to__user__username', flat=True))
    post_id = list(instance.values_list('response_to__id', flat=True))
    response_user = list(instance.values_list("response_user__username", flat=True))
    email = list(instance.values_list("response_user__email", flat=True))

    send_mail(
        subject=post_author[0],
        message=f"Greetings, {response_user[0]}\n"
                f"Your response to {post_author[0]}'s post has been accepted!",
        from_email='',
        recipient_list=[email[0]])

    return HttpResponseRedirect(f'/accounts/profile/post/{post_id[0]}/')

def register_view(request):
    form = BaseRegisterForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        a = OneTimeCode.objects.create(code=''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10)), user=user)
        send_mail(
            subject="Registration Code",
            message=f"Greetings, {username}\n"
                    f"Your registration code: {a.code}\n",
            from_email='',
            recipient_list=[email])
        return redirect('/accounts/register/otc/')
    else:
        form = BaseRegisterForm
    return render(request, 'registration/register.html', {'form': form})

def mass_mail(request):
    form = MassMailForm(request.POST)
    if form.is_valid():
        form.save()
        subject = form.cleaned_data.get('title')
        text = form.cleaned_data.get('text')
        mail_list = [mail for mail in User.objects.all().values_list('email', flat=True)[1:]]
        send_mail(
            f'{subject}',
            f'{text}',
            '',
            mail_list
        )
        return redirect('/')
    return render(request, 'send_mass_mail.html', {'form': form})

def otc(request):
    form = OneTimeForm(request.POST)
    if form.is_valid():
        code = request.POST['code']
        a = OneTimeCode.objects.filter(code=code)
        if a.exists():
            login(request, OneTimeCode.objects.get(code=code).user)
            a.delete()
            return redirect('/accounts/profile/')
        else:
            raise forms.ValidationError(
                'wrong code'
            )
    else:
        form = OneTimeForm()
    return render(request, 'registration/otc.html', {'form': form})

class Board(ListView):
    model = BoardNotice
    ordering = '-creation'
    template_name = 'board.html'
    context_object_name = 'board'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset()


class MyResponses(ListView):
    model = BoardNotice
    ordering = '-creation'
    template_name = 'my_responses.html'
    context_object_name = 'board'

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = Response.objects.filter(response_user=self.request.user)
        return context


class MyResponsesPost(DetailView):

    model = BoardNotice
    ordering = ['-creation']
    template_name = 'my_post_responses.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.filter(response_to_id=self.kwargs.get('pk'))
        return context


class DeleteResponse(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'delete.html'
    success_url = '/accounts/profile/'


class NoticeDetail(LoginRequiredMixin, DetailView):
    model = BoardNotice
    template_name = 'notice.html'
    context_object_name = 'post'


class RespondToPost(LoginRequiredMixin, CreateView):
    model = Response
    form = ResponseForm
    fields = ['text',]
    template_name = 'respond.html'
    success_url = "/board/post/{}"
    context_object_name = 'response'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.response_user = self.request.user
        self.object.response_to_id = self.kwargs.get('pk')
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse('notice_detail', kwargs={'pk': self.kwargs.get('pk')})


class DeletePost(LoginRequiredMixin, DeleteView):
    model = BoardNotice
    template_name = 'delete.html'
    success_url = reverse_lazy('board')


class CreateNotice(LoginRequiredMixin, CreateView):
    form_class = BoardForm
    model = BoardNotice
    template_name = 'notice_edit.html'
    context_object_name = 'board_new'
    success_url = reverse_lazy('board')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EditNotice(LoginRequiredMixin, UpdateView):
    form_class = BoardForm
    model = BoardNotice
    template_name = 'notice_edit.html'
    context_object_name = 'board_new'
    success_url = reverse_lazy('board')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
