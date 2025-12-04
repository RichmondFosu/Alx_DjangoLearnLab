### API Views Overview

#### 1. BookListView (GET /books/)
- Returns list of all books.
- Allows any user.
- Supports filtering by ?year=YYYY.

#### 2. BookDetailView (GET /books/<pk>/)
- Returns a single book.

#### 3. BookCreateView (POST /books/create/)
- Requires authentication.
- Uses custom create hook.

#### 4. BookUpdateView (PUT/PATCH /books/<pk>/update/)
- Requires authentication.

#### 5. BookDeleteView (DELETE /books/<pk>/delete/)
- Requires authentication.

### Permissions
- Read-only views: Anyone
- Write actions: authenticated only



## Testing Approach

### Overview

This project provides a RESTful API for managing **Books** and **Authors**.
Comprehensive unit tests are implemented to ensure API endpoints function correctly, including:

* CRUD operations on books.
* Filtering, searching, and ordering.
* Authentication and permissions enforcement.
* Correct status codes and response data.

All tests use **Django’s built-in test framework** with **Django REST Framework’s `APITestCase`**.

---

### Test Structure

Tests are located in `api/test_views.py` under the class `BookAPITestCase`.

| Feature                       | Test Method                        | Description                                                           |
| ----------------------------- | ---------------------------------- | --------------------------------------------------------------------- |
| List Books                    | `test_list_books`                  | Verifies API returns all books (status `200 OK`).                     |
| Retrieve Book                 | `test_retrieve_book`               | Checks retrieving a single book by ID returns correct data.           |
| Create Book (Authenticated)   | `test_create_book_authenticated`   | Ensures authenticated users can create books.                         |
| Create Book (Unauthenticated) | `test_create_book_unauthenticated` | Confirms unauthenticated users cannot create books (`403 Forbidden`). |
| Update Book (Authenticated)   | `test_update_book_authenticated`   | Validates authenticated users can update books.                       |
| Update Book (Unauthenticated) | `test_update_book_unauthenticated` | Confirms unauthenticated users cannot update books (`403 Forbidden`). |
| Delete Book (Authenticated)   | `test_delete_book_authenticated`   | Checks authenticated users can delete books.                          |
| Delete Book (Unauthenticated) | `test_delete_book_unauthenticated` | Confirms unauthenticated users cannot delete books (`403 Forbidden`). |
| Filtering by Author           | `test_filter_books_by_author`      | Validates filtering by author ID returns correct results.             |
| Search Books                  | `test_search_books`                | Ensures search by book title or author name works.                    |
| Ordering Books                | `test_order_books`                 | Confirms ordering by fields like `publication_year` works correctly.  |

---

### Testing Environment

* **Database:** Temporary test database created/destroyed automatically.
* **API Client:** `APIClient` simulates HTTP requests in tests.
* **Authentication:** Test user (`username: testuser`) validates protected endpoints.

---

### Running Tests

Run the tests with:

```bash
python manage.py test api
```

Django will:

* Discover all methods starting with `test_` in `api/test_views.py`.
* Run tests in an isolated test database.
* Destroy the database after completion.

---

### Interpreting Test Results

* `.` → Test passed
* `F` → Test failed (logic or data mismatch)
* `E` → Error occurred (URL, permission, or serializer issue)

All 15 tests currently pass, confirming that:

* CRUD endpoints function as intended.
* Search, filter, and ordering are accurate.
* Permissions and authentication are enforced.

---

### Notes & Future Improvements

* Edge case tests (invalid input, large datasets, partial updates) can be added.
* CI/CD pipelines could run tests automatically on each push for continuous verification.
* Additional tests could be added for API performance and response time.

