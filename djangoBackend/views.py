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
        if self.action == "restore" or "include_deleted" in self.request.query_params:
            return queryset
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
        if self.action == "restore" or "include_deleted" in self.request.query_params:
            return queryset
        return queryset.filter(deleted_at__isnull=True)

    def destroy(self, request, *args, **kwargs):
        vital_data = self.get_object()
        vital_data.deleted_at = timezone.now()
        vital_data.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def restore(self, request, *args, **kwargs):
        vital_data = self.get_object()
        vital_data.deleted_at = None
        vital_data.save()
        return Response(status=status.HTTP_200_OK)


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
