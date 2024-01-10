from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.serializers import serialize
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache


def register_user(request):
    # formdan kelgan malumotlarni qabul qilish va ishlash
    if 'username' in request.POST and 'email' in request.POST and 'password' in request.POST and 'number' in request.POST and 'info' in request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        number = request.POST['number']
        info = request.POST['info']
        image = request.FILES['image']
        if User.objects.filter(username = username).exists() or User.objects.filter(email = email).exists():
            return redirect('register_user')
        else:
            user = User.objects.create(username = username ,email =email ,password = password)
            user.save()
            new_user = Foydalanuvchi.objects.create(ism =user , contact = number ,bio = info ,rasm = image)
            new_user.save()
            login(request,user)
            return redirect('bosh_sahifa')
    elif 'submit' in request.POST:
        user = Foydalanuvchi.objects.get(id = int(request.POST['submit']))
        fake_user = user
        user.delete()
        return render(request,'login.html',{'sign':True,'user':fake_user})


    else:
        return render(request,'login.html',{'sign':True})
        
# ro'yxattan o'tish ishlari yakunlandi


#  kirish qismi 
def kirish(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # new_user  =Foydalanuvchi.objects.get(ism =  )
            return redirect('bosh_sahifa')  # Replace 'home' with the name or URL of your home page
        else:
            return render(request, 'login.html', {'login': True})
    else:
        return render(request,'login.html',{'login':True})
    
#  kirish qismi yakunlandi
def profile(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    
    if 'user' in request.POST:
        sotuvchi = Foydalanuvchi.objects.get(id = int(request.POST['user']))
        products = Mahsulot.objects.filter(ega = sotuvchi)
        current_user = Foydalanuvchi.objects.get(ism = request.user)
        liked_objs = Loved.objects.filter(liker = current_user).count()
        return render(request,'profile.html',{'products':products,'sotuvchi':sotuvchi,'user':current_user,'count':liked_objs})
        

    else:
        current_user = Foydalanuvchi.objects.get(ism = request.user)
        liked_objs = Loved.objects.filter(liker = current_user).count()
        sotuvchi = Foydalanuvchi.objects.get(ism = request.user)
        products = Mahsulot.objects.filter(ega = sotuvchi)
        return render(request,'profile.html',{'products':products,'sotuvchi':sotuvchi,'user':current_user,'count':liked_objs})
        


def bosh_sahifa(request):

    if request.user.is_authenticated:

        sotuvchi =Foydalanuvchi.objects.get( ism = request.user )
        if request.user != AnonymousUser():
            if Foydalanuvchi.objects.filter(ism = request.user).exists():
                sotuvchi = Foydalanuvchi.objects.get(ism = request.user)
            else:
                sotuvchi = Foydalanuvchi.objects.create(ism = request.user , rasm = None , contact = request.user.email ,bio = 'None')
                sotuvchi.save()
        liked_objs = Loved.objects.filter(liker = sotuvchi).count()
        
        products = Mahsulot.objects.all()

        liked_objs = Loved.objects.filter(liker = sotuvchi).count()

        return render(request,'header.html',{'products':products,'sotuvchi':sotuvchi,'count':liked_objs})

    else:
        return render(request,'header.html',{'products':products})

@login_required
def mahsulot_kiritish(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    user = Foydalanuvchi.objects.get( ism = request.user )
    if 'nom' in request.POST and 'narx' in request.POST and 'info' in request.POST and 'chegirma' in request.POST and 'bonus' in request.POST and request.FILES:
        nom = request.POST['nom']
        narx = request.POST['narx']
        info = request.POST['info']
        chegirma = request.POST['chegirma']
        bonus = request.POST['bonus']
        image = request.FILES['image']
        new_item = Mahsulot.objects.create(ega =user ,nomi = nom , rasm = image ,info = info ,price = narx,chegirma = chegirma ,bonus =bonus)
        new_item.save()
        return redirect('mahsulot_kiritish')
    
    elif 'edit' in request.POST:
        object =Mahsulot.objects.get(id = int(request.POST['edit']))
        return render(request,'edit.html',{'object':object})
    
    elif 'delete' in request.POST:
        objects  = Mahsulot.objects.get(id = int(request.POST['delete']))
        objects.delete()
        return redirect('index')
    
    elif 'heart' in request.POST:
        object = request.POST['heart']
        the_product = Mahsulot.objects.get(id = int(object))
        if the_product.saved != None:
            delete = Loved.objects.get(liker = user ,object =the_product).delete()
            the_product.saved = None
            the_product.save()
            count_of_all_saves = Loved.objects.filter(liker = user).count()
            user.total = count_of_all_saves
            user.save()
            return HttpResponse(f"{count_of_all_saves}")
        else:
            new_loved_obj = Loved.objects.create(liker = user ,object = the_product)
            the_product.saved = new_loved_obj
            the_product.save()
            count_of_all_saves = Loved.objects.filter(liker = user).count()
            user.total = count_of_all_saves
            user.save()
            return HttpResponse(f"{count_of_all_saves}")
    else:
        return render(request,'edit.html')


# mahsulot qismi tugadi
    

# o'z galareyasini tashkil qilish
@login_required
def yoqtirganlarga_saqlash(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if request.method == 'POST' and request.META.get('HTTP_HX_REQUEST') == 'true':
        if 'love' in request.POST:
            user = Foydalanuvchi.objects.get(ism = request.user)
            object = Foydalanuvchi.objects.get(id =int(request.POST['love']))

            if Loved.objects.filter(liker = user ,user = object).exists():
                new = Loved.objects.get(liker = user ,user = object)
                new.delete()
                count = Loved.objects.filter(liker = user).count()
                user.total = count
                user.save()
                return HttpResponse(f"{count}")

                
            else:
                new = Loved.objects.create(liker = user ,user = object)
                new.save()
                count = Loved.objects.filter(liker = user).count()
                user.total = count
                user.save()
                return HttpResponse(f"{count}")
        elif 'like' in request.POST:
            
            user = Foydalanuvchi.objects.get(ism = request.user)
            liked_obj = Mahsulot.objects.get(id =int(request.POST['like']))
            if Loved.objects.filter(liker = user ,object = liked_obj).exists():
                new = Loved.objects.filter(liker = user ,object = liked_obj).all()
                new.delete()
                count = Loved.objects.filter(liker = user).count()

                user.total = count
                user.save()

                return HttpResponse(f"{count}")

            else:
                new = Loved.objects.create(liker = user ,object = liked_obj)
                new.save()
                count = Loved.objects.filter(liker = user).count()
                user.total = count
                user.save()

                return HttpResponse(f"{count}")

    elif 'like' in request.POST:
        user = Foydalanuvchi.objects.get(ism = request.user)
        liked_obj = Mahsulot.objects.get(id =int(request.POST['like']))
        if Loved.objects.filter(liker = user ,object = liked_obj).exists():
            new = Loved.objects.filter(liker = user ,object = liked_obj).all()
            new.delete()
            count = Loved.objects.filter(liker = user).count()
            user.total = count
            user.save()

            return redirect('bosh_sahifa')

        else:
            new = Loved.objects.create(liker = user ,object = liked_obj)
            new.save()
            count = Loved.objects.filter(liker = user).count()

            user.total = count
            user.save()

            return redirect('bosh_sahifa')


#  foydalanuvchini baholash
def foydalanuvchini_baholash(request):
    if not request.user.is_authenticated:
        return redirect('kirish')


    if request.method == 'POST' and request.META.get('HTTP_HX_REQUEST') == 'true':
        user = Foydalanuvchi.objects.get(ism = request.user)
        if 'a' in request.POST:
            baho = 1
            n = Foydalanuvchi.objects.get(id = int(request.POST['a']))

        elif 'b' in request.POST:
            baho = 2
            n = Foydalanuvchi.objects.get(id = int(request.POST['b']))

        elif 'c' in request.POST:
            baho = 3
            n = Foydalanuvchi.objects.get(id = int(request.POST['c']))

        elif 'd' in request.POST:
            baho = 4
            n = Foydalanuvchi.objects.get(id = int(request.POST['d']))

        elif 'e' in request.POST:
            baho = 5
            n = Foydalanuvchi.objects.get(id = int(request.POST['e']))

        if Ball.objects.filter(liker = user ,user = n).exists(): # agar avval baholangan bo'lsa
            oldingi = Ball.objects.get(liker = user ,user = n)
            oldingi.delete()

            new = Ball.objects.create(liker = user ,user = n,baho = baho )
            new.save()
            total_ball = Ball.objects.filter(user = n ).all()
            total = 0
            for ball in total_ball:
                total += ball.baho

            arifmetik = round(total / total_ball.count(),1)
            n.total = total_ball.count()
            n.stared = arifmetik
            n.save()
            return HttpResponse(f"({arifmetik}) {total_ball.count()}")
 
        else:
            new_score = Ball.objects.create(liker = user ,user = n,baho = baho)
            new_score.save()
            total_ball = Ball.objects.filter(user = n )
            total = 0
            for ball in total_ball:
                total += ball.baho

            arifmetik = round(total / total_ball.count(),1)
            n.total = total_ball.count()
            n.stared = arifmetik
            n.save()

            return HttpResponse(f"({arifmetik}) {total_ball.count()}")

# mahsulotni baholash
def mahsulotni_baholash(request):
    if not request.user.is_authenticated:
        return redirect('kirish')

    if request.method == 'POST' and request.META.get('HTTP_HX_REQUEST') == 'true':

        user = Foydalanuvchi.objects.get(ism = request.user) #liker
        if 'a' in request.POST:
            baho = 1
            n =Mahsulot.objects.get(id =int(request.POST['a'])) #mahsulot

        elif 'b' in request.POST:
            n =Mahsulot.objects.get(id =int(request.POST['b']))
            baho = 2

        elif 'c' in request.POST:
            baho = 3
            n =Mahsulot.objects.get(id =int(request.POST['c']))

        elif 'd' in request.POST:
            baho = 4
            n =Mahsulot.objects.get(id =int(request.POST['d']))
        elif 'e' in request.POST:
            baho = 5
            n =Mahsulot.objects.get(id =int(request.POST['e']))
        if Ball.objects.filter(liker = user ,object = n).exists(): # agar avval baholangan bo'lsa
            oldingi = Ball.objects.get(liker = user ,object = n)
            oldingi.delete()

            new = Ball.objects.create(liker = user ,object = n,baho = baho )
            new.save()
            total_ball = Ball.objects.filter(object = n ).all()
            total = 0
            for ball in total_ball:
                total += ball.baho

            arifmetik = round(total / total_ball.count(),1)
            n.total = total_ball.count()
            n.stared = arifmetik
            n.save()
            return HttpResponse(f"({arifmetik}) {total_ball.count()}")
 
        else:
            new_score = Ball.objects.create(liker = user ,object = n,baho = baho)
            new_score.save()
            total_ball = Ball.objects.filter(object = n )
            total = 0
            for ball in total_ball:
                total += ball.baho

            arifmetik = total / total_ball.count()
            n.total = total_ball.count()
            n.stared = arifmetik
            n.save()

            return HttpResponse(f"({arifmetik}) {total_ball.count()}")
  


# mahsulot egasi
def mahsulot_egasi(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    if request.POST:
        data = request.POST['user']
        user = Foydalanuvchi.objects.get(id = int(data))
        products = Mahsulot.objects.filter(ega = user)
        current_user = Foydalanuvchi.objects.get(ism =request.user)
        liked_objs = Loved.objects.filter(liker = current_user).count()

        return render(request,'mahsulot_egasi.html',{'sotuvchi':current_user,'products':products,'user':user,'count':liked_objs})



def saqlangan_mahsulotlar(request):
    if not request.user.is_authenticated:
        return redirect('kirish')
    user = Foydalanuvchi.objects.get(ism = request.user)
    specials = Loved.objects.filter(liker = user).all()
    return render(request,'specials.html',{'products':specials,'user':user})


def search(request,name):
    items = Mahsulot.objects.filter(Q(nomi__icontains = name)).all()
    sotuvchi = Foydalanuvchi.objects.get(ism = request.user)
    count = Loved.objects.filter(liker = sotuvchi).count()
    return render(request,'searched.html',{'products':items,'count':count,'user':sotuvchi})




