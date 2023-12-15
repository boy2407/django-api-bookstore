from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Review
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    review_star = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    review_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, }),
        required=True,
        error_messages={
            'required': 'Vui lòng nhập bình luận của bạn',
        },
    )
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

