from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from uuid import uuid4
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Company (models.Model):
    companyName = models.CharField(null= True,blank=True, max_length=200)
    companyLogo = models.ImageField(default="default_logo.jpg", upload_to='company_logos')
    address = models.CharField(null= True,blank=True, max_length=200)
    phoneNum = models.CharField(null= True,blank=True, max_length=100)
    postalCode = models.CharField(null= True,blank=True, max_length=10)
    emailAddress = models.CharField(null= True,blank=True, max_length=100)

    uniqueId = models.CharField(null= True,blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    dateCreated = models.DateTimeField(default=timezone.now,blank=True, null=True)
    lastUpdate = models.DateTimeField(default=timezone.now,blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.companyName, self.uniqueId)
    
    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.dateCreated is None:
            self.dateCreated = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.companyName, self.uniqueId)) 
        
        self.slug = slugify('{} {}'.format(self.companyName, self.uniqueId))
        self.lastUpdate = timezone.localtime(timezone.now())

        super(Company, self).save(*args, **kwargs)

class Invoice(models.Model):
    TERMS = [
        ('14 days', '14 Days'),
        ('30 days', '30 Days'),
        ('60 days', '60 Days'),
    ]

    STATUS = [
        ('CURRENT', 'CURRENT'),
        ('OVERDUE', 'OVERDUE'),
        ('PAID', 'PAID'),
    ]

    tittle = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=100)
    dueDate = models.DateField(null=True, blank=True)
    paymentTerms = models.CharField(choices=TERMS, default='14 days', max_length=100)
    status = models.CharField(choices=STATUS, default='CURRENT', max_length=100)
    notes = models.TextField(null=True, blank=True)

    #relationship 
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.SET_NULL)

    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    dateCreated = models.DateTimeField(default=timezone.now,blank=True, null=True)
    lastUpdate = models.DateTimeField(default=timezone.now,blank=True, null=True)

    def __str__(self) -> str:
        return slugify('{} {}'.format(self.number, self.uniqueId))

    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.dateCreated is None:
            self.dateCreated = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.number, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.number, self.uniqueId))
        self.lastUpdate = timezone.localtime(timezone.now())

        super(Invoice, self).save(*args, **kwargs)

class Product(models.Model):
    CURRENCY = [
    ('Rp', 'Rupiah'),
    ('$', 'USD'),
    ]
    tittle = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    currency = models.CharField(choices=CURRENCY, default='R', max_length=100)

    invoice = models.ForeignKey(Invoice, blank=True, null=True, on_delete=models.CASCADE)
    
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    dateCreated = models.DateTimeField(default=timezone.now,blank=True, null=True)
    lastUpdate = models.DateTimeField(default=timezone.now,blank=True, null=True)

    def __str__(self) -> str:
        return slugify('{} {}'.format(self.tittle, self.uniqueId))

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.dateCreated is None:
            self.dateCreated = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.tittle, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.tittle, self.uniqueId))
        self.lastUpdate = timezone.localtime(timezone.now())

        super(Product, self).save(*args, **kwargs)

class Settings(models.Model):
    companyName = models.CharField(null= True,blank=True, max_length=200)
    companyLogo = models.ImageField(default="default_logo.jpg", upload_to='company_logos')
    address = models.CharField(null= True,blank=True, max_length=200)
    phoneNum = models.CharField(null= True,blank=True, max_length=100)
    postalCode = models.CharField(null= True,blank=True, max_length=10)
    emailAddress = models.CharField(null= True,blank=True, max_length=100)

    uniqueId = models.CharField(null= True,blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    dateCreated = models.DateTimeField(default=timezone.now,blank=True, null=True)
    lastUpdate = models.DateTimeField(default=timezone.now,blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.companyName, self.uniqueId)
    
    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.dateCreated is None:
            self.dateCreated = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.companyName, self.uniqueId)) 
        
        self.slug = slugify('{} {}'.format(self.companyName, self.uniqueId))
        self.lastUpdate = timezone.localtime(timezone.now())

        super(Settings, self).save(*args, **kwargs)