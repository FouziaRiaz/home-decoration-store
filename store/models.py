from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    category_name= models.CharField(max_length=200, unique=True)
    slug=models.SlugField(max_length=200, null=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name=models.CharField(max_length=200, null=True)
    slug=models.SlugField(max_length=200, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    price=models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(null=True,blank=True)
    is_available = models.BooleanField(default=True)
   
    def __str__(self):
        return self.name
#we have write the below code bcz we get an error if we dont give an image of any product for solving this error:  
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url
 
class Order(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered= models.DateTimeField(auto_now_add=True)
    complete= models.BooleanField(default=False,null=True,blank=False)
    transaction_id= models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return str(self.id)

   
    @property
    def get_cart_total(self):
        try:
            orderitems=self.orderitem_set.all()
            total =sum([item.get_total for item in orderitems])
            return total
        except TypeError:
            pass
    
        

    @property
    def get_cart_items(self):
        try:
            orderitems = self.orderitem_set.all()
            total = sum([item.quantity for item in orderitems])
            return total
        except TypeError:
            pass
    

class OrderItem(models.Model):
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True,null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity= models.IntegerField(default=0)
    date_added= models.DateTimeField(auto_now_add=True)


# for calculating total:   AttributeError
    @property
    def get_total(self):
        try:
            total= self.product.price * self.quantity
            return total
        except AttributeError:
            pass
    
 
class ShippingAddress(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, null= True,blank=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, null= True,blank=True)
    address= models.CharField(max_length=200,null=True)
    city= models.CharField(max_length=200,null=True)
    state= models.CharField(max_length=200,null=True)
    zipcode= models.CharField(max_length=200,null=True)
    date_added= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address