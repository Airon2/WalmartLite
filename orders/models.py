from django.db import models
from shopApp.models import Product
from django.core.validators import MinValueValidator

STATUS_CHOISES = [
    ('Сборка заказа','Сборка заказа'),
    ('Доставка','Доставка'),
    ('Доставлено','Доставлено'),
    ('Отменен','Отменен'),
    ('Ошибка','Ошибка'),
]

class Order(models.Model):
    products = models.ManyToManyField("OrderElement")
    timestamp = models.DateTimeField(auto_now_add=False)
    order_delivered_time = models.DateTimeField()
    order_delivered_status = models.CharField(choices = STATUS_CHOISES, default = 0)
    
    def get_total_price(self):
        total = sum([e.get_element_price() for e in self.products.all()])
        return total
    
    def __str__(self) -> str:
        return f'{self.pk} ${round(self.get_total_price(),2)}'
    
class OrderElement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    
    def get_element_price(self):
        return self.product.price*self.count
    
    def __str__(self) -> str:
        return f'{self.product.name} x{self.count} ${round(self.get_element_price(),2)}'
        