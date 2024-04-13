from django.db import models
import uuid

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
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
    ews_score = models.FloatField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    def calculate_ews_score(self):
        pulse_model = [
            CentileModel.objects.filter(vital_model__name='Pulse').latest("created_at").first_percentile,
            CentileModel.objects.filter(vital_model__name='Pulse').latest("created_at").fifth_percentile,
            CentileModel.objects.filter(vital_model__name='Pulse').latest("created_at").tenth_percentile,
            CentileModel.objects.filter(vital_model__name='Pulse').latest("created_at").ninetieth_percentile,
            CentileModel.objects.filter(vital_model__name='Pulse').latest("created_at").ninetyfifth_percentile,
            CentileModel.objects.filter(vital_model__name='Pulse').latest("created_at").ninetyninth_percentile
        ]
        
        sys_model = [
            CentileModel.objects.filter(vital_model__name='Systol').latest("created_at").first_percentile,
            CentileModel.objects.filter(vital_model__name='Systol').latest("created_at").fifth_percentile,
            CentileModel.objects.filter(vital_model__name='Systol').latest("created_at").tenth_percentile,
            CentileModel.objects.filter(vital_model__name='Systol').latest("created_at").ninetieth_percentile,
            CentileModel.objects.filter(vital_model__name='Systol').latest("created_at").ninetyfifth_percentile,
            CentileModel.objects.filter(vital_model__name='Systol').latest("created_at").ninetyninth_percentile
        ]
        
        dia_model = [
            CentileModel.objects.filter(vital_model__name='Diastol').latest("created_at").first_percentile,
            CentileModel.objects.filter(vital_model__name='Diastol').latest("created_at").fifth_percentile,
            CentileModel.objects.filter(vital_model__name='Diastol').latest("created_at").tenth_percentile,
            CentileModel.objects.filter(vital_model__name='Diastol').latest("created_at").ninetieth_percentile,
            CentileModel.objects.filter(vital_model__name='Diastol').latest("created_at").ninetyfifth_percentile,
            CentileModel.objects.filter(vital_model__name='Diastol').latest("created_at").ninetyninth_percentile
        ]
        
        rr_model = [
            CentileModel.objects.filter(vital_model__name='Respiration').latest("created_at").first_percentile,
            CentileModel.objects.filter(vital_model__name='Respiration').latest("created_at").fifth_percentile,
            CentileModel.objects.filter(vital_model__name='Respiration').latest("created_at").tenth_percentile,
            CentileModel.objects.filter(vital_model__name='Respiration').latest("created_at").ninetieth_percentile,
            CentileModel.objects.filter(vital_model__name='Respiration').latest("created_at").ninetyfifth_percentile,
            CentileModel.objects.filter(vital_model__name='Respiration').latest("created_at").ninetyninth_percentile
        ]
        
        o2_model = [
            CentileModel.objects.filter(vital_model__name='Oxygen').latest("created_at").first_percentile,
            CentileModel.objects.filter(vital_model__name='Oxygen').latest("created_at").fifth_percentile,
            CentileModel.objects.filter(vital_model__name='Oxygen').latest("created_at").tenth_percentile,
            CentileModel.objects.filter(vital_model__name='Oxygen').latest("created_at").ninetieth_percentile,
            CentileModel.objects.filter(vital_model__name='Oxygen').latest("created_at").ninetyfifth_percentile,
            CentileModel.objects.filter(vital_model__name='Oxygen').latest("created_at").ninetyninth_percentile
        ]
        
        def clustering(vital_data, percentile_model):
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

        pulse_score = clustering(self.pulse, pulse_model)
        sys_score = clustering(self.systol, sys_model)
        dia_score = clustering(self.diastol, dia_model)
        rr_score = clustering(self.respiration_rate, rr_model)
        o2_score = clustering(self.oxygen_saturation, o2_model)
        ews_score = pulse_score + sys_score + dia_score + rr_score + o2_score
        return ews_score / 5

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