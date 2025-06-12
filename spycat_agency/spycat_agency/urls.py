from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from agency.views import SpyCatViewSet, MissionViewSet, TargetViewSet

router = DefaultRouter()
router.register(r'spycats', SpyCatViewSet, basename='spycat')
router.register(r'missions', MissionViewSet, basename='mission')
router.register(r'targets', TargetViewSet, basename='target')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
