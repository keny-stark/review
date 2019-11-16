from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from accounts.models import Profile


class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username', required=True)
    password = forms.CharField(max_length=100, label='Password', required=True,
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=100, label='Password Confirm', required=True,
                                       widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise ValidationError('User with this email already exists',
                                  code='user_email_exists')
        except User.DoesNotExist:
            return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise ValidationError('User with this username already exists',
                                  code='user_username_exists')
        except User.DoesNotExist:
            return username

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_confirm']
        if password_1 != password_2:
            raise ValidationError('Passwords do not match',
                                  code='passwords_do_not_match')
        return self.cleaned_data


class UserChangeForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', required=False)
    birth_date = forms.DateField(label='День рождения', input_formats=['%Y-%m-%d', '%d.%m.%Y'], required=False)
    site = forms.URLField(max_length=255, label='Сайт', required=False)

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            return getattr(self.instance.profile, field_name)
        return super().get_initial_for_field(field, field_name)

    def clean_site(self):
        url = self.cleaned_data.get('site', '')
        if url:
            protocol, full_path = url.split('://', 1)
            site_name = full_path.split('/', 1)[0]
            site_name = site_name.split('?', 1)[0]
            print(site_name)
            if site_name != 'github.com':
                raise ValidationError('wrong site. only github.com))')
        return url

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.profile = self.save_profile(commit)
        return user

    def save_profile(self, commit=True):
        profile, _ = Profile.objects.get_or_create(user=self.instance)
        for field in self.Meta.profile_fields:
            setattr(profile, field, self.cleaned_data.get(field))
        if not profile.avatar:
            profile.avatar = None
        if commit:
            profile.save()
        return profile

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar', 'birth_date']
        profile_fields = ['avatar', 'birth_date', 'site']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="New Password", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm the password", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="old password", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Old password is incorrect!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'old_password']


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True, label='Email')
#
#     class Meta(UserCreationForm.Meta):
#         fields = ('username', 'email')
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         try:
#             User.objects.get(email=email)
#             raise ValidationError('Email already registered.', code='email_registered')
#         except User.DoesNotExist:
#             return email
