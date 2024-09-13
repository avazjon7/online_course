from django import forms
# from jazzmin.templatetags.jazzmin import User
from online_course.models import Customer
from users.models import Users

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255)
    username = forms.CharField(max_length=100, required=False)
    class Meta:
        model = Users
        fields = ('username', 'email', 'password')

    def clean_username(self):
        email = self.data.get('email')
        if Users.objects.filter(username=email).exists():
            raise forms.ValidationError(f'This {email} is already exists')
        return email

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['password']


    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True

        if commit:
            user.save()

        return user


class SendingEmailForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
    from_to = forms.EmailField(required=True)
    recipient = forms.EmailField(required=True)



