"""
Script to populate the database with sample data for testing
Run this script using: python manage.py shell < populate_db.py
"""

from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment
from accounts.models import UserProfile

print("Starting database population...")

# Create sample users
print("\nCreating users...")
users_data = [
    {'username': 'admin', 'email': 'admin@blog.com', 'password': 'admin123', 'role': 'admin', 'first_name': 'Admin', 'last_name': 'User'},
    {'username': 'john_author', 'email': 'john@blog.com', 'password': 'author123', 'role': 'author', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': 'jane_author', 'email': 'jane@blog.com', 'password': 'author123', 'role': 'author', 'first_name': 'Jane', 'last_name': 'Smith'},
    {'username': 'reader1', 'email': 'reader1@blog.com', 'password': 'reader123', 'role': 'reader', 'first_name': 'Bob', 'last_name': 'Reader'},
]

created_users = {}
for user_data in users_data:
    role = user_data.pop('role')
    password = user_data.pop('password')
    
    if not User.objects.filter(username=user_data['username']).exists():
        user = User.objects.create_user(**user_data)
        user.set_password(password)
        user.save()
        user.profile.role = role
        user.profile.bio = f"I'm {user_data['first_name']}, a {role} on this blog platform."
        user.profile.save()
        created_users[user_data['username']] = user
        print(f"✓ Created user: {user_data['username']} ({role})")
    else:
        created_users[user_data['username']] = User.objects.get(username=user_data['username'])
        print(f"- User already exists: {user_data['username']}")

# Create categories
print("\nCreating categories...")
categories_data = [
    {'name': 'Technology', 'description': 'Latest in technology, programming, and software development'},
    {'name': 'Lifestyle', 'description': 'Tips and insights for better living'},
    {'name': 'Travel', 'description': 'Explore the world through our travel stories'},
    {'name': 'Food', 'description': 'Delicious recipes and food reviews'},
    {'name': 'Health', 'description': 'Health and wellness tips'},
]

created_categories = {}
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
    created_categories[cat_data['name']] = category
    if created:
        print(f"✓ Created category: {cat_data['name']}")
    else:
        print(f"- Category already exists: {cat_data['name']}")

# Create tags
print("\nCreating tags...")
tags_names = ['Python', 'Django', 'Web Development', 'Tutorial', 'Tips', 'Review', 'Guide', 'News', 'Opinion', 'How-to']

created_tags = {}
for tag_name in tags_names:
    tag, created = Tag.objects.get_or_create(name=tag_name)
    created_tags[tag_name] = tag
    if created:
        print(f"✓ Created tag: {tag_name}")
    else:
        print(f"- Tag already exists: {tag_name}")

# Create sample posts
print("\nCreating posts...")
posts_data = [
    {
        'title': 'Getting Started with Django',
        'content': '<h2>Introduction to Django</h2><p>Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. In this post, we will explore the basics of Django and how to get started.</p><p>Django follows the Model-View-Template (MVT) architectural pattern and comes with many built-in features like authentication, ORM, and admin interface.</p>',
        'author': 'john_author',
        'category': 'Technology',
        'tags': ['Python', 'Django', 'Tutorial'],
        'status': 'published'
    },
    {
        'title': '10 Tips for Better Python Code',
        'content': '<h2>Write Better Python</h2><p>Python is known for its readability and simplicity. Here are 10 tips to make your Python code even better:</p><ol><li>Use list comprehensions</li><li>Follow PEP 8 style guide</li><li>Use virtual environments</li><li>Write documentation</li><li>Use type hints</li></ol>',
        'author': 'john_author',
        'category': 'Technology',
        'tags': ['Python', 'Tips', 'Guide'],
        'status': 'published'
    },
    {
        'title': 'My Journey to Becoming a Developer',
        'content': '<h2>How I Started Programming</h2><p>This is my personal story of how I transitioned from a different career into software development. It wasn\'t easy, but it was worth it.</p><p>I started learning to code through online courses and building small projects. The key was consistency and never giving up.</p>',
        'author': 'jane_author',
        'category': 'Lifestyle',
        'tags': ['Opinion', 'Guide'],
        'status': 'published'
    },
    {
        'title': 'Building a REST API with Django',
        'content': '<h2>Django REST Framework</h2><p>Learn how to build a RESTful API using Django and Django REST Framework. We will cover serializers, viewsets, and authentication.</p><p>REST APIs are essential for modern web applications and mobile app backends.</p>',
        'author': 'john_author',
        'category': 'Technology',
        'tags': ['Django', 'Web Development', 'Tutorial'],
        'status': 'published'
    },
    {
        'title': 'Healthy Living Tips',
        'content': '<h2>Stay Healthy and Active</h2><p>Health is wealth. Here are some simple tips to maintain a healthy lifestyle:</p><ul><li>Exercise regularly</li><li>Eat balanced meals</li><li>Get enough sleep</li><li>Stay hydrated</li><li>Manage stress</li></ul>',
        'author': 'jane_author',
        'category': 'Health',
        'tags': ['Tips', 'Guide'],
        'status': 'published'
    },
    {
        'title': 'Draft: Upcoming Features',
        'content': '<h2>What\'s Coming Next</h2><p>This is a draft post about upcoming features we are planning to implement.</p>',
        'author': 'john_author',
        'category': 'Technology',
        'tags': ['News'],
        'status': 'draft'
    },
]

created_posts = []
for post_data in posts_data:
    tags_list = post_data.pop('tags')
    author_username = post_data.pop('author')
    category_name = post_data.pop('category')
    
    post_data['author'] = created_users[author_username]
    post_data['category'] = created_categories[category_name]
    
    if not Post.objects.filter(title=post_data['title']).exists():
        post = Post.objects.create(**post_data)
        for tag_name in tags_list:
            post.tags.add(created_tags[tag_name])
        created_posts.append(post)
        print(f"✓ Created post: {post_data['title']}")
    else:
        print(f"- Post already exists: {post_data['title']}")

# Create sample comments
print("\nCreating comments...")
if created_posts:
    comments_data = [
        {
            'post': 0,  # Index in created_posts
            'user': 'reader1',
            'content': 'Great article! Very helpful for beginners.',
        },
        {
            'post': 0,
            'user': 'jane_author',
            'content': 'Thanks for sharing this. Django is indeed a powerful framework.',
        },
        {
            'post': 1,
            'user': 'reader1',
            'content': 'These tips are really useful. I will definitely apply them in my code.',
        },
        {
            'post': 2,
            'user': 'john_author',
            'content': 'Inspiring story! Keep up the good work.',
        },
    ]
    
    for comment_data in comments_data:
        post_index = comment_data.pop('post')
        if post_index < len(created_posts):
            user_username = comment_data.pop('user')
            comment_data['post'] = created_posts[post_index]
            comment_data['user'] = created_users[user_username]
            
            Comment.objects.get_or_create(**comment_data)
            print(f"✓ Created comment on: {comment_data['post'].title}")

print("\n" + "="*50)
print("Database population completed!")
print("="*50)
print("\nSample Accounts:")
print("-" * 50)
print("Admin: username='admin', password='admin123'")
print("Author: username='john_author', password='author123'")
print("Author: username='jane_author', password='author123'")
print("Reader: username='reader1', password='reader123'")
print("-" * 50)
