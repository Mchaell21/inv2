from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import Company, Product, Invoice, Settings
import json
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column



class DateInput(forms.DateInput):
    input_type = 'date'

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['companyName','companyLogo','address','phoneNum','postalCode','emailAddress']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['tittle','description','quantity','price', 'currency']

class InvoiceForm(forms.ModelForm):
    THE_OPTIONS = [
    ('14 days', '14 days'),
    ('30 days', '30 days'),
    ('60 days', '60 days'),
    ]
    STATUS_OPTIONS = [
    ('CURRENT', 'CURRENT'),
    ('OVERDUE', 'OVERDUE'),
    ('PAID', 'PAID'),
    ]

    title = forms.CharField(
                    required = True,
                    label='Invoice Name or Title',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Invoice Title'}),)
    paymentTerms = forms.ChoiceField(
                    choices = THE_OPTIONS,
                    required = True,
                    label='Select Payment Terms',
                    widget=forms.Select(attrs={'class': 'form-control mb-3'}),)
    status = forms.ChoiceField(
                    choices = STATUS_OPTIONS,
                    required = True,
                    label='Change Invoice Status',
                    widget=forms.Select(attrs={'class': 'form-control mb-3'}),)
    notes = forms.CharField(
                    required = True,
                    label='Enter any notes for the client',
                    widget=forms.Textarea(attrs={'class': 'form-control mb-3'}))

    dueDate = forms.DateField(
                        required = True,
                        label='Invoice Due',
                        widget=DateInput(attrs={'class': 'form-control mb-3'}),)

    dueDate = forms.DateField(
                        required= True,
                        label='Invoice Due',
                        widget=DateInput(attrs={'class': 'form-control'}),
                    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6'),
                Column('dueDate', css_class='form-group col-md-6'),
                css_class='form-row'),
            Row(
                Column('paymentTerms', css_class='form-group col-md-6'),
                Column('status', css_class='form-group col-md-6'),
                css_class='form-row'),
            'notes',

            Submit('submit', ' EDIT INVOICE '))

    class Meta:
        model = Invoice
        fields = ['tittle', 'number', 'dueDate', 'paymentTerms', 'status', 'notes']

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['companyName','companyLogo','address','phoneNum','postalCode','emailAddress']

class CompanySelectForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.initial_comp= kwargs.pop('initial_company')
        self.COM_LIST = Company.objects.all()
        self.COM_CHOICES = [('-----', '--Select a Client--')]


        for company in self.COM_LIST:
            d_t = (company.uniqueId, company.companyName)
            self.COM_CHOICES.append(d_t)


        super(CompanySelectForm,self).__init__(*args,**kwargs)

        self.fields['company'] = forms.ChoiceField(
                                        label='Choose a related client',
                                        choices = self.COM_CHOICES,
                                        widget=forms.Select(attrs={'class': 'form-control mb-3'}),)

    class Meta:
        model = Invoice
        fields = ['company']


    def clean_company(self):
        c_comp = self.cleaned_data['company']
        if c_comp == '-----':
            return self.initial_comp
        else:
            return Company.objects.get(uniqueId=c_comp)