from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Item, Comment, Claim

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['school_id', 'is_staff']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'found', 'claimed', 'verified']
    list_filter = ['found', 'claimed', 'verified']
    actions = ['mark_as_found', 'mark_as_returned']

    def mark_as_found(self, request, queryset):
        queryset.update(found=True)
    mark_as_found.short_description = "Mark selected items as found"

    def mark_as_returned(self, request, queryset):
        queryset.update(claimed=True, verified=True)
    mark_as_returned.short_description = "Mark selected items as returned"

admin.site.register(Comment)
admin.site.register(Claim)
