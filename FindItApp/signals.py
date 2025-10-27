# signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Feedback, Notification
from django.contrib.auth.models import User

# Set up logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Feedback)
# In signals.py, inside your notification creation logic
def create_feedback_notification(sender, instance, created, **kwargs):
    if created and instance.user:  # Ensure instance.user is not None
        # If using school_id as the identifier:
        message = f"{instance.user.school_id} added a feedback."
        # Or if you want to use something else:
        # message = f"{instance.user.first_name} {instance.user.last_name} added a feedback."
        
        # Create the notification
        Notification.objects.create(
            user=instance.user, 
            message=message
        )
