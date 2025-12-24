// =======================
// GLOBAL HELPERS
// =======================

function getCSRFToken() {
  const el = document.querySelector('input[name="csrfmiddlewaretoken"]');
  return el ? el.value : "";
}

function showAlert(type, title, text) {
  Swal.fire({
    icon: type, // success | error | warning | info
    title: title,
    text: text,
    confirmButtonColor: "#3085d6",
  });
}

// =======================
// OPEN MODALS
// =======================

function openArticleModal() {
  const modalEl = document.getElementById("articleModal");
  if (!modalEl) return;
  new bootstrap.Modal(modalEl).show();
}

function openBookModal() {
  const modalEl = document.getElementById("bookModal");
  if (!modalEl) return;
  new bootstrap.Modal(modalEl).show();
}

// =======================
// DELETE ARTICLE
// =======================

window.deleteArticle = function (articleId) {
  Swal.fire({
    title: "Delete article?",
    text: "This action cannot be undone",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    confirmButtonText: "Yes, delete",
  }).then((result) => {
    if (!result.isConfirmed) return;

    fetch(`/blog/delete-article/${articleId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          document.getElementById(`article-${articleId}`)?.remove();
          showAlert("success", "Deleted", "Article deleted successfully");
        } else {
          showAlert("error", "Error", data.error || "Delete failed");
        }
      })
      .catch(() => {
        showAlert("error", "Error", "Server error while deleting article");
      });
  });
};

// =======================
// DELETE BOOK
// =======================

window.deleteBook = function (bookId) {
  Swal.fire({
    title: "Delete book?",
    text: "This action cannot be undone",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    confirmButtonText: "Yes, delete",
  }).then((result) => {
    if (!result.isConfirmed) return;

    fetch(`/blog/books/delete/${bookId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          document.getElementById(`book-${bookId}`)?.remove();
          showAlert("success", "Deleted", "Book deleted successfully");
        } else {
          showAlert("error", "Error", data.error || "Delete failed");
        }
      })
      .catch(() => {
        showAlert("error", "Error", "Server error while deleting book");
      });
  });
};

// =======================
// ADD ARTICLE (AJAX)
// =======================

const articleForm = document.getElementById("articleForm");
if (articleForm && !articleForm.dataset.bound) {
  articleForm.dataset.bound = "true";

  articleForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    fetch("/blog/add-article-ajax/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          showAlert("success", "Added", "Article added successfully");
          setTimeout(() => location.reload(), 1200);
        } else {
          showAlert("error", "Error", data.error || "Failed to add article");
        }
      })
      .catch(() => {
        showAlert("error", "Error", "Server error while adding article");
      });
  });
}

// =======================
// ADD BOOK (AJAX)
// =======================

const bookForm = document.getElementById("bookForm");
if (bookForm && !bookForm.dataset.bound) {
  bookForm.dataset.bound = "true";

  bookForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    fetch("/blog/add-book-ajax/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          showAlert("success", "Added", "Book added successfully");
          setTimeout(() => location.reload(), 1200);
        } else {
          showAlert("error", "Error", data.error || "Failed to add book");
        }
      })
      .catch(() => {
        showAlert("error", "Error", "Server error while adding book");
      });
  });
}
