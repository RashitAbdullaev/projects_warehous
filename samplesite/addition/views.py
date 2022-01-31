from django.db.models import Sum, Q
from django.shortcuts import render, redirect
from .form import *
from .models import Сategories, Material_type, Material, Coming, Rent
from django.urls import reverse_lazy, reverse
from .pylib.barcode import generate_barcode
from django.views.generic import ListView, CreateView, TemplateView, FormView
from django.forms import modelformset_factory, Textarea, TextInput, Select, RadioSelect


class Category(CreateView):
    template_name = 'addition/create_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('rent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Сategories.objects.all()
        return context


class MaterialType(CreateView):
    template_name = 'addition/create_type_material.html'
    form_class = Material_typeForm
    success_url = reverse_lazy('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material_type'] = Material_type.objects.filter(category=self.kwargs['id_category'])
        return context


class Materials(CreateView):
    template_name = 'addition/create_material.html'
    form_class = MaterialForm
    success_url = reverse_lazy('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material'] = Material.objects.filter(material_type=self.kwargs['id_material_type'])
        return context

    def form_valid(self, form):
        get_data = generate_barcode(self.kwargs['id_material_type'], self.request.POST['material_type'],
                                    self.request.POST['title_material'])
        form.instance.barcode = get_data[1]
        form.instance.ean = get_data[0]
        form.save()
        return super().form_valid(form)


class Comings(CreateView):
    template_name = 'addition/create_coming.html'
    form_class = ComingForm
    success_url = reverse_lazy('category')

    def form_valid(self, form):
        form.instance.unit_price = int(self.request.POST['general_price']) / int(self.request.POST['quantity'])
        form.save()
        return super().form_valid(form)


class Rents(CreateView):
    template_name = 'addition/rent.html'
    form_class = RentForm
    success_url = reverse_lazy('rent')
    ean_list = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def info_rents(request, worker, ):
    rent = Rent.objects.filter(worker=worker)
    Rents.ean_list.clear()
    RentFormSet = modelformset_factory(Rent, fields=('material', 'date_of_issue', 'quantity',),

                                       can_delete=True, extra=0,
                                       labels={'quantity': '', 'material': '', 'date_of_issue': ''},
                                       widgets={'material': Select(attrs=({'class': 'material ', 'disabled': True,
                                                                           'value': 'selected'})),
                                                'date_of_issue': TextInput(attrs=({'class': 'date'})),
                                                'quantity': TextInput(attrs=({'class': 'quantity'}))})
    if request.method == 'POST':
        formset = RentFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('rent')
    else:
        formset = RentFormSet(queryset=rent)
    context = {'formset': formset, 'rent': rent}
    return render(request, 'addition/info_rent.html', context)


def data_rents(request, ean, worker, ):
    material_ean = Material.objects.get(ean=ean)
    Rents.ean_list.append(material_ean)
    RentFormSet = modelformset_factory(Rent, fields=('material', 'quantity', 'in_stock'), can_delete=False,
                                       extra=len(Rents.ean_list),
                                       labels={'quantity': '', 'material': '', 'in_stock': ''},
                                       widgets={'quantity': TextInput(attrs=({'class': 'rent_quantity'})),
                                                'material': Select(
                                                    attrs=({'class': 'rent_material', 'disabled': True})),
                                                'in_stock': TextInput(attrs=({'class': 'in_stock', 'disabled': True}))})
    formset = RentFormSet(request.POST)
    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                form.instance.worker = worker
                form.save()
            return redirect('rent')
    else:

        try:
            formset = RentFormSet(initial=[{'material': x, 'in_stock':
                Coming.objects.aggregate(sum=Sum('quantity', filter=Q(material=x.pk)))['sum'] -
                Rent.objects.aggregate(sum=Sum('quantity', filter=Q(material=x.pk)))['sum']}
                                           for x in Rents.ean_list],
                                  queryset=Rent.objects.filter(quantity=0))
        except TypeError:
            formset = RentFormSet(initial=[{'material': x, 'in_stock':
                Coming.objects.aggregate(sum=Sum('quantity', filter=Q(material=x.pk)))['sum'] - 0}
                                           for x in Rents.ean_list],
                                  queryset=Rent.objects.filter(quantity=0))

    context = {'material_ean': material_ean, 'formset': formset, 'worker': worker, 'ean': Rents.ean_list}
    return render(request, 'addition/get_rent.html', context)
