from abc import ABC, abstractmethod
# Bad solution
class NotificationService:
    def send_notification(self, notification_type, message, user):
        if notification_type == "email":
            return f"Email {message}, has been sent to {user}"
        elif notification_type == "sms":
            return f"SMS {message} has been sent to {user}"
        elif notification_type == "Push":
            return f"Push notification {message} has been sent to {user}"
        else:
            raise ValueError(f"Unkown type {notification_type}")

service = NotificationService()
service.send_notification("email", "Welcome on board", "john@a.c")
# It's bad solution, our class would be extremely long, it's hard do debug etc 


# Good solution 
class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, message, user):
        pass 
    # we create an interface

# each strategy gets its own class
class EmailStrategy(NotificationStrategy):
    def send(self, message, user):
        print("Connecting to SMTP server on port 587...")
        print(f"Sending Email to {user}: {message}")

class SmsStrategy(NotificationStrategy):
    def send(self, message, user):
        print("Authorizing via SMS gateway token...")
        print(f"Sending SMS to {user}: {message}")

class PushStrategy(NotificationStrategy):
    def send(self, message, user):
        print("Connecting to Firebase Cloud Messaging...")
        print(f"Sending Push notification to {user}: {message}")


class BetterNotificationService:
    def __init__(self, strategy: NotificationStrategy):
        self._strategy = strategy
    def notify(self, message, user):
        self._strategy.send(message, user)
    def set_strategy(self, strategy: NotificationStrategy):
        self._strategy = strategy

email_strategy = EmailStrategy()
service = BetterNotificationService(email_strategy)
service.notify("Hello on board", "john@a.c")

print ("-" * 40)

sms_strategy = SmsStrategy()
service.set_strategy(sms_strategy)
service.notify("Your auth is: 1234", "+48 123 456 000")

# PROS:
# + easier to debug (we can isolate each strategy)
# + open / closed rule
# CONS:
# - a lot of new small clases & new files
# - client has to know which strategies exists