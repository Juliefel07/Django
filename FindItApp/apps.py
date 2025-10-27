from django.apps import AppConfig

class FinditappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FindItApp'

    def ready(self):
        # Import signals here so they are registered when the app is ready
        import FindItApp.signals  # Ensure your signals module is imported
