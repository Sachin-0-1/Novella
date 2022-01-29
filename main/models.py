from django.db import models

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=25)

    def __str__(self):
        return self.category

class Images(models.Model):
    x = models.ForeignKey(Category, on_delete=models.CASCADE)
    file = models.ImageField()

    def __str__(self):
        return self.category.category