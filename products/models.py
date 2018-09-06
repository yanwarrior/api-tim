from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    stock_minimum = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
