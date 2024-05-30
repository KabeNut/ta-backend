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
    vital_model = VitalModelSerializer(read_only=True)

    class Meta:
        model = CentileModel
        fields = "__all__"


class VitalDataSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    class Meta:
        model = VitalData
        fields = "__all__"
