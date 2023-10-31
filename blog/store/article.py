def get_all_articles(cursor, descending=False):
  query = """
    SELECT A.*, C.name as cat_name 
    FROM article as A
    INNER JOIN category as C
    ON A.category = C.id
    """
  
  if descending: query = """
    SELECT A.*, C.name as cat_name 
    FROM article as A
    INNER JOIN category as C
    ON A.category = C.id 
    ORDER BY id DESC
  """
  cursor.execute(query)
  return cursor.fetchall()

# HERE'S IS ANOTHER ALTERNATIVE, JUST INCASE THIS ONE DOESN'T WORK OUT.
def get_all_articles_alt(cursor, descending=False):
  query = "SELECT * FROM article"
  
  if descending: query = "SELECT * FROM article ORDER BY id DESC"
  cursor.execute(query)
  
  # GET ALL ARTICLES 
  articles = cursor.fetchall()

  data = []
  for article in articles:
    # GET THE CATEGORY
    category = get_one_category(cursor, article.get("category"))
    # ADD A NEW PROPERTY TO THE ARTICLE
    article['cat_name'] = category.get("name")
    data.append(article)
  
  return data




def get_one_article(cursor, id):
  query = "SELECT * FROM article WHERE id = %s"
  cursor.execute(query, [id])
  return cursor.fetchone()
  
