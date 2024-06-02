from rest_framework import serializers
from .models import *


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class VitalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalData
        fields = "__all__"


class VitalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalModel
        fields = "__all__"


class CentileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentileModel
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["vital_model"] = VitalModelSerializer(instance.vital_model).data
        return response


class VitalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalData
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["patient"] = PatientSerializer(instance.patient).data
        return response
