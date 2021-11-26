from django.forms import ModelForm
from django import forms
from .models import *


class CategoryForm(ModelForm):
    title = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'input-group'}), label='Категория')

    class Meta:
        model = Сategories
        fields = ('title',)


class Material_typeForm(ModelForm):
    title_material_type = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'input-group'}),
                                          label='Тип материала')

    class Meta:
        model = Material_type
        fields = ('title_material_type', 'category',)


class MaterialForm(ModelForm):
    title_material = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'input-group'}),
                                     label='Материал')

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
    model = Rent
    fields = ('worker', 'tool', 'date_of_issue', 'date_of_delivery',)
