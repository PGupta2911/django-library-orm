from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from library.models import Book

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
    # 👉 THIS MUST RENDER HTML
    return render(request, "blog/article_add.html")


@login_required
def add_article(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        content = request.POST.get("content")  # ✅ NEW

        if not title or not author or not content:
            return render(request, "blog/article_add.html", {
                "error": "All fields are required"
            })

        Article.objects.create(
            title=title,
            author=author,
            content=content,   # ✅ SAVE CONTENT
            created_by=request.user
        )

        return redirect("blog:manage_blog")

    return redirect("blog:add_article_page")



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