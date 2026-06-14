from rest_framework import serializers

from apps.attractions.serializers import AttractionSerializer
from .models import Review, RouteStop, TravelRoute


class RouteStopSerializer(serializers.ModelSerializer):
    attraction = AttractionSerializer(read_only=True)
    attraction_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RouteStop
        fields = ["id", "day", "order", "note", "attraction", "attraction_id"]


class ReviewSerializer(serializers.ModelSerializer):
    rating_label = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "route", "reviewer_name", "rating", "rating_label", "feedback", "created_at"]
        read_only_fields = ["created_at"]

    def get_rating_label(self, obj):
        return f"{obj.rating}星"

    def validate_route(self, value):
        if not value.can_review:
            raise serializers.ValidationError("该线路尚未结束，暂不能评价")
        return value


class TravelRouteSerializer(serializers.ModelSerializer):
    stops = RouteStopSerializer(many=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    ticket_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    estimated_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    enrolled_count = serializers.IntegerField(read_only=True)
    group_progress = serializers.IntegerField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    can_review = serializers.BooleanField(read_only=True)

    class Meta:
        model = TravelRoute
        fields = [
            "id",
            "title",
            "city",
            "days",
            "transport",
            "hotel_level",
            "min_group_size",
            "max_group_size",
            "base_cost",
            "guide_fee",
            "ticket_total",
            "estimated_cost",
            "status",
            "status_label",
            "enrolled_count",
            "group_progress",
            "review_count",
            "average_rating",
            "can_review",
            "description",
            "stops",
            "reviews",
        ]

    def create(self, validated_data):
        stops_data = validated_data.pop("stops", [])
        route = TravelRoute.objects.create(**validated_data)
        self._sync_stops(route, stops_data)
        return route

    def update(self, instance, validated_data):
        stops_data = validated_data.pop("stops", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if stops_data is not None:
            instance.stops.all().delete()
            self._sync_stops(instance, stops_data)
        return instance

    def _sync_stops(self, route, stops_data):
        for stop in stops_data:
            RouteStop.objects.create(
                route=route,
                attraction_id=stop["attraction_id"],
                day=stop.get("day", 1),
                order=stop.get("order", 1),
                note=stop.get("note", ""),
            )
