from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import HttpResponseRedirect
from teams_and_players.models import Player, Team
from datetime import date
from teams_and_players.forms import CareerPeriodForm, TeamForm, PlayerForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def players_view(request):
    players = Player.objects.all()
    return render(request, 'teams_and_players/players.html', context={'players': players})


def get_one_player_view(request, player_id):
    player = Player.objects.get(id=player_id)
    return render(request, 'teams_and_players/one_player.html', context={'player': player})


def create_player_view(request):
    if request.method == 'GET':
        return render(request, 'teams_and_players/create_player.html', context={'is_error': False})
    else:
        error_text = None
        nickname = request.POST.get('name')
        name = request.POST.get('nickname')
        age = int(request.POST.get('age'))
        birthday = request.POST.get('birthday')
        country = request.POST.get('country')
        image = request.POST.get('photo')
        biography = request.POST.get('biography')
        if len(nickname) > 30 or len(nickname) < 5:
            error_text = 'nickname length should be in range from 5 to 30'
        elif len(name) > 30 or len(name) < 5:
            error_text = 'name length should be in range from 5 to 30'
        elif age > 99 or age <= 0:
            error_text = 'age should be in range from 1 to 99'
        elif len(country) > 20 or len(country) < 5:
            error_text = 'country length should be in range from 5 to 20'
        try:
            d = date(year=int(birthday.split('-')[0]), month=int(birthday.split('-')[1]),
                     day=int(birthday.split('-')[2]))
        except ValueError:
            error_text = 'incorrect date'
        if error_text is not None:
            return render(request, 'teams_and_players/create_player.html',
                          context={'is_error': True, 'error_text': error_text})
        Player.objects.create(
            nickname=nickname,
            name=name,
            age=age,
            birthday=birthday,
            country=country,
            photo=image,
            biography=biography,
        )
        return HttpResponseRedirect('/')


def create_career_view(request):
    if request.method == 'POST':
        form = CareerPeriodForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = CareerPeriodForm()
    return render(request, 'teams_and_players/create_career.html', context={'form': form})


class TeamListView(ListView):
    model = Team


class TeamDetailView(DetailView):
    model = Team


class TeamCreateView(UserPassesTestMixin, CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy('teams_and_players_app:team_list')

    def test_func(self):
        return self.request.user.is_staff


class TeamUpdateView(UserPassesTestMixin, UpdateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy('teams_and_players_app:team_list')

    def test_func(self):
        return self.request.user.is_staff


class TeamDeleteView(UserPassesTestMixin, DeleteView):
    model = Team
    success_url = reverse_lazy('teams_and_players_app:team_list')

    def test_func(self):
        return self.request.user.is_superuser


class PlayerListView(ListView):
    model = Player


class PlayerDetailView(DetailView):
    model = Player


class PlayerCreateView(UserPassesTestMixin, CreateView):
    model = Player
    form_class = PlayerForm
    success_url = reverse_lazy('teams_and_players_app:player_list')

    def test_func(self):
        return self.request.user.is_staff


class PlayerUpdateView(UserPassesTestMixin, UpdateView):
    model = Player
    form_class = PlayerForm
    success_url = reverse_lazy('teams_and_players_app:player_list')

    def test_func(self):
        return self.request.user.is_staff


class PlayerDeleteView(UserPassesTestMixin, DeleteView):
    model = Player
    success_url = reverse_lazy('teams_and_players_app:player_list')

    def test_func(self):
        return self.request.user.is_superuser
