"# Blog-Django" 
# 📝 Django Blog API with JWT Auth

A simple blogging platform built using Django REST Framework and JWT authentication, where users can:

- Create posts
- List all posts (with pagination)
- Comment on other users' posts
- Retrieve a post with its comments
- Only authors can delete their posts

---

## 🚀 Features

- JWT Authentication (SimpleJWT)
- Pagination for posts and comments
- Only post authors can delete their posts
- Custom ViewSet for managing blogs & comments

---

## 📦 Requirements

- Python 3.8+
- Django 4.x
- Django REST Framework
- SimpleJWT

---

## 🔧 Installation

```bash
git clone https://github.com/yourusername/blog-api.git
cd blog-api
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
