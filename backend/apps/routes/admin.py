from django.contrib import admin

from .models import Review, RouteStop, TravelRoute


class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(TravelRoute)
class TravelRouteAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "days", "status", "min_group_size", "max_group_size", "review_count", "average_rating")
    list_filter = ("status", "city")
    search_fields = ("title", "city")
    inlines = [RouteStopInline, ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer_name", "route", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("reviewer_name", "route__title", "feedback")
    readonly_fields = ("created_at",)
