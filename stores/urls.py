from rest_framework.routers import DefaultRouter
from stores import views

router = DefaultRouter()
router.register(r'regions', views.RegionalViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'', views.StoreViewSet)

urlpatterns = router.urls
