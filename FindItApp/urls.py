from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_signup_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('lost_item_report/', views.lost_items_dashboard, name='lost_item_report'),

    path('post_item/', views.report_lost_item, name='post_item'),
    path('item/<int:item_id>/found/', views.mark_item_found, name='mark_item_found'),
    path('how_it_works/', views.how_it_works, name='how_it_works'),
    path('tips/', views.tips, name='tips'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedbacks, name='feedbacks'),
    path('report_found_item/', views.report_found_item, name='report_found_item'), 
    path('lost-item/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('lost-item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('claim_item/<int:item_id>/', views.claim_item, name='claim_item'),
    path('report/', views.report_lost_item, name='report_lost_item'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('notification/mark_read/<int:id>/', views.mark_notification_read, name='mark_notification_read'),
    path('feedback/<int:id>/edit/', views.edit_feedback, name='edit_feedback'),
    path('feedback/<int:id>/delete/', views.delete_feedback, name='delete_feedback'),
    path("update-avatar/", views.update_avatar, name="update_avatar"),
    path('feedback/<int:feedback_id>/', views.feedback_detail_view, name='feedback_detail'),
    path('notifications/', views.notifications_view, name='notifications_view'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('lost_item_report/', views.lost_items_dashboard, name='lost_items_dashboard'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('mark_read/<int:pk>/', views.mark_read, name='mark_read'),
    path('mark_unread/<int:pk>/', views.mark_unread, name='mark_unread'),
    path('notifications/read/<int:id>/', views.mark_notification_read, name='mark_notification_read'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('settings/', views.settings_view, name='settings'),
    path('updates/', views.updates, name='updates'),
    path('delete_notification/<int:pk>/', views.delete_notification, name='delete_notification'),
    path('clear_notifications/', views.clear_notifications, name='clear_notifications'),
    path('settings/change-password/', views.change_password_view, name='change_password'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('notifications/mark-read/<int:id>/', views.mark_notification_read, name='mark_notification_read'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
