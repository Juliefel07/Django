from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Item, LostItem, Feedback, Claim, Profile
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import json
from .models import Student
from django.shortcuts import render, get_object_or_404, redirect
from .models import Notification
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash


User = get_user_model()


def login_signup_view(request):
    if request.method == "POST":

        # -----------------------
        # LOGIN
        # -----------------------
        if "login_submit" in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.full_name}!")
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('login')

        # -----------------------
        # SIGNUP
        # -----------------------
        elif "signup_submit" in request.POST:
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            school_id = request.POST.get('school_id')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # 🟡 Check passwords match
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect('login')

            # 🟡 Check for existing accounts
            if Student.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
                return redirect('login')
            if Student.objects.filter(school_id=school_id).exists():
                messages.error(request, "School ID already exists!")
                return redirect('login')

            # 🟢 Create new user
            user = Student.objects.create_user(
                email=email,
                full_name=full_name,
                school_id=school_id,
                password=password
            )

            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')

    return render(request, 'login.html')

def home(request):
    notifications = Notification.objects.all()
    avatars = list(range(1, 11))  # Default avatars 1–10
    return render(request, "home.html", {"avatars": avatars, "notifications": notifications})


def login_signup_view(request):
    if request.method == "POST":

        # LOGIN
        if "login_submit" in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.full_name}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password.")
                return redirect("login")

        # SIGNUP
        elif "signup_submit" in request.POST:
            full_name = request.POST.get("full_name")
            email = request.POST.get("email")
            school_id = request.POST.get("school_id")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect("login")

            if Student.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
                return redirect("login")

            if Student.objects.filter(school_id=school_id).exists():
                messages.error(request, "School ID already exists!")
                return redirect("login")

            user = Student.objects.create_user(
                email=email,
                full_name=full_name,
                school_id=school_id,
                password=password
            )

            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "")
    return redirect("login")

# ------------------------------------------------------------
# LOST ITEM REPORTING
# ------------------------------------------------------------

@login_required
def report_lost_item(request):
    """Handles lost item reporting form"""
    if request.method == "POST":
        title = request.POST.get("name")
        item_type = request.POST.get("item")
        description = request.POST.get("description")
        contact_number = request.POST.get("contact_number")
       


        # ✅ Use only valid model fields
        item = Item.objects.create(
            owner=request.user,
            title=title,
            item_type=item_type,
            description=description,
            contact_number=contact_number,
            found=False,
        )

        messages.success(request, "Your lost item report has been submitted successfully!")
        return redirect("lost_item_report")

    return render(request, "report_form.html")


@login_required
def lost_items_dashboard(request):
    """Displays all lost items with search functionality"""
    query = request.GET.get("q")
    items = Item.objects.all()

    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query))

    items = items.order_by("-created_at")
    return render(request, "lost_item_report.html", {"items": items})


@login_required
def mark_item_found(request, item_id):
    """Allows user or admin to mark an item as found"""
    item = get_object_or_404(Item, id=item_id)

    if item.owner != request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to mark this item as found.")
        return redirect("lost_item_report")

    if request.method == "POST":
        item.found = True
        item.save()
        messages.success(request, "Item marked as found.")
    return redirect("lost_item_report")
def updates(request):
    return render(request, 'updates.html')

@login_required
def item_detail(request, id):
    """Displays details of a specific item"""
    item = get_object_or_404(Item, id=id)
    return render(request, "item_detail.html", {"item": item})

# ------------------------------------------------------------
# FOUND ITEM REPORTING
# ------------------------------------------------------------

@login_required
def report_found_item(request):
    if request.method == "POST":
        title = request.POST.get("finder_name") or "None"
        item_type = request.POST.get("item_type") or "Unknown"
        finder_name = request.POST.get("finder_name") or "Unknown"
        contact_number = request.POST.get("contact_number") or "Unknown"
        place_found = request.POST.get("place_found") or "Unknown"
        found_date = request.POST.get("found_date") or timezone.now().date()
        found_description = request.POST.get("found_description") or "No description provided."

        # Create the found item
        found_item = Item.objects.create(
            owner=request.user,
            title=title,
            item_type=item_type,
            description=found_description,
            contact_number=contact_number,
            found=True,
        )

        # Find potential lost items that match the title or description
        potential_matches = Item.objects.filter(
            found=False,  # only lost items
        ).filter(
            Q(title__icontains=title) | Q(description__icontains=found_description)
        )

        # Create notifications for matches
        for lost_item in potential_matches:
            create_match_notification(lost_item, found_item)

        messages.success(request, f"Found item '{title}' added to the dashboard!")
        return redirect("lost_item_report")

    return render(request, "report_found_item.html")

# ------------------------------------------------------------
# CLAIM, EDIT, DELETE ITEMS
# ------------------------------------------------------------

@login_required
def claim_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.claimed = True
    item.save()
    messages.success(request, "Item has been claimed.")
    return redirect("lost_item_report")


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        item.title = request.POST.get("title", item.title)
        item.description = request.POST.get("description", item.description)
        item.save()
        messages.success(request, "Item updated successfully.")
        return redirect("lost_items_dashboard")

    return render(request, "edit_item.html", {"item": item})


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    messages.success(request, "Item deleted successfully.")
    return redirect("lost_items_dashboard")

# ------------------------------------------------------------
# FEEDBACK VIEWS
# ------------------------------------------------------------



@login_required
def edit_feedback(request, id):
    fb = get_object_or_404(Feedback, id=id)
    if request.method == "POST":
        fb.feedbacks = request.POST.get("feedbacks")
        fb.rating = request.POST.get("rating", fb.rating)
        fb.save()
        messages.success(request, "Feedback updated successfully.")
        return redirect("feedbacks")
    return render(request, "edit_feedback.html", {"feedback": fb})


@login_required
def delete_feedback(request, id):
    fb = get_object_or_404(Feedback, id=id)
    fb.delete()
    messages.success(request, "Feedback deleted successfully.")
    return redirect("feedbacks")

# ------------------------------------------------------------
# PROFILE & AVATAR
# ------------------------------------------------------------

@login_required
@csrf_exempt
def update_avatar(request):
    """Updates profile avatar (AJAX endpoint)"""
    if request.method == "POST":
        data = json.loads(request.body)
        avatar = data.get("avatar")
        if avatar:
            profile = request.user.profile
            profile.avatar = f"avatar{avatar}.png"
            profile.save()
            return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# ------------------------------------------------------------
# NOTIFICATIONS
# ------------------------------------------------------------


@login_required
def mark_notification_read(request, id):
    notification = get_object_or_404(Notification, id=id)
    notification.read = True
    notification.save()
    return HttpResponseRedirect(reverse("notifications_view"))

# ------------------------------------------------------------
# STATIC PAGES
# ------------------------------------------------------------

@login_required
def how_it_works(request):
    return render(request, "how_it_works.html")


def tips(request):
    return render(request, "tips.html")


def contact(request):
    return render(request, "contact.html")


def feedback_detail_view(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    return render(request, "feedback_detail.html", {"feedback": feedback})


def privacy_view(request):
    return render(request, "privacy.html")


def settings_view(request):
    return render(request, "settings.html")



@login_required
def feedbacks(request):
    """Displays and handles feedback submissions"""
    if request.method == "POST":
        # Get the name from the form, default to "Anonymous"
        name = request.POST.get("name") or "Anonymous"
        feedback_text = request.POST.get("feedbacks")
        rating = request.POST.get("rating") or 0

        # Create the feedback entry
        feedback = Feedback.objects.create(
            user=request.user,
            name=name,
            feedbacks=feedback_text,
            rating=rating
        )

        # Create a unique notification
        notif_message = f"{name} added a feedback!"
        # Check if the notification already exists for this feedback
        if not Notification.objects.filter(message=notif_message, user=request.user).exists():
            Notification.objects.create(
                user=request.user,  # Change to admin user if needed
                message=notif_message,
                is_read=False
            )

        messages.success(request, "Thank you for your feedback!")
        return redirect("feedbacks")

    # Display all feedbacks
    feedback_list = Feedback.objects.all().order_by("-id")
    return render(request, "feedbacks.html", {"feedback_list": feedback_list})

@login_required
def notifications_view(request):
    if request.user.is_staff:  # admin users see all notifications
        notifications = Notification.objects.all().order_by("-created_at")
    else:
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notifications.html", {"notifications": notifications})

@require_POST
def mark_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk)
    notif.is_read = True
    notif.save()
    return JsonResponse({'status': 'success'})

@require_POST
def mark_unread(request, pk):
    notif = get_object_or_404(Notification, pk=pk)
    notif.is_read = False
    notif.save()
    return JsonResponse({'status': 'success'})

@require_POST
def delete_notification(request, pk):
    notif = get_object_or_404(Notification, pk=pk)
    notif.delete()
    return JsonResponse({'status': 'success'})


@require_POST
def clear_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'success'})
    
@login_required
def change_password_view(request):
    if request.method == 'POST':
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')
        
        if not request.user.check_password(current):
            messages.error(request, "Current password is incorrect.")
        elif new != confirm:
            messages.error(request, "New password and confirm password do not match.")
        else:
            request.user.set_password(new)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in
            messages.success(request, "Password updated successfully!")
            return redirect('settings')  # ✅ FIXED — must match your urls.py
    return render(request, 'change_password.html')

@login_required
def how_it_works(request):
    return render(request, "how_it_works.html")

@login_required
def mark_notification_read(request, id):
    notif = get_object_or_404(Notification, id=id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def create_match_notification(lost_item, found_item):
    message = f"Potential match found! Lost item '{lost_item.title}' may match found item '{found_item.title}'."

    # Ensure the notification is linked to the item owners
    Notification.objects.create(user=lost_item.owner, message=message, is_read=False)
