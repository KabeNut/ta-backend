from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import *
from .serializers import *


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        queryset = Patient.objects.all()
        if (
            self.action == "restore"
            or self.request.query_params.get("filter") == "include_deleted"
        ):
            return queryset
        elif self.request.query_params.get("filter") == "only_deleted":
            return queryset.filter(deleted_at__isnull=False)
        else:
            return queryset.filter(deleted_at__isnull=True)

    def destroy(self, request, *args, **kwargs):
        patient = self.get_object()
        patient.deleted_at = timezone.now()
        patient.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def restore(self, request, *args, **kwargs):
        patient = self.get_object()
        patient.deleted_at = None
        patient.save()
        return Response(status=status.HTTP_200_OK)


class VitalDataViewSet(viewsets.ModelViewSet):
    serializer_class = VitalDataSerializer

    def get_queryset(self):
        queryset = VitalData.objects.all()
        if (
            self.action == "restore"
            or self.request.query_params.get("filter") == "include_deleted"
        ):
            return queryset
        elif self.request.query_params.get("filter") == "only_deleted":
            return queryset.filter(deleted_at__isnull=False)
        return queryset.filter(deleted_at__isnull=True)

    def destroy(self, request, *args, **kwargs):
        vital_data = self.get_object()
        vital_data.deleted_at = timezone.now()
        vital_data.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def restore(self, request, *args, **kwargs):
        vital_data = self.get_object()
        vital_data.deleted_at = None
        vital_data.save()
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        pulse_model = instance.get_latest_percentiles("Pulse")
        sys_model = instance.get_latest_percentiles("Systol")
        dia_model = instance.get_latest_percentiles("Diastol")
        rr_model = instance.get_latest_percentiles("Respiration")
        o2_model = instance.get_latest_percentiles("Oxygen")
        temperature_model = instance.get_latest_percentiles("Temperature")

        pulse_score = instance.clustering(instance.pulse, pulse_model)
        sys_score = instance.clustering(instance.systol, sys_model)
        dia_score = instance.clustering(instance.diastol, dia_model)
        rr_score = instance.clustering(instance.respiration_rate, rr_model)
        o2_score = instance.clustering(instance.oxygen_saturation, o2_model)
        temperature_score = instance.clustering(instance.temperature, temperature_model)

        calculations = {
            "respiration_rate": rr_score,
            "oxygen_saturation": o2_score,
            "pulse": pulse_score,
            "systol": sys_score,
            "diastol": dia_score,
            "temperature": temperature_score,
        }

        serializer = self.get_serializer(instance)
        data = serializer.data
        data["calculations"] = calculations
        return Response(data)


class CentileModelViewSet(viewsets.ModelViewSet):
    queryset = CentileModel.objects.all()
    serializer_class = CentileModelSerializer

    @action(detail=True, methods=["get"])
    def getLatest(self, request, *args, **kwargs):
        centile_model = CentileModel.objects.filter(
            vital_model__name=kwargs["pk"]
        ).latest("created_at")
        serializer = CentileModelSerializer(centile_model)
        return Response(serializer.data)


class VitalModelViewSet(viewsets.ModelViewSet):
    queryset = VitalModel.objects.all()
    serializer_class = VitalModelSerializer
