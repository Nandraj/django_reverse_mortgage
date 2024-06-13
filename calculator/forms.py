from django import forms


class ReverseMortgageForm(forms.Form):
    age = forms.IntegerField(label="Age", min_value=62)
    home_value = forms.DecimalField(label="Home Value", min_value=0, decimal_places=2)
    margin = forms.ChoiceField(
        label="Margin",
        choices=[
            (x, f"{x}%")
            for x in [
                1.500,
                1.625,
                1.750,
                1.875,
                2.000,
                2.125,
                2.250,
                2.375,
                2.500,
                2.625,
                2.750,
                2.875,
                3.000,
                3.125,
                3.250,
            ]
        ],
    )
