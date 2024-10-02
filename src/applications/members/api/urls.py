from rest_framework.routers import SimpleRouter

from applications.members.api.views import UserViewSet, ParticipationRequestViewSet

router = SimpleRouter()
router.register("user", UserViewSet)
router.register("participation-request", ParticipationRequestViewSet)

urlpatterns = router.urls
