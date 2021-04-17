from django.apps import AppConfig


"""
deisgn for configration, need import all singals, be careful about changes in signals.py
"""
class ChatConfig(AppConfig):
    name = 'chat'

    def ready(self):
        import chat.signals

    