from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    tag = models.CharField(max_length = 50, 
                           choices = [
                                        ('tag1','tag1'),
                                        ('tag2','tag2'),
                                        ('tag3','tag3'),
                                        ('tag4','tag4'),
                                    ])
    def __str__(self):
        return self.tag

class Item(models.Model):
    SKU = models.CharField(max_length = 50)
    name = models.CharField(max_length = 100)
    description = models.TextField()
    category = models.CharField(max_length = 50, 
                                choices = [
                                    ('Bundles', 'BUN'),
                                    ('Finished Products', 'FIN'),
                                    ('Raw Materials', 'RAW'),
                                    ('Consumables', 'CNSM'),
                                    ('Medical Supplies', 'MED'),
                                    ('Stationery', 'STAT'),
                                ])
    in_stock = models.DecimalField(max_digits=10, decimal_places=2)
    available_stock = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default = True)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        # pass
        unique_together = (('SKU', 'user'),)


    def __str__(self):
        return self.name
