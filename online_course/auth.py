from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView
from online_course.auth_form import AuthenticationForm
from online_course.forms import SendingEmailForm
from online_course.forms import LoginForm,RegisterForm
from django.http import HttpResponse

from django.utils.encoding import force_bytes
from django.utils.http import  urlsafe_base64_encode, urlsafe_base64_decode
from online_course.tokens import account_activation_token

from users.models import User



class LoginPage(LoginView):
    redirect_authenticated_user = True
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('customers')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password')
        return self.render_to_response(self.get_context_data(form=form))


class RegisterPage(FormView):
    template_name = 'registration//register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        send_mail(
            'User is succesfully registered',
            'Test body',
            ['avazjon867@gmail.com','otabekpdamla@gmail.com'],
            fail_silently=False
        )
        login(self.request, user,backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)

def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

class SendingEmail(View):
    sent = False

    def get(self, request, *args, **kwargs):
        form = SendingEmailForm()
        context = {
            'form': form,
            'sent': self.sent
        }
        return render(request, 'online_course/send-email.html', context)

    def post(self, request, *args, **kwargs):
        form = SendingEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient_list = form.cleaned_data['recipient_list']
            send_mail(
                subject,
                message,
                recipient_list,
                fail_silently=False
            )
            self.sent = True
            context = {
                'form': form,
                'sent': self.sent
            }
            return render(request, 'online_course/send-email.html', context)

class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponse('Thank you for your email confirmation. Now you can login to your account.')
        else:
            return HttpResponse('Activation link is invalid!')