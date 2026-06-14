from rest_framework import viewsets

from .models import Review, TravelRoute
from .serializers import ReviewSerializer, TravelRouteSerializer


class TravelRouteViewSet(viewsets.ModelViewSet):
    serializer_class = TravelRouteSerializer

    def get_queryset(self):
        queryset = (
            TravelRoute.objects.prefetch_related("stops__attraction", "bookings", "reviews")
            .all()
        )
        status = self.request.query_params.get("status")
        city = self.request.query_params.get("city")
        if status:
            queryset = queryset.filter(status=status)
        if city:
            queryset = queryset.filter(city__icontains=city)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.select_related("route").all()
        route_pk = self.kwargs.get("route_pk")
        if route_pk:
            queryset = queryset.filter(route_id=route_pk)
        else:
            route_id = self.request.query_params.get("route")
            if route_id:
                queryset = queryset.filter(route_id=route_id)
        return queryset

    def perform_create(self, serializer):
        route_pk = self.kwargs.get("route_pk")
        if route_pk:
            serializer.save(route_id=route_pk)
        else:
            serializer.save()
