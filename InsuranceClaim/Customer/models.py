from django.db import models

# Create your models here.
class Insurance_Claim(models.Model):
    Age=models.CharField(max_length=250)
    Gender=models.CharField(max_length=250)
    Education=models.CharField(max_length=250)
    Occupation=models.CharField(max_length=250)
    Relationship=models.CharField(max_length=250)
    Incident_Type=models.CharField(max_length=250)
    Collision_Type=models.CharField(max_length=250)
    Incident_Severity=models.CharField(max_length=250)
    Authorities_Contacted=models.CharField(max_length=250)
    Vehicle_Damage=models.CharField(max_length=250)
    Property_Damage=models.CharField(max_length=250)
    Bodily_Injuries=models.CharField(max_length=250)
    Witness=models.CharField(max_length=250)
    Police_Report=models.CharField(max_length=250)
    Total_Claim=models.CharField(max_length=250)
    Injury_Claim=models.CharField(max_length=250)
    Property_Claim=models.CharField(max_length=250)
    Vehicle_Claim=models.CharField(max_length=250)
    Prediction=models.CharField(max_length=250)