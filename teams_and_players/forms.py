from django import forms
from teams_and_players.models import CareerPeriod


class CareerPeriodForm(forms.ModelForm):

    class Meta:
        model = CareerPeriod
        fields = [
            'player',
            'team',
            'role',
            'start_date',
        ]
