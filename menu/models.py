from django.db import models

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"


    def __str__(self):
        return self.name
    

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="menu_items")
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="menu_images/", blank=True, null=True) 
    quantity = models.IntegerField(default=1)
    createdAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name