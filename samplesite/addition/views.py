from django.db.models import Sum, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .form import *
from .models import Сategories, Material_type, Material, Coming, Rent
from django.urls import reverse_lazy, reverse
from .pylib.barcode import generate_barcode
from django.views.generic import ListView, CreateView, TemplateView, FormView
from django.forms import modelformset_factory


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Data_rents(TemplateView):
    template_name = 'addition/get_rent.html'
    context_object_name = 'material'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['material'] = Material.objects.get(ean=self.kwargs['ean'])
        # context['last_coming'] = Coming.objects.filter(material=context['material'].pk).last()
        sum_coming = Coming.objects.aggregate(quantity=Sum('quantity', filter=Q(material=context['material'].pk)))
        sum_rent = Rent.objects.aggregate(quantity=Sum('quantity', filter=Q(material=context['material'].pk)))
        context['in_stock'] = sum_coming['quantity'] - sum_rent['quantity']
        return context


# class Info_rents(TemplateView):
#     template_name = 'addition/info_rent.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         RentFormSet = modelformset_factory(Rent, fields=('worker', 'tool', 'quantity', 'date_of_issue'),
#                                            can_delete=True, extra=0, labels={'worker': '', 'tool': '', 'quantity': '',
#                                                                              'date_of_issue': ''})
#         context['formset'] = RentFormSet(queryset=Rent.objects.filter(worker=self.kwargs['worker']))
#         return context
#
#     def post(self, request):
#         if request.method == 'POST':
#             formset = self.get_context_data().RentFormSet(request.POST)
#             if formset.is_valid():
#                 formset.save()
#                 return redirect('rent')
#         else:
#             formset = self.get_context_data().RentFormSet()
#         context = {'formset': formset}
#         return render(request, 'addition/info_rent.html', context)

def info_rents(request, worker):
    rent = Rent.objects.filter(worker=worker)
    RentFormSet = modelformset_factory(Rent, form=RentForm, fields=('quantity',),
                                       can_delete=True, extra=0)
    if request.method == 'POST':
        formset = RentFormSet(request.POST )
        if formset.is_valid():
            formset.save()
            return redirect('rent')
    else:
        formset = RentFormSet(queryset=Rent.objects.filter(worker=worker))
    context = {'formset': formset, 'rent':rent}
    return render(request, 'addition/info_rent.html', context)
