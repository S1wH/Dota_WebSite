from django import forms
from teams_and_players.models import CareerPeriod, Team, Player

COUNTRY_CHOICES = (
    ("1", "Russia"),
    ("2", "US"),
    ("3", "Germany"),
    ("4", "France"),
    ("5", "Norway"),
    ("6", "China"),
)


class CareerPeriodForm(forms.ModelForm):
    class Meta:
        model = CareerPeriod
        fields = [
            "player",
            "team",
            "role",
            "start_date",
        ]


class TeamForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя",
        help_text="Имя команды",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"}),
    )

    country = forms.ChoiceField(
        label="Страна",
        choices=COUNTRY_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    establish_date = forms.DateField(
        label="Дата основания",
        help_text="Дата основания команды",
        widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "Дата"}),
    )

    logo = forms.ImageField(
        label="Логотип команды",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    biography = forms.CharField(
        label="Биография команды",
        help_text="Краткое описание команды",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Биография"}
        ),
    )

    class Meta:
        model = Team
        fields = ["name", "country", "establish_date", "logo", "biography"]


class PlayerForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя",
        help_text="Имя игрока",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"}),
    )

    nickname = forms.CharField(
        label="Ник",
        help_text="Никнейм игрока",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Никнейм"}
        ),
    )

    age = forms.IntegerField(
        label="Возраст",
        help_text="возраст игрока",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Возраст"}
        ),
    )

    birthday = forms.DateField(
        label="День рождения",
        help_text="День рождения игрока",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
            },
            format="%Y-%m-%d",
        ),
    )

    country = forms.ChoiceField(
        label="Страна",
        choices=COUNTRY_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    photo = forms.ImageField(
        label="Фото",
        help_text="Фото игрока",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    biography = forms.CharField(
        label="Биография",
        help_text="Краткое описание карьеры игрока",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Player
        fields = "__all__"
