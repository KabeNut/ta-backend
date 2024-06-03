from django.contrib import admin
from .models import *


class PatientAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "gender",
        "age",
        "height",
        "weight",
        "created_at",
        "updated_at",
        "deleted_at",
    ]


class VitalDataAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "respiration_rate",
        "oxygen_saturation",
        "pulse",
        "systol",
        "diastol",
        "temperature",
        "ews_score",
        "created_at",
        "updated_at",
        "deleted_at",
    ]


class CentileModelAdmin(admin.ModelAdmin):
    list_display = [
        "vital_model",
        "first_percentile",
        "fifth_percentile",
        "tenth_percentile",
        "ninetieth_percentile",
        "ninetyfifth_percentile",
        "ninetyninth_percentile",
        "created_at",
    ]


class VitalModelAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Patient, PatientAdmin)
admin.site.register(VitalData, VitalDataAdmin)
admin.site.register(CentileModel, CentileModelAdmin)
admin.site.register(VitalModel, VitalModelAdmin)
