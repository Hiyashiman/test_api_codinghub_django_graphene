from django.db import models

# Create your models here.
class Product(models.Model):
    type = models.CharField(max_length=100)
    item = models.IntegerField()
    


class ProductsDetail(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    img = models.TextField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
