from django import forms
from .models import News


class NewsForm(forms.ModelForm):
    header = forms.CharField(
        label="Заголовок",
        help_text="Короткое название новости",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Заголовок"}
        ),
    )

    class Meta:
        model = News
        fields = "__all__"
