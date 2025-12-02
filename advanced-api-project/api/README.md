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
