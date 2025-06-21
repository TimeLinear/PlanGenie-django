import firebase_admin
from firebase_admin import messaging, credentials
from django.conf import settings

if not firebase_admin._apps and settings.FIREBASE_CREDENTIALS:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)


def get_device_token(user_uuid: str) -> str:
    """Mock function to return device token from user uuid."""
    return f"test-token-{user_uuid}"


def send_push_notification(token: str, title: str, body: str) -> None:
    message = messaging.Message(notification=messaging.Notification(title=title, body=body), token=token)
    try:
        messaging.send(message)
    except Exception:
        pass