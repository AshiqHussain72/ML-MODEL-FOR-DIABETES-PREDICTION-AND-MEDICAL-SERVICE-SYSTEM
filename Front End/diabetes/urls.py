from unicodedata import name
from django.urls import path
from diabetes import views as diabetes_views

app_name = 'diabetes'
urlpatterns = [
    path('',diabetes_views.index,name="index"),
    path('about/',diabetes_views.about,name="about"),
    path('blog/',diabetes_views.blog,name="blog"),
    path('analyze/',diabetes_views.analyze, name='analyze'),
    path('analyze/result/',diabetes_views.result, name='result'),
    path('predict/',diabetes_views.predict,name='predict'),
    path('report/',diabetes_views.report,name="report"),
    path('report/predict_update/<int:id>/',diabetes_views.predict_update,name="predict_update"),
    path('report/predict_delete/<int:id>/',diabetes_views.predict_delete, name='predict_delete'),


  

]
