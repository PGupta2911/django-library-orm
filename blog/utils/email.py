import threading

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# ================= ARTICLE EMAIL =================
def send_article_added_email(user, article):
    def _send_email():
        subject = "✅ Article Added Successfully"
        from_email = settings.EMAIL_HOST_USER
        to = [user.email]

        html_content = render_to_string(
            "email/article_added.html",
            {
                "user": user,
                "article": article
            }
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=from_email,
            to=to
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

    threading.Thread(target=_send_email).start()


# ================= BOOK EMAIL =================
def send_book_added_email(user, book):
    def _send():
        print("📩 Book email thread started for:", book.title)

        subject = "📚 Book Added Successfully"
        from_email = settings.EMAIL_HOST_USER
        to = [user.email]

        html_content = render_to_string(
            "email/book_added.html",
            {
                "user": user,
                "book": book,
            },
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=from_email,
            to=to,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

    threading.Thread(target=_send).start()