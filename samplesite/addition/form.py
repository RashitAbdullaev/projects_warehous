from django.forms import ModelForm
from django import forms
from .models import *


class CategoryForm(ModelForm):
    title = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'input_category'}), label='')

    class Meta:
        model = Сategories
        fields = ('title',)


class Material_typeForm(ModelForm):
    title_material_type = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'input-type_material'}),
                                          label='')
    category = forms.ModelChoiceField(queryset=Сategories.objects.all(), label='')

    class Meta:
        model = Material_type
        fields = ('title_material_type', 'category',)


class MaterialForm(ModelForm):
    Metr = 'Метр'
    Litr = 'Литр'
    Gramm = 'Грамм'
    Kg = 'Килограмм'
    Pc = 'Штука'
    Package = 'Упоковка'
    Unit_Type = [
        (Metr, 'Метр'),
        (Litr, 'Литр'),
        (Gramm, 'Грамм'),
        (Kg, 'Килограмм'),
        (Pc, 'Штука'),
        (Package, 'Упоковка')

    ]
    title_material = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'input-title_material'}),
                                     label='')
    material_type = forms.ModelChoiceField(queryset=Material_type.objects.all(), label='',)

    unit = forms.ChoiceField(choices=Unit_Type,widget=forms.widgets.Select(attrs={'class': 'input-unit'}),label='')
    class Meta:
        model = Material
        fields = ('title_material', 'unit', 'material_type',)


class ComingForm(ModelForm):
    quantity = forms.IntegerField(widget=forms.widgets.TextInput(attrs={'class': 'input-group'}),
                                  label='Количество')

    general_price = forms.IntegerField(widget=forms.widgets.TextInput(attrs={'class': 'input-group'}),
                                       label='Общая цена')

    date = forms.DateField(widget=forms.widgets.TextInput(attrs={'class': 'input-group'}),
                           label='Дата')

    class Meta:
        model = Coming
        fields = ('quantity', 'general_price', 'currency', 'date', 'warehouse', 'material')


class RentForm(ModelForm):
    class Meta:
        model = Rent
        fields = ('quantity',)
