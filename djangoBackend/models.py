from django.db import models
import uuid


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    gender = models.CharField(max_length=255, default='Male')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return self.name


class VitalData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    respiration_rate = models.FloatField()
    oxygen_saturation = models.FloatField()
    pulse = models.FloatField()
    systol = models.FloatField()
    diastol = models.FloatField()
    temperature = models.FloatField(default=32)
    ews_score = models.FloatField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    def calculate_ews_score(self):
        pulse_model = self.get_latest_percentiles("Pulse")
        sys_model = self.get_latest_percentiles("Systol")
        dia_model = self.get_latest_percentiles("Diastol")
        rr_model = self.get_latest_percentiles("Respiration")
        o2_model = self.get_latest_percentiles("Oxygen")
        temperature_model = self.get_latest_percentiles("Temperature")

        pulse_score = self.clustering(self.pulse, pulse_model)
        sys_score = self.clustering(self.systol, sys_model)
        dia_score = self.clustering(self.diastol, dia_model)
        rr_score = self.clustering(self.respiration_rate, rr_model)
        o2_score = self.clustering(self.oxygen_saturation, o2_model)
        temperature_score = self.clustering(self.temperature, temperature_model)
        ews_score = pulse_score + sys_score + dia_score + rr_score + o2_score + temperature_score
        return ews_score / 6

    def clustering(self, vital_data, percentile_model):
        if vital_data < percentile_model[0] or vital_data > percentile_model[5]:
            return 3
        elif vital_data > percentile_model[0] and vital_data < percentile_model[1]:
            return 2
        elif vital_data > percentile_model[1] and vital_data < percentile_model[2]:
            return 1
        elif vital_data > percentile_model[3] and vital_data < percentile_model[4]:
            return 1
        elif vital_data > percentile_model[4] and vital_data < percentile_model[5]:
            return 2
        else:
            return 0

    def get_latest_percentiles(self, vital_model_name):
        return [
            CentileModel.objects.filter(vital_model__name=vital_model_name)
            .latest("created_at")
            .first_percentile,
            CentileModel.objects.filter(vital_model__name=vital_model_name)
            .latest("created_at")
            .fifth_percentile,
            CentileModel.objects.filter(vital_model__name=vital_model_name)
            .latest("created_at")
            .tenth_percentile,
            CentileModel.objects.filter(vital_model__name=vital_model_name)
            .latest("created_at")
            .ninetieth_percentile,
            CentileModel.objects.filter(vital_model__name=vital_model_name)
            .latest("created_at")
            .ninetyfifth_percentile,
            CentileModel.objects.filter(vital_model__name=vital_model_name)
            .latest("created_at")
            .ninetyninth_percentile,
        ]

    def save(self, *args, **kwargs):
        self.ews_score = self.calculate_ews_score()
        super(VitalData, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.ews_score = self.calculate_ews_score()
        super(VitalData, self).save(*args, **kwargs)

    def __str__(self):
        return self.patient.name


class VitalModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CentileModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vital_model = models.ForeignKey(VitalModel, on_delete=models.CASCADE)
    first_percentile = models.FloatField()
    fifth_percentile = models.FloatField()
    tenth_percentile = models.FloatField()
    ninetieth_percentile = models.FloatField()
    ninetyfifth_percentile = models.FloatField()
    ninetyninth_percentile = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vital_model.name
