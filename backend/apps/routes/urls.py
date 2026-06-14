from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, TravelRouteViewSet

router = DefaultRouter()
router.register("", TravelRouteViewSet, basename="travel-route")

review_router = DefaultRouter()
review_router.register("", ReviewViewSet, basename="review")

urlpatterns = [
    path("", include(router.urls)),
    path("<int:route_pk>/reviews/", include(review_router.urls)),
]
