from django.contrib import admin

from .models import *


class СategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'title')


class Material_typeAdmin(admin.ModelAdmin):
    list_display = ('title_material_type', 'category')
    search_fields = ('title_material_type', 'title_material_type')


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title_material', 'material_type')


class ComingAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'general_price', 'unit_price', 'currency', 'date', 'warehouse', 'material')


class RentAdmin(admin.ModelAdmin):
    list_display = ('date_of_issue', 'date_of_delivery', 'worker', 'tool')


admin.site.register(Сategories, СategoriesAdmin)
admin.site.register(Material_type, Material_typeAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Coming, ComingAdmin)
admin.site.register(Rent, RentAdmin)
