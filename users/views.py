from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView
from config.settings import EMAIL_DEFAULT_SENDER
from users.forms import LoginForm, RegisterModelForm, SendingEmailForm
from users.authentication_form import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from users.models import User
from users.tokens import account_activation_token


class LoginPage(LoginView):
    redirect_authenticated_user = True
    form_class = AuthenticationForm
    template_name = 'online_course/register/login.html'

    def get_success_url(self):
        return reverse_lazy('online_course')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password')
        return self.render_to_response(self.get_context_data(form=form))


class RegisterPage(FormView):
    template_name = 'online_course/register/register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('online_course')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Send activation email
        current_site = get_current_site(self.request)
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email = EmailMessage(
            'Activate your account',
            message,
            EMAIL_DEFAULT_SENDER,
            [user.email],
        )
        email.content_subtype = 'html'
        email.send()

        return HttpResponse('<h1>Please confirm your email address to complete the registration</h1>')


class LogoutPage(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponse("Вы успешно вышли из системы.")


class SendingEmail(View):
    sent = False

    def get(self, request, *args, **kwargs):
        form = SendingEmailForm()
        context = {
            'form': form,
            'sent': self.sent
        }
        return render(request, 'users/send-email.html', context)

    def post(self, request, *args, **kwargs):
        form = SendingEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient_list = form.cleaned_data['recipient_list']
            send_mail(
                subject,
                message,
                EMAIL_DEFAULT_SENDER,
                recipient_list,
                fail_silently=False
            )
            self.sent = True
            context = {
                'form': form,
                'sent': self.sent
            }
            return render(request, 'users/send-email.html', context)


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')
