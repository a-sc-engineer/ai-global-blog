---
title: AI Global Blog
emoji: 🌍
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# AI-Powered Global Blog System

🚀 **[Live Demo → adrija-sc-ai-global-blog.hf.space](https://adrija-sc-ai-global-blog.hf.space)**

A fully functional Django blog system integrated with the `restcountries.com` API and Hugging Face Inference API for powerful AI features.

## Features
- **Global Explorer Blog**: Write articles and tag them with a focus country.
- **restcountries API**: Automatically fetches and displays the country's flag, capital, population, and region on the post page.
- **Smart AI Cover Image Generator**: Automatically generates a highly accurate cover image by pulling context from Wikipedia and passing it to Hugging Face.
- **AI Sentiment Comment Labeler**: Automatically analyzes all comments using Hugging Face's Sentiment Analysis model and labels them as Positive 😊, Neutral 😐, or Negative 😠.
- **Core Blog Features**: Search, filtering, user authentication, likes, and comments.

## Setup Instructions

### 1. Prerequisites
Ensure you have Python installed on your system.

### 2. Clone and Setup Environment
```bash
git clone <your-repo-url>
cd django_blog_project
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup API Keys
Create a `.env` file in the root of the project and add your Hugging Face API Token:
```env
HUGGINGFACE_API_KEY=your_hugging_face_token_here
```
*(You can get a free token by creating an account at huggingface.co)*

### 5. Run Migrations and Start Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser!
