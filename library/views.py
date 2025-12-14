from django.http import HttpResponse
from django.utils import timezone
from .models import Author, Books

def create_author(request):
    name = request.GET.get("name")
    email = request.GET.get("email")

    author = Author.objects.create(name=name, email=email)
    return HttpResponse(f"Author created: {author.name}")

def create_book(request):
    title = request.GET.get("title")
    author_id = request.GET.get("author_id")

    author = Author.objects.get(id="author_id")
    
    book = Books.objects.create(
        title=title,
        published_date=timezone.now(),
        author=author
    )

    return HttpResponse(f"Books created: {book.title}")


def get_author(request, author_id):
    author = Author.objects.get(id=author_id)
    books =author.books.all()

    output = f"<h3>Author: {author.name}</h3><br>Books:<br>"
    for book in books:
        output += f"- {book.title}<br>"
    
    return HttpResponse(output)

def get_book(request, book_id):
    book = Books.objects.get(id=book_id)
    return HttpResponse(f"title : {book.title}, Author: {book.author.name}")

def update_author(request, author_id):
    new_name= request.GET.get("name")

    author = Author.objects.get(id=author_id)
    author.name = new_name
    author.save()

    return HttpResponse("Author updated successfully")

def update_book(request,book_id):
    new_title = request.GET.get("title")

    book= Books.objects.get(id=book_id)
    book.title=new_title
    book.save()

    return HttpResponse("Book updated sucessfully")

def delete_author(request,author_id):
    Author.objects.get(id=author_id).delete()
    return HttpResponse("Author deleted")


def delete_book(request,book_id):
    Author.objects.get(id=book_id).delete()
    return HttpResponse("Book deleted")







