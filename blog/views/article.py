from flask import Blueprint, current_app, render_template, flash, redirect, abort, request
from ..utils.decorators import authenticate
from ..config.database import get_connection
from ..store.category import get_all_categories, get_one_category
from ..store.article import get_all_articles, get_one_article
from werkzeug.utils import secure_filename
from datetime import datetime
from ..utils.helper import sub_words
import os

article = Blueprint("article", __name__)
db = get_connection()

# @article.get("/")
# @authenticate
# def article_view_page():
#   if not db:
#     return abort(500, "Error connecting to db")
#   _, cursor = db
#   articles = get_all_articles(cursor, True)
#   return render_template("admin/view-article.html", articles=articles, sub_words=sub_words) 

@article.get("/view")
@authenticate
def articles_page():
  if not db:
    return abort(500, "Error connecting to db")
  
  conn, cursor = db
  # articles = get_all_articles_alt(cursor)
  articles = get_all_articles(cursor)
  
  return render_template("admin/view-article.html", articles=articles, sub_words=sub_words)

@article.get("/add")
@authenticate
def article_add_page():
  if not db:
    return abort(500, "Error connecting to db")
  _, cursor = db
  categories = get_all_categories(cursor)
  return render_template("admin/add-article.html", categories=categories) 


@article.post("/create")
@authenticate
def create_article():
  form = request.form
  image = request.files.get("image")

  allowed_types = ["image/png", "image/jpeg", "image/jpg"]

  if not image.mimetype in allowed_types:
    flash("File (type) not allowed", "danger")
    return redirect("/owner/article/add")
  # GET UPLOADED FILENAME
  filename = str(datetime.now().timestamp()) + "-" + secure_filename(image.filename)
  image.save(os.path.join(current_app.config["BLOG_UPLOAD_PATH"], filename))

  # GET FORM FIELDS
  title = form.get("title")
  content = form.get("content")
  author = form.get("author")
  category = form.get("category")

  if not db:
    flash("Error connecting to db", "danger")
    return redirect("/owner/article/add")
  
  conn, cursor = db

  query = "INSERT INTO article(title, image, content, author, category) VALUES (%s, %s, %s, %s, %s)"
  cursor.execute(query, [title, filename, content, author, category])
  conn.commit()

  if not cursor.rowcount: 
    flash("Failed to add article!", "danger")
    return redirect("/owner/article/add")
  
  flash("Article added successfully!", "success")
  return redirect("/owner/article/")

@article.get("/edit/<id>")
@authenticate
def edit_article_page(id):
  if not db:
    return abort(500, "Error connecting to db")
  
  conn, cursor = db
  categories = get_all_categories(cursor)
  article = get_one_article(cursor, id)
  
  return render_template("admin/edit-article.html", categories=categories, article=article)


# HANDLE DELETE ARTICLE PAGE
@article.get("/delete/<id>")
@authenticate
def delete_article(id):
  if not db:
    return abort(500, "Error connecting to db")
  
  conn, cursor = db
  query = "DELETE FROM article WHERE id = %s"
  cursor.execute(query, [id])
  conn.commit()


  if not cursor.rowcount: 
    flash("Failed to delete article!", "danger")
    return redirect("/owner/article/")
  
  flash("Article deleted!", "success")
  return redirect("/owner/article/")

@article.post("/update")
@authenticate
def update_article():
  form = request.form
  image = request.files.get("image")
  image_name = form.get("prev-image")

  if secure_filename(image.filename):
    data = article_file_upload(image)
    image_name = data.get("filename")

    # DELETE PREV IMAGE
    prev_image_path = os.path.join(current_app.config['BLOG_UPLOAD_PATH'], form.get("prev-image")) # GET THE FILE PATH
    if os.path.exists(prev_image_path): # CHECK IF FILE EXISTS
      os.remove(prev_image_path) # DELETE FILE
    

  # GET FORM VALUES
  title = form.get("title")
  category = form.get("category")
  author = form.get("author")
  content = form.get("content")
  article_id = form.get("id")

  # CHECK CONNECTION
  if not db:
    return abort(500, "Error connecting to db")
  
  conn, cursor = db

  # UPDATE TABLE
  query = """
    UPDATE article 
    SET title = %s, 
      image = %s, 
      category = %s, 
      content = %s, 
      author = %s 
    WHERE id = %s
  """
  cursor.execute(query, [title, image_name, category, content, author, article_id])
  conn.commit()

  # CHECK IF INSERTED
  if not cursor.rowcount: 
    flash("Failed to update article", "danger")
    return redirect(f"/owner/article/edit/{article_id}")
  
  flash("Article updated!", "success")
  return redirect("/owner/article/view")
