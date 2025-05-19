from rest_framework.routers import DefaultRouter
from song.views import SongViewSet

router = DefaultRouter()
router.register(r'song', SongViewSet)

urlpatterns = router.urls 
