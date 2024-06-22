from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from diabetes.models import Prediction

class DiabetesPredictForm(forms.ModelForm):

    class Meta:
        model = Prediction
        
        fields = [ 'pregnancies', 'gulcose', 'blood_pressure', 'skin_thickness', 'insuline', 'bmi', 'diabetes_pedigree', 'age'  ]

