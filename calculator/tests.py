from django.test import TestCase, Client
from django.urls import reverse
from .forms import ReverseMortgageForm
from .views import calculate_principal_limit


class MortgageCalculatorTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_calculate_principal_limit(self):
        self.assertAlmostEqual(
            calculate_principal_limit(62, 300000, 1.500), 115710, delta=0.01
        )
        self.assertAlmostEqual(
            calculate_principal_limit(70, 300000, 2.000), 91800, delta=0.01
        )
        self.assertAlmostEqual(
            calculate_principal_limit(75, 300000, 3.000), 77250, delta=0.01
        )
        self.assertAlmostEqual(
            calculate_principal_limit(80, 300000, 3.000), 61800, delta=0.01
        )

    def test_mortgage_calculator_view_get(self):
        response = self.client.get(reverse("mortgage_calculator"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calculator/mortgage_calculator.html")
        self.assertIsInstance(response.context["form"], ReverseMortgageForm)
        self.assertContains(response, "<form")
        self.assertContains(response, "Age")
        self.assertContains(response, "Home Value")
        self.assertContains(response, "Margin")

    def test_mortgage_calculator_view_post(self):
        response = self.client.post(
            reverse("mortgage_calculator"),
            {"age": 70, "home_value": 300000, "margin": 2.000},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calculator/mortgage_calculator.html")
        self.assertContains(response, "Principal Limit: $91800")

    def test_invalid_form_submission(self):
        response = self.client.post(
            reverse("mortgage_calculator"),
            {
                "age": 61,
                "home_value": 300000,
                "margin": 2.000,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "calculator/mortgage_calculator.html")
        self.assertContains(
            response, "Ensure this value is greater than or equal to 62."
        )
        self.assertIsInstance(response.context["form"], ReverseMortgageForm)
        self.assertTrue(response.context["form"].errors)

    def test_form_creation(self):
        form_data = {"age": 70, "home_value": 300000, "margin": 2.000}
        form = ReverseMortgageForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["age"], 70)
        self.assertEqual(form.cleaned_data["home_value"], 300000)
        self.assertEqual(form.cleaned_data["margin"], "2.0")
