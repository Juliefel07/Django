from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        # Get the 10 most recent notifications
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:10]

        # Get total unread count (no slicing)
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        notifications = []
        unread_count = 0

    return {
        "notifications": notifications,
        "unread_count": unread_count,
    }
