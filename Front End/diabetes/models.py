from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator 
from decimal import Decimal

# Create your models here.
class Prediction(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pregnancies = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    gulcose = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    blood_pressure = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    skin_thickness = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    insuline = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    bmi = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    diabetes_pedigree = models.DecimalField(max_digits=10, decimal_places=4, validators=[MinValueValidator(Decimal('0.00'))])

    age = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    
    date_posted = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=255)

    def __str__(self) :
        return f"{self.user} Report"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ['-date_posted']
    

    
class Carausel(models.Model):
    image = models.ImageField(upload_to='pics/%y/%m/%d')
    title = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class DiabetesTypes(models.Model):
    image = models.ImageField(upload_to='pics/diabetestype/%y/%m/%d')
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title
