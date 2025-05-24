import redis

class NotificationsManager:

    r = redis.Redis()

    @classmethod
    def push_notification(cls, notification: str) -> None:
        cls.r.publish("notifications", notification)


