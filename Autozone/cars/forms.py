from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from .models import CarInstance


class RegisterOldCarForm(forms.ModelForm):
    class Meta:
        model = CarInstance
        fields = ['car_model', 'car_varient', 'price', 'fuel_type', 'transmission_type', 'reg_year', 'km_driven', 'city',
                  'image', 'image1', 'image2']

    def __init__(self, *args, **kwargs):
        super(RegisterOldCarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('car_model', css_class='form-group col-md-6'),
                Column('car_varient', css_class='form-group col-md-6'),
                css_class='row mb-3'
            ),
            Row(
                Column('price', css_class='form-group col-md-4'),
                Column('km_driven', css_class='form-group col-md-4'),
                Column('reg_year', css_class='form-group col-md-4'),
                css_class='row mb-3'
            ),
            Row(
                Column('fuel_type', css_class='form-group col-md-4'),
                Column('transmission_type', css_class='form-group col-md-4'),
                Column('city', css_class='form-group col-md-4'),
                css_class='row mb-3'
            ),
            'image',
            Row(
                # Column('image', css_class='form-group col-md-4'),
                Column('image1', css_class='form-group col-md-6'),
                Column('image2', css_class='form-group col-md-6'),
                css_class='row mb-3'
            ),
            Submit('submit', 'Save')
        )
