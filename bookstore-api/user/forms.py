from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from store.models import Review
from order.models import Address
from crispy_forms.helper import FormHelper

# Create your models here.
class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        required=True,
        error_messages={
            'required': 'Vui lòng nhập họ của bạn',
        },
    )
    last_name = forms.CharField(
        required=True,
        error_messages={
            'required': 'Vui lòng nhập tên của bạn',
        },
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Vui lòng nhập email của bạn',
        },
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()

        return user
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get("email")
        # bug
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is invalid')
        # len function updated ###
        if len(email) >= 350:
            raise forms.ValidationError("Your email is too long")
        return email

class UpdateUserForm(forms.ModelForm):

    first_name = forms.CharField(
        required=True,
        error_messages={
            'required': 'Vui lòng nhập họ của bạn',
        },
    )
    last_name = forms.CharField(
        required=True,
        error_messages={
            'required': 'Vui lòng nhập tên của bạn',
        },
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Vui lòng nhập email của bạn',
        },
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # bug
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is invalid')
        # len function updated ###
        if len(email) >= 350:
            raise forms.ValidationError("Your email is too long")
        return email

class ReviewForm(forms.ModelForm):
    review_star = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    review_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write Your Review'}))

    class Meta:
        model = Review
        fields = [
            'review_star',
            'review_text'
        ]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
