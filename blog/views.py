from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from blog.utils.email import send_article_added_email, send_book_added_email
from library.models import Author, Book

from .models import Article


@login_required
def manage_blog(request):
    books = Book.objects.all()
    articles = Article.objects.all()
    return render(request, "blog/manage.html", {
        "books": books,
        "articles": articles
    })

@login_required
def add_article_page(request):
    return render(request, "blog/article_add.html")


@login_required
def add_article(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            return render(request, "blog/article_add.html", {
                "error": "All fields are required"
            })

        article = Article.objects.create(
            title=title,
            author=request.user.get_full_name() or request.user.username,
            content=content,
            created_by=request.user
        )

        # 🔥 EMAIL CALL (MANDATORY)
        send_article_added_email(request.user, article)

        return redirect("blog:manage_blog")

    return render(request, "blog/article_add.html")


@login_required
@csrf_exempt
def delete_article(request, id):
    if request.method == "POST":
        Article.objects.filter(id=id).delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=405)


@login_required
@csrf_exempt
def delete_book(request, book_id):
    if request.method == "POST":
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return JsonResponse({"success": True})
        except Book.DoesNotExist:
            return JsonResponse({"success": False}, status=404)
    return JsonResponse({"success": False}, status=405)

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, "blog/article_detail.html", {
        "article": article
    })

@login_required
def add_article_ajax(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            return JsonResponse({
                "success": False,
                "error": "Title and content are required"
            }, status=400)

        article = Article.objects.create(
            title=title,
            author=request.user.get_full_name() or request.user.username,
            content=content,
            created_by=request.user
        )

        # 🔥 SAME EMAIL LOGIC
        send_article_added_email(request.user, article)

        return JsonResponse({
            "success": True,
            "article": {
                "title": article.title,
                "author": article.author,
            }
        })


def add_book_ajax(request):
    try:
        title = request.POST.get("title")
        description = request.POST.get("description", "")
        image = request.FILES.get("image")

        if not title:
            return JsonResponse({
                "success": False,
                "error": "Title is required"
            })

        # ✅ AUTHOR INSTANCE (VERY IMPORTANT)
        author, _ = Author.objects.get_or_create(
            user=request.user
        )

        # ✅ BOOK CREATE
        book = Book.objects.create(
            title=title,
            description=description,
            author=author,
            cover_image=image
        )

        # 🔥🔥🔥 EMAIL CALL EXACT YAHAN 🔥🔥🔥
        send_book_added_email(request.user, book)

        return JsonResponse({"success": True})

    except Exception as e:
        print("ADD BOOK ERROR:", e)
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)
    


    

