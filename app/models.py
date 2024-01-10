from django.db import models
from django.contrib.auth.models import User

class Foydalanuvchi(models.Model):

    ism = models.ForeignKey(User,on_delete = models.CASCADE)
    rasm = models.ImageField(upload_to='image')
    contact = models.CharField(max_length = 50)
    bio = models.CharField(max_length = 50)
    spam = models.BooleanField(default = False,null = True ,blank = True)
    stared = models.FloatField(default = 0)
    total = models.IntegerField(default = 0)

# 

    def __str__(self):
        return self.ism.username

class Mahsulot(models.Model):
    
    ega = models.ForeignKey(Foydalanuvchi,on_delete = models.CASCADE,related_name = 'ega')
    nomi = models.CharField(max_length = 30)
    rasm = models.ImageField(upload_to='image')
    info = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 14 , decimal_places = 2)
    like = models.ManyToManyField(Foydalanuvchi,null=True,blank=True,related_name='likers')
    chegirma = models.IntegerField(null =True ,blank = True)
    bonus = models.CharField(max_length = 3,null =True ,blank = True)
    vaqt = models.DateTimeField(auto_now_add = True,null =True,blank =True)
    stared = models.FloatField(default = 0)
    total = models.IntegerField(default = 0)
    saved = models.ForeignKey('Loved',on_delete =models.CASCADE,null =True,blank =True)

    class Meta :
        ordering = ['-stared','-total']

    def __str__(self):
        return self.nomi

class Ball(models.Model):
    liker = models.ForeignKey(Foydalanuvchi,on_delete = models.CASCADE,null = True,blank = True,related_name = 'like')
    user = models.ForeignKey(Foydalanuvchi,on_delete = models.CASCADE,null = True,blank = True,related_name = 'user')
    object = models.ForeignKey(Mahsulot,on_delete = models.CASCADE,null = True,blank = True)
    baho = models.IntegerField() 
    
    def __str__(self):
        return str(self.baho)
    
class Loved(models.Model):
    liker = models.ForeignKey(Foydalanuvchi,on_delete = models.CASCADE,null = True,blank = True,related_name = 'lover')
    user = models.ForeignKey(Foydalanuvchi,on_delete = models.CASCADE,null = True,blank = True,related_name = 'loved')
    object = models.ForeignKey(Mahsulot,on_delete = models.CASCADE,null = True,blank = True)

    

