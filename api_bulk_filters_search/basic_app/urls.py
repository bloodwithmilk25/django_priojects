from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter

from .views import MovieViewSet, DirectorViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')

bulk_router = BulkRouter()
bulk_router.register(r'directors', DirectorViewSet)

urlpatterns = router.urls
urlpatterns += bulk_router.urls
