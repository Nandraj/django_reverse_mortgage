from decimal import Decimal
from django.shortcuts import render
from .forms import ReverseMortgageForm


def calculate_principal_limit(age, home_value, margin):
    # Simplified formula
    principle_limit_factor = Decimal((100 - age) / 100)
    return round(home_value * principle_limit_factor * Decimal(1 + margin / 100))


def mortgage_calculator(request):
    result = None
    if request.method == "POST":
        form = ReverseMortgageForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data["age"]
            home_value = form.cleaned_data["home_value"]
            margin = float(form.cleaned_data["margin"])
            result = calculate_principal_limit(age, home_value, margin)
    else:
        form = ReverseMortgageForm()
    return render(
        request,
        "calculator/mortgage_calculator.html",
        {"form": form, "result": result},
    )
