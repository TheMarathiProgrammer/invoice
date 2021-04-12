from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .utils import render_to_pdf
from django.template.loader import get_template
import time
# Create your views here.
def store(request):
	products = Product.objects.all()
	user_id = request.user.id
	if request.user.is_authenticated:
		
		order,created = Order.objects.get_or_create(user=request.user,complete=False)
		cartItems = order.get_cart_items
	else:
		cartItems=[]
	context = {"products":products,'cartItems':cartItems,'user_id':user_id}
	template = 'store.html'
	return render(request,template,context)

def cart(request):
	if request.user.is_authenticated:
		user_id = request.user.id
		order,created = Order.objects.get_or_create(user=request.user,complete=False)
		items = order.orderitems_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
	context = {'items':items,'order':order,'cartItems':cartItems,'user_id':user_id}
	template = 'cart.html'
	return render(request,template,context)

def checkout(request):
	if request.user.is_authenticated:
		order,created = Order.objects.get_or_create(complete=False)
		items = order.orderitems_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
	context = {'items':items,'order':order,'cartItems':cartItems}
	template='checkout.html'
	return render(request,template,context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(user=request.user,complete=False)
	orderItem, created = OrderItems.objects.get_or_create(product=product,order=order)
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()
	print('Id:',productId)
	print('action:',action)
	return JsonResponse("Item Was Added",safe=False)

def form(request):
	
	user = request.user
	if request.method=='POST':
		name= request.POST.get('name')
		price = request.POST.get('price')
		p = Product.objects.create(user=user,name=name,price=price)
		print(name,price)
		template = 'form.html'
	else:
		template = 'form.html'
	return render(request,template)

def signup(request):
	if request.method =='POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('store')
	else:
		form=UserCreationForm()
	return render(request,'registration/signup.html',{
		'form':form
		})

def bills(request):
	user = request.user.id
	orderitem = OrderItems.objects.all()
	order = Order.objects.all()
	template='bills.html'
	context = {'order':order,'user':user,'orderitem':orderitem}
	return render(request,template,context)

def get(request):
	user = request.user.id
	username = request.user
	orderitem = OrderItems.objects.all()
	order = Order.objects.all()
	total = ''
	date = time.strftime("%x")
	for i in order:
		if i.user_id == user:
			total=i.get_cart_total
	template = get_template('invoice.html')
	title = str(username)+str(date)
	# context = {'invoice_id':123,'customer_name':'Ashutosh Pawaskar','amount':1399.99}
	context = {'title':title,'username':username,'order':order,'user':user,'orderitem':orderitem,'total':total,'date':date}
	html = template.render(context)
	pdf = render_to_pdf('invoice.html',context)
	if pdf:
		print('true')
		orders = Order.objects.filter(user=username)
		for i in orders:
			if i.complete == False:
				i.complete = True
				i.save()
			print(i)
	return HttpResponse(pdf,content_type='application/pdf')

# def get(self, request, *args, **kwargs):
# 	template = get_template('invoice.html')
# 	context = {
# 	"invoice_id": 123,
# 	"customer_name": "John Cooper",
# 	"amount": 1399.99,
# 	"today": "Today",
# 	}
# 	html = template.render(context)
# 	pdf = render_to_pdf('invoice.html', context)
# 	if pdf:
# 		response = HttpResponse(pdf, content_type='application/pdf')
# 		filename = "Invoice_%s.pdf" %("12341231")
# 		content = "inline; filename='%s'" %(filename)
# 		download = request.GET.get("download")
# 		if download:
# 			content = "attachment; filename='%s'" %(filename)
# 			response['Content-Disposition'] = content
# 			return response
# 			return HttpResponse("Not found")