from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @action(detail=True, methods=['post'])
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        cat_id = request.data.get('cat_id')

        try:
            cat = SpyCat.objects.get(id=cat_id)
        except SpyCat.DoesNotExist:
            return Response({'error': 'SpyCat not found'}, status=404)

        if cat.mission_set.exists():
            return Response({'error': 'Cat already has a mission'}, status=400)

        mission.assigned_cat = cat
        mission.save()
        return Response({'message': 'Cat assigned successfully'})


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def update(self, request, *args, **kwargs):
        target = self.get_object()
        mission = target.mission

        if target.is_completed or mission.is_completed:
            return Response({'error': 'Cannot update completed target or mission'}, status=400)

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        target = self.get_object()
        target.is_completed = True
        target.save()

        # Автоматичне завершення місії
        mission = target.mission
        if all(t.is_completed for t in mission.targets.all()):
            mission.is_completed = True
            mission.save()

        return Response({'message': 'Target marked as complete'})
