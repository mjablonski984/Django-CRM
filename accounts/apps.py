from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    # Override ready to make signals work when in separate file  
    # ( In settings.py make sure app is named as accounts.apps.AccountsConfig and not just accounts)
    def ready(self):
        import accounts.signals

    # If you dont want to override ready method in __init__.py add: default_app_config = 'accounts.apps.AccountsConfig')