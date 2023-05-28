from django.apps import AppConfig


class MatchesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matches'

    def ready(self):
        from django.core.signals import setting_changed
        from matches.signals import match_period_post_save
        setting_changed.connect(match_period_post_save)

