from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Product(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=100,null=True)
	price = models.FloatField()

	def __str__(self):
		return self.name
class Order(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	date_ordered = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	complete = models.BooleanField(default=False,blank=True,null=True)

	@property
	def get_cart_total(self):
		orderitems = self.orderitems_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitems_set.all()
		total = sum([item.quantity for item in orderitems])
		return total
	
class OrderItems(models.Model):
	product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
	order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
	quantity = models.IntegerField(default=0,null=True,blank=True)

	@property
	def get_total(self):
		total = self.product.price *self.quantity
		return total
	