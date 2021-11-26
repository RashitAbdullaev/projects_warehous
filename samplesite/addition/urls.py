from django.urls import path
from .views import Category, MaterialType, Materials, Comings, Rents
urlpatterns = [
    path('', Category.as_view(), name='category'),
    path('MaterialType/<int:id_category>', MaterialType.as_view(), name='material_type'),
    path('materials/<int:id_material_type>', Materials.as_view(), name='materials'),
    path('coming/<int:id_material>', Comings.as_view(), name='coming'),
    path('rent/<int:id_material>', Rents.as_view(), name='rents'),
]
