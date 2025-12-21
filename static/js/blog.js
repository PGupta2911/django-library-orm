// ================= BOOKS =================

window.addBook = function () {
  window.location.href = "/books/add/";
};

window.deleteBook = function (bookId) {
  if (!confirm("Delete this book?")) return;

  fetch(`/blog/books/delete/${bookId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(),
    },
  })
    .then((res) => {
      if (!res.ok) throw new Error("Delete failed");
      return res.json();
    })
    .then((data) => {
      if (data.success) {
        document.getElementById(`book-${bookId}`).remove();
      } else {
        alert("Book delete failed");
      }
    })
    .catch((err) => console.error(err));
};

// ================= ARTICLES =================

window.addArticle = function () {
  window.location.href = "/blog/add-article/";
};

window.deleteArticle = function (articleId) {
  if (!confirm("Delete this article?")) return;

  fetch(`/blog/delete-article/${articleId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(),
    },
  })
    .then((res) => {
      if (!res.ok) throw new Error("Delete failed");
      return res.json();
    })
    .then((data) => {
      if (data.success) {
        document.getElementById(`article-${articleId}`).remove();
      }
    })
    .catch((err) => console.error(err));
};

// ================= CSRF =================

function getCSRFToken() {
  return document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
}
