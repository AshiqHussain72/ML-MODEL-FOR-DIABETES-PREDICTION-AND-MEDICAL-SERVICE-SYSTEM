from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import DiabetesPredictForm
from django.contrib import messages
from diabetes.models import Prediction

from .models import Carausel, DiabetesTypes

# Create your views here.


# carausel
def index(request):
    obj = Carausel.objects.all()
    diabetes_type = DiabetesTypes.objects.all()
    context = {
        "obj": obj,
        "diabetes_type":diabetes_type,
        }
    return render(request, "diabetes/index.html", context)


def about(request):
    return render(request, "diabetes/about.html")


def blog(request):
    return render(request, "diabetes/blog.html")


def analyze(request):
    return render(request, "diabetes/analyze.html")


def result(request):
    # loading dataset
    data = pd.read_csv("diabetes.csv")
    # train test split
    X = data.drop("Outcome", axis=1)
    Y = data["Outcome"]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    # Trainning the Model
    model = LogisticRegression()
    model.fit(X_train, Y_train)

    val1 = float(request.GET["pregnancies"])
    val2 = float(request.GET["gulcose"])
    val3 = float(request.GET["blood_pressure"])
    val4 = float(request.GET["skin_thickness"])
    val5 = float(request.GET["insuline"])
    val6 = float(request.GET["bmi"])
    val7 = float(request.GET["diabetes_pedigree"])
    val8 = float(request.GET["age"])

    pred = model.predict([[val1, val2, val3, val4, val5, val6, val7, val8]])

    result1 = ""
    if pred == [1]:
        result1 = "Positive"
    else:
        result1 = "Negative"

    return render(request, "diabetes/analyze.html", {"result2": result1})


# currently in USE to predict
def predict(request):
    username = None
    if request.user.is_authenticated:
        username = request.user
        # print(username)

    if request.method == "POST":
        form = DiabetesPredictForm(request.POST)
        # loading dataset
        data = pd.read_csv("diabetes.csv")
        # train test split
        X = data.drop("Outcome", axis=1)
        Y = data["Outcome"]
        X_train, X_test, Y_train, Y_test = train_test_split(X,
                                                            Y,
                                                            test_size=0.2)
        # Trainning the Model
        model = LogisticRegression()
        model.fit(X_train, Y_train)

        val1 = float(request.POST["pregnancies"])
        val2 = float(request.POST["gulcose"])
        val3 = float(request.POST["blood_pressure"])
        val4 = float(request.POST["skin_thickness"])
        val5 = float(request.POST["insuline"])
        val6 = float(request.POST["bmi"])
        val7 = float(request.POST["diabetes_pedigree"])
        val8 = float(request.POST["age"])

        pred = model.predict([[val1, val2, val3, val4, val5, val6, val7,
                               val8]])
        print(pred)

        result1 = ""
        if pred == [1]:
            result1 = "Positive"
        else:
            result1 = "Negative"

        # report = Prediction(result=result1)

        ins = Prediction(
            user=username,
            pregnancies=val1,
            gulcose=val2,
            blood_pressure=val3,
            skin_thickness=val4,
            insuline=val5,
            bmi=val6,
            diabetes_pedigree=val7,
            age=val8,
            result=result1,
        )

        if form.is_valid():
            ins.save()
            # to get user
            # profile = form.save(commit = False)
            # profile.user = request.user
            # profile.save()

            # username = form.cleaned_data.get("user")
            messages.success(
                request,
                f"{ username } : Diabetes {result1} ",
            )
        return redirect("/")

    else:
        form = DiabetesPredictForm()

    context = {
        "form": form,
    }
    return render(request, "diabetes/predict.html", context)


# predict result listing
# def report(request):
#     if request.user.is_authenticated:
#         userid = request.user.id
#     obj = Prediction.objects.filter(user=userid)
#     context = {"obj": obj}
#     return render(request, "diabetes/report.html", context)

# predict result listing for searching
from django.db.models import Q


def report(request):
    context = dict()
    if request.user.is_authenticated:
        userid = request.user.id
    #for searching
    if 'q' in request.GET:
        q = request.GET[
            'q']  # from search in report.html  search field  name="q"
        multiple_q = Q(
            Q(pregnancies__icontains=q) | Q(result__icontains=q)
            | Q(age__icontains=q))
        context["obj"] = Prediction.objects.filter(multiple_q, user=userid)
    #end searching
    else:
        context['obj'] = Prediction.objects.filter(
            user=userid)  #creating dictionary to pass all obj of Todo model
    return render(request, "diabetes/report.html", context)


#updating predict_report
def predict_update(request, id):
    context = dict()
    try:
        predict = Prediction.objects.get(id=id)
    except Prediction.DoesNotExist:
        messages.error(request, "Item doesnt exist")
        return ("/")

    if request.method == "GET":
        context["form"] = DiabetesPredictForm(instance=predict)
        return render(request, "diabetes/predict_update.html", context)

    if request.user.is_authenticated:
        username = request.user

    form = DiabetesPredictForm(request.POST)
    # loading dataset
    data = pd.read_csv("diabetes.csv")
    # train test split
    X = data.drop("Outcome", axis=1)
    Y = data["Outcome"]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    # Trainning the Model
    model = LogisticRegression()
    model.fit(X_train, Y_train)
    val1 = float(request.POST["pregnancies"])
    val2 = float(request.POST["gulcose"])
    val3 = float(request.POST["blood_pressure"])
    val4 = float(request.POST["skin_thickness"])
    val5 = float(request.POST["insuline"])
    val6 = float(request.POST["bmi"])
    val7 = float(request.POST["diabetes_pedigree"])
    val8 = float(request.POST["age"])

    pred = model.predict([[val1, val2, val3, val4, val5, val6, val7, val8]])
    print(pred)
    result1 = ""
    if pred == [1]:
        result1 = "Positive"
    else:
        result1 = "Negative"

    if form.is_valid():
        predict.user = username
        predict.pregnancies = form.cleaned_data.get('pregnancies')
        predict.gulcose = form.cleaned_data.get('gulcose')
        predict.blood_pressure = form.cleaned_data.get('blood_pressure')
        predict.skin_thickness = form.cleaned_data.get('skin_thickness')
        predict.insuline = form.cleaned_data.get('insuline')
        predict.bmi = form.cleaned_data.get('bmi')
        predict.diabetes_pedigree = form.cleaned_data.get('diabetes_pedigree')
        predict.age = form.cleaned_data.get('age')
        predict.result = result1
        predict.save()
        messages.success(
            request,
            f"{ username } : Diabetes {result1} ",
        )
        return redirect('/')
    context['form'] = form
    return render(request, "diabetes/predict_update.html", context)


def predict_delete(request, id):
    context = ()
    try:
        predict = Prediction.objects.get(id=id)
        predict.delete()
        messages.success(request, "Prediction Report Deleted!!!")
    except predict.DoesNotExist:
        messages.danger(request, "Prediction Doesn't Exists ")

    return redirect("/")
