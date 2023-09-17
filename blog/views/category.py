from flask import Flask,  request, Blueprint, render_template, flash, get_flashed_messages, redirect, session
from ..config.database import get_connection
from ..utils.decorators import authenticate, guest
from ..store.category import get_one_category, get_all_categories

category = Blueprint("category", __name__)

db = get_connection()

@category.get("/category")
@authenticate
def handle_category():
    # categories = []
    conn, cursor = db
    query = "SELECT * FROM category"
    cursor.execute(query)
    db_categories = cursor.fetchall()
    print("DB CATEGORIES", db_categories)
    # categories.append(query)
    # print("CATEGORIES", categories)
    editing = None

    if request.args.get("cat_id"):
        editing = get_one_category(cursor, id=request.args.get("cat_id"))

    return render_template("/admin/category.html", category=enumerate(db_categories), editing=editing)

@category.post("/handle_category")
def handle_add_category():
    form = request.form

    # FORM INPUT
    category = form.get("category")

    if not db:
        flash("ERROR CONNECTING TO DATABASE", "error")
        return redirect("/owner/category")
    
    conn, cursor = db
    query = "INSERT INTO category (name) VALUES (%s)"
    cursor.execute(query, [category])
    conn.commit()

    if not cursor.rowcount:
        flash("Failed to add to category", "danger")
        return redirect("/owner/category")
    
    flash("Added Successfully", "success")
    return redirect("/owner/category")

# @category.get("/delete_category/<name>")
# def delete_category(name):
#     if not db:
#         flash("ERROR CONNECTING TO DATABASE", "error")
#         return redirect("/owner/category")
    
#     conn, cursor = db
#     query = "DELETE FROM category WHERE name=%s"
#     cursor.execute(query, [name])
#     conn.commit()

#     query = "SELECT * FROM category"
#     cursor.execute(query)
#     db_categories = cursor.fetchall()

#     if db_categories:
#         flash("FAILED TO DELETE CATEGORY", "error")
#         return redirect("/owner/category")
    
#     flash("DELETED SUCCESSFULLY", "success")
#     return redirect("/owner/category")
@category.post("/delete_category")
def delete_category():
    form = request.form

    name = form.get("value")

    if not db:
        flash("ERROR CONNECTING TO DATABASE", "error")
        return redirect("/owner/category")
    
    conn, cursor = db
    query = "DELETE FROM category WHERE name=%s"
    cursor.execute(query, [name])
    conn.commit()

    query = "SELECT * FROM category"
    cursor.execute(query)
    db_categories = cursor.fetchall()

    if db_categories:
        flash("FAILED TO DELETE CATEGORY", "error")
        return redirect("/owner/category")
    
    flash("DELETED SUCCESSFULLY", "success")
    return redirect("/owner/category")

@category.post("/update/<id>")
@authenticate
def handle_update_category(id):
  name = request.form.get("category")
  if not db:
    flash("Error connecting to db", "danger")
    return redirect("/owner/category")
  
  conn, cursor = db
  query = "UPDATE category SET name = %s WHERE id = %s"
  cursor.execute(query, [name, id])
  conn.commit()

  if not cursor.rowcount:
    flash("Failed to update category", "danger")
    return redirect("/owner/category")
  
  flash("Category updated successfully!", "success")
  return redirect("/owner/category")
