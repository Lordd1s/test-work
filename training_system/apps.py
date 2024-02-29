from django.apps import AppConfig


class TrainingSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'training_system'

    def ready(self):
        import training_system.signals
