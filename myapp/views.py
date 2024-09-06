from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import Category, News
from .forms import CategoryForm, NewsForm


class HomeView(View):
    def get(self, request):
        categories = Category.objects.all()
        category_id = request.GET.get('category')

        category_form = CategoryForm(request.POST)
        if category_id:
            try:
                news = News.objects.filter(category_id=category_id)
                ct = Category.objects.get(pk=category_id)
            except:
                messages.error(request, 'Kategoriya mavjud emas!')
                return redirect('home')
        else:
            news = News.objects.all()
            ct = None
        context = {
            'title': "Bosh sahifa",
            'categories': categories,
            'news': news,
            'ct': ct,
            'category_form': category_form,
        }
        return render(request, 'home.html', context)


class CreateCategoryView(View):
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.create()
            messages.success(request, "Kategoriya qo'shildi!")
        else:
            messages.error(request, "Ma'lumotlar noto'g'ri kiritildi!")

        return redirect('home')

    def get(self, request):
        return redirect('home')


class UpdateCategoryView(View):
    def post(self, request, id):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = Category.objects.get(pk=id)
            form.update(category=category)
            messages.success(request, "Kategoriya yangilandi!")
        else:
            messages.error(request, "Ma'lumotlar noto'g'ri kiritildi!")

        return redirect('home')

    def get(self, request, id):
        return redirect('home')


class DeleteCategoryView(View):
    def get(self, request, id):
        try:
            Category.objects.get(id=id).delete()
            messages.warning(request, "Kategoriya o'chirildi!")
        except:
            messages.error(request, "Qandaydur xatolik yuz berdi!")

        return redirect('home')


class CreateNewsView(View):
    def get(self, request):
        form = NewsForm()
        return render(request, 'add_news.html', {'form': form})

    def post(self, request):
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangilik muvaffaqiyatli qo'shildi!")
            return redirect('home')
        return render(request, 'add_news.html', {'form': form})


class UpdateNewsView(View):
    def get(self, request, id):
        try:
            news = News.objects.get(id=id)
        except:
            messages.error(request, "Qandaydur xatolik yuz berdi!")
            return redirect('home')
        form = NewsForm(instance=news)
        return render(request, 'edit_news.html', {'form': form, 'news': news})

    def post(self, request, id):
        news = News.objects.get(id=id)
        form = NewsForm(request.POST, request.FILES, instance=news)

        if 'image' not in request.FILES:
            form.instance.image = news.image

        if form.is_valid():
            form.save()
            messages.success(request, "Yangilik muvaffaqiyatli tahrirlandi!")
            return redirect('news_detail', id=news.id)
        else:
            messages.error(request, "Iltimos, barcha maydonlarni to'g'ri to'ldiring!")
        return render(request, 'edit_news.html', {'form': form, 'news': news})


class DeleteNewsView(View):
    def get(self, request, id):
        try:
            News.objects.get(id=id).delete()
            messages.warning(request, "Yangilik o'chirildi!")
        except Exception as e:
            messages.error(request, f"Qandaydur xatolik yuz berdi! {e}")

        return redirect('home')


class NewsDetailView(View):
    def get(self, request, id):
        try:
            new = News.objects.get(pk=id)
            new.views += 1
            new.save()
        except:
            messages.error(request, 'Yangilik mavjud emas!')
            return redirect('home')
        context = {
            'title': new.title,
            'new': new,
        }
        return render(request, 'detail.html', context)


class AboutView(View):
    def get(self, request):
        context = {
            'title': "Biz haqimizda",
        }
        return render(request, 'about.html')


def user_login(request):
    if request.user.is_authenticated:
        messages.warning(request, "Siz tizimga allaqachon kirib bo'lgansiz")
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
            return redirect('home')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
            return redirect('login')
    else:
        return render(request, 'login.html', {'title': "Login sahifasi"})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Parollar mos kelmaydi!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bunday foydalanuvchi mavjud!")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name)
        user.email = username  # Username sifatida emailni saqlaymiz
        user.save()
        login(request, user)
        messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
        return redirect('home')
    else:
        return render(request, 'register.html', {'title': "Ro'yxatdan o'tish"})

