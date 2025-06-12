
import requests
from rest_framework import serializers
from .models import SpyCat, Mission, Target

class SpyCatSerializer(serializers.ModelSerializer):
 class Meta:
        model = SpyCat
        fields = '__all__'


 def validate_breed(self, value):
        response = requests.get("https://api.thecatapi.com/v1/breeds")
        if response.status_code == 200:
            breeds = [breed['name'].lower() for breed in response.json()]
            if value.lower() not in breeds:
                raise serializers.ValidationError("Breed not found in TheCatAPI.")
        else:
            raise serializers.ValidationError("Failed to validate breed (Cat API unavailable).")
        return value

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = '__all__'
        read_only_fields = ['mission']


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, write_only=True)
    assigned_cat = serializers.PrimaryKeyRelatedField(queryset=SpyCat.objects.all(), required=False)

    class Meta:
        model = Mission
        fields = ['id', 'assigned_cat', 'is_completed', 'targets']

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission
