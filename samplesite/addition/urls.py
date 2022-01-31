from django.urls import path
from .views import Category, MaterialType, Materials, Comings, Rents, info_rents, data_rents
urlpatterns = [
    path('', Rents.as_view(), name='rent'),
    path('info_rent/<str:worker>',  info_rents, name='Info_rent'),
    path('data_rent/<int:ean>/<str:worker>', data_rents, name='data_rent'),
    path('categories', Category.as_view(), name='category'),
    path('MaterialType/<int:id_category>', MaterialType.as_view(), name='material_type'),
    path('materials/<int:id_material_type>', Materials.as_view(), name='materials'),
    path('coming/<int:id_material>', Comings.as_view(), name='coming'),
]
