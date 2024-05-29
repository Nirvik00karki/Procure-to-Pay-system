from django.apps import AppConfig


class P2PAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'p2p_app'

    def ready(self):
        import p2p_app.signals 


