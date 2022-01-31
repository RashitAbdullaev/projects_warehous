from django.db import models
from django.utils import timezone
from django.utils import formats


class Сategories(models.Model):
    title = models.CharField(max_length=20, verbose_name="Название категории")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"

    def __str__(self):
        return str(self.title)


class Material_type(models.Model):
    title_material_type = models.CharField(max_length=20, verbose_name='Тип материала')
    category = models.ForeignKey(Сategories, null=True, on_delete=models.CASCADE, verbose_name='Категории')

    class Meta:
        verbose_name = 'Тип материала'
        verbose_name_plural = "Типы материалов"
        ordering = ['title_material_type']

    def __str__(self):
        return str(self.title_material_type)


class Material(models.Model):
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
    title_material = models.CharField(max_length=20, verbose_name='Материал')
    unit = models.CharField(max_length=20, choices=Unit_Type, default=Metr, verbose_name='Ед измерения')
    barcode = models.ImageField(upload_to='images/', null=True,verbose_name='Штрихкод')
    ean = models.IntegerField(verbose_name='Значения штрихкода', null=True, unique=True)
    material_type = models.ForeignKey(Material_type, null=True, on_delete=models.CASCADE, verbose_name='Тип материала')

    def __str__(self):
        return str(self.title_material)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = "Материалы"


class Coming(models.Model):
    Dollar = 'Доллар'
    EUR = 'Евро'
    Rus_rub = 'Рубль(Россия)'
    Bel_rub = 'Рубль(Беларусь)'
    Currency_type = [
        (Dollar, 'Доллар'),
        (EUR, 'Евро'),
        (Rus_rub, 'Рубль(Росcия)'),
        (Bel_rub, 'Рубль(Беларусь)')
    ]

    warehouse57 = 'Скалад 57'
    warehouse50 = 'Склад 50'
    warehouse_Type = [
        (warehouse57, 'Склад 57'),
        (warehouse50, 'Склад 50')

    ]
    quantity = models.IntegerField(null=True, verbose_name='Количество')
    general_price = models.FloatField(null=True, verbose_name='Общая цена')
    unit_price = models.FloatField(null=True, blank=True, verbose_name='Цена за единицу')
    currency = models.CharField(max_length=20, choices=Currency_type, default=Dollar, verbose_name='Валюта')
    date = models.DateField(verbose_name='Дата')
    warehouse = models.CharField(max_length=25, choices=warehouse_Type, default=warehouse50, verbose_name='Склад')
    material = models.ForeignKey(Material, null=True, on_delete=models.CASCADE, verbose_name='Материал')

    class Meta:
        verbose_name = 'Приход'
        verbose_name_plural = "Приходы"


class Rent(models.Model):
    date_of_issue = models.DateTimeField(verbose_name='Дата выдачи', default=timezone.now)
    date_of_delivery = models.DateTimeField(verbose_name='Дата сдачи', null=True, blank=True)
    worker = models.CharField(max_length=25, verbose_name='Работник', null=False, blank=True)
    quantity = models.IntegerField(null=True, verbose_name='Количество', blank=True)
    in_stock = models.IntegerField(null=True, blank=True, verbose_name='в наличии')
    material = models.ForeignKey(Material, null=True, on_delete=models.CASCADE, verbose_name='материал',blank=False)

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = "Аренды"
