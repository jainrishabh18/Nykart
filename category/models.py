# 
from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    # slug is url for category
    slug = models.SlugField(max_length=100, unique=True)
    description =models.CharField(max_length=255, blank=True)
    cat_img = models.ImageField(upload_to='photos/categories',blank=True)
    
    # verbos used to eliminate django default of making every model plural by addding s to it.
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        # reverse = allows to retrieve url details from url's.py file through the name value provided there
        return reverse('products_by_category',args=[self.slug])


    def __str__(self):
        return self.category_name
