from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import Author, Book


def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Author.objects.create(user=user)

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'auth/signup.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user_obj.username,  # IMPORTANT
                password=password
            )
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect('/login/')
    

@login_required
def dashboard(request):
    author = Author.objects.get(user=request.user)

    book_list = Book.objects.filter(author=author).order_by('-id')

    paginator = Paginator(book_list, 6)  # 6 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {
        'page_obj': page_obj
    })



@login_required
def add_book(request):
    if request.method == 'POST':
        author = Author.objects.get(user=request.user)
        Book.objects.create(
            author=author,title=request.POST['title'],
            description=request.POST['description'],
            cover_image=request.FILES['cover'],
            is_published='publish' in request.POST,
            published_date=timezone.now() if 'publish' in request.POST else None
        )
        return redirect('/dashboard/')
    return render(request, 'add_book.html')

@login_required
def book_detail(request, book_id):
    author = Author.objects.get(user=request.user)
    book = Book.objects.get(id=book_id, author=author)

    return render(request, 'book_detail.html', {'book': book})






