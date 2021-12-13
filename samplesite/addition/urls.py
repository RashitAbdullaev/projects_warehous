from django.urls import path
from .views import Category, MaterialType, Materials, Comings, Rents, info_rents, Data_rents
urlpatterns = [
    path('', Rents.as_view(), name='rent'),
    path('info_rent/<str:worker>',  info_rents, name='info_rent'),
    path('rent/<int:ean>', Data_rents.as_view(), name='data_rent'),
    path('categories', Category.as_view(), name='category'),
    path('MaterialType/<int:id_category>', MaterialType.as_view(), name='material_type'),
    path('materials/<int:id_material_type>', Materials.as_view(), name='materials'),
    path('coming/<int:id_material>', Comings.as_view(), name='coming'),
]
