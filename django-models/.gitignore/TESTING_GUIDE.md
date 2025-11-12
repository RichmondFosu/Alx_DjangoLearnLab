# Quick Reference: Custom Permissions Testing Guide

## Project Structure Overview

```
LibraryProject/
├── manage.py
├── db.sqlite3
└── relationship_app/
    ├── models.py           (Book model with Meta permissions)
    ├── views.py            (add_book, edit_book, delete_book views)
    ├── urls.py             (Permission-based URL patterns)
    ├── forms.py
    ├── admin.py
    └── templates/relationship_app/
        ├── base.html                (Master layout)
        ├── list_books.html          (Book list with permission checks)
        ├── add_book.html            (Add book form)
        ├── edit_book.html           (Edit book form)
        ├── delete_book.html         (Delete confirmation)
        ├── login.html
        ├── register.html
        ├── admin_view.html
        ├── librarian_view.html
        └── member_view.html
```

---

## Key Components

### 1. Book Model Permissions
**In models.py:**
```python
class Meta:
    permissions = (
        ('can_add_book', 'Can add book'),
        ('can_change_book', 'Can change book'),
        ('can_delete_book', 'Can delete book'),
    )
```

### 2. Permission-Enforced Views

| View | Decorator | Permission | URL |
|------|-----------|-----------|-----|
| `add_book` | `@permission_required('relationship_app.can_add_book')` | can_add_book | `/books/add/` |
| `edit_book` | `@permission_required('relationship_app.can_change_book')` | can_change_book | `/books/<id>/edit/` |
| `delete_book` | `@permission_required('relationship_app.can_delete_book')` | can_delete_book | `/books/<id>/delete/` |

### 3. URL Patterns
```python
path('books/add/', add_book, name='add-book'),
path('books/<int:book_id>/edit/', edit_book, name='edit-book'),
path('books/<int:book_id>/delete/', delete_book, name='delete-book'),
```

### 4. Template Permission Checking
```django
{% if perms.relationship_app.can_add_book %}
    <!-- Show "Add Book" button -->
{% endif %}

{% if perms.relationship_app.can_change_book %}
    <!-- Show "Edit" button -->
{% endif %}

{% if perms.relationship_app.can_delete_book %}
    <!-- Show "Delete" button -->
{% endif %}
```

---

## Testing Workflow

### Step 1: Start the Development Server
```bash
python manage.py runserver
```
Navigate to: `http://localhost:8000/`

### Step 2: Create Test Users in Django Admin

1. Go to `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Click **Users** under **Authentication and Authorization**

#### Create User 1: Full Permission User (Admin/Librarian)
- Username: `admin_user`
- Password: `TestPass123!`
- Permissions: Check all three:
  - ☑ relationship_app | book | Can add book
  - ☑ relationship_app | book | Can change book
  - ☑ relationship_app | book | Can delete book

#### Create User 2: Limited Permission User (Librarian)
- Username: `librarian_user`
- Password: `TestPass123!`
- Permissions: Check only:
  - ☑ relationship_app | book | Can add book
  - ☑ relationship_app | book | Can change book

#### Create User 3: No Permission User (Member)
- Username: `member_user`
- Password: `TestPass123!`
- Permissions: (Leave all unchecked)

### Step 3: Test Adding Books

#### Test 3.1: User WITH `can_add_book` Permission
1. Logout and login as `admin_user` or `librarian_user`
2. Navigate to book list: `http://localhost:8000/relationship_app/books/`
3. Verify: Green "Add New Book" button is visible ✅
4. Click the button
5. Should see form with:
   - Title field
   - Author dropdown
   - ISBN field
6. Fill in details and submit
7. Book should be created ✅

#### Test 3.2: User WITHOUT `can_add_book` Permission
1. Logout and login as `member_user`
2. Navigate to book list
3. Verify: "Add New Book" button is NOT visible ✅
4. Try to access directly: `http://localhost:8000/relationship_app/books/add/`
5. Should see: **403 Forbidden** error ✅

### Step 4: Test Editing Books

#### Test 4.1: User WITH `can_change_book` Permission
1. Logout and login as `admin_user` or `librarian_user`
2. Navigate to book list
3. Click "Edit" button on any book
4. Should see pre-filled form ✅
5. Modify a field and submit
6. Book should be updated ✅

#### Test 4.2: User WITHOUT `can_change_book` Permission
1. Logout and login as `member_user`
2. Navigate to book list
3. Verify: "Edit" button is NOT visible on books ✅
4. Try to access directly: `http://localhost:8000/relationship_app/books/1/edit/`
5. Should see: **403 Forbidden** error ✅

### Step 5: Test Deleting Books

#### Test 5.1: User WITH `can_delete_book` Permission
1. Logout and login as `admin_user`
2. Navigate to book list
3. Click "Delete" button on any book
4. Should see confirmation page with book details ✅
5. Click "Yes, Delete This Book"
6. Book should be deleted and redirect to list ✅

#### Test 5.2: User WITHOUT `can_delete_book` Permission
1. Logout and login as `librarian_user` or `member_user`
2. Navigate to book list
3. Verify: "Delete" button is NOT visible ✅
4. Try to access directly: `http://localhost:8000/relationship_app/books/1/delete/`
5. Should see: **403 Forbidden** error ✅

### Step 6: Verify Permission Badges

1. Login as different users
2. Navigate to book list (`/relationship_app/books/`)
3. Scroll to "Your Permissions" section
4. Verify badges show correct status:
   - Green "Yes" badges for permissions user has
   - Red "No" badges for permissions user doesn't have

---

## Troubleshooting

### Issue: Templates extending base.html not rendering correctly
**Solution**: Ensure Bootstrap CSS is loaded (base.html includes CDN links)

### Issue: "No such permission" error
**Solution**: Ensure migrations were applied:
```bash
python manage.py migrate
```

### Issue: Permission checks not working
**Solution**: Verify:
1. User was assigned permission in admin
2. Permission format is correct: `relationship_app.can_add_book`
3. Clear browser cache and re-login

### Issue: Buttons not appearing based on permissions
**Solution**: Check template permission syntax:
```django
{% if perms.relationship_app.can_add_book %}
```
(Note: Use underscores in app name, not hyphens)

---

## Expected Behavior Summary

### User with ALL Permissions (admin_user)
- ✅ Can view book list
- ✅ Can see "Add New Book" button
- ✅ Can see "Edit" button on each book
- ✅ Can see "Delete" button on each book
- ✅ Permission badges show: Add=Yes, Edit=Yes, Delete=Yes

### User with SOME Permissions (librarian_user)
- ✅ Can view book list
- ✅ Can see "Add New Book" button
- ✅ Can see "Edit" button on each book
- ❌ Cannot see "Delete" button (no permission)
- ✅ Permission badges show: Add=Yes, Edit=Yes, Delete=No

### User with NO PERMISSIONS (member_user)
- ✅ Can view book list
- ❌ Cannot see "Add New Book" button
- ❌ Cannot see "Edit" or "Delete" buttons
- ❌ Permission badges show: Add=No, Edit=No, Delete=No
- ❌ Accessing secured URLs returns 403 Forbidden

---

## File Locations for Reference

- **Custom Permissions Definition**: `relationship_app/models.py` (lines with `class Meta:`)
- **Permission-Enforced Views**: `relationship_app/views.py` (search for `@permission_required`)
- **URL Patterns**: `relationship_app/urls.py` (lines with `/books/add/`, `/books/.../edit/`, `/books/.../delete/`)
- **Permission Display Templates**: 
  - `add_book.html`
  - `edit_book.html`
  - `delete_book.html`
  - `list_books.html`
- **Base Template**: `base.html` (extended by all permission templates)

---

## Management Commands

### Run server:
```bash
python manage.py runserver
```

### Create superuser (if needed):
```bash
python manage.py createsuperuser
```

### Check project status:
```bash
python manage.py check
```

### View all permissions:
```bash
python manage.py shell
>>> from django.contrib.auth.models import Permission
>>> Permission.objects.filter(content_type__app_label='relationship_app', codename__startswith='can_')
```

---

## Success Criteria ✅

All of the following should be true:

1. ✅ Book model has Meta class with three custom permissions
2. ✅ Three views decorated with `@permission_required` exist
3. ✅ Three URL patterns map to permission-enforced views
4. ✅ Templates show/hide buttons based on user permissions
5. ✅ Users without permission see 403 Forbidden
6. ✅ All tests pass as described above
7. ✅ Project validation: `python manage.py check` passes
8. ✅ Database: `python manage.py migrate` applied successfully
