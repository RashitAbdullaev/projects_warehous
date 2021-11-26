from .form import *
from .models import Сategories, Material_type, Material, Coming, Rent
from django.urls import reverse_lazy
from .pylib.barcode import generate_barcode
from django.views.generic import ListView, CreateView, TemplateView


class Category(CreateView):
    template_name = 'addition/create_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category')

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
    template_name = 'addition/create_category.html'
    form_class = RentForm
    success_url = reverse_lazy('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rent'] = Rent.objects.all()
        return context


