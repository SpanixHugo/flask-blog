def get_all_articles(cursor, descending=False):
  query = """SELECT * FROM article"""
  
  if descending: query = """SELECT * FROM article ORDER BY id DESC"""
  cursor.execute(query)
  return cursor.fetchall()
  

def get_one_article(cursor, id):
  query = "SELECT * FROM article WHERE id = %s"
  cursor.execute(query, [id])
  return cursor.fetchone()
  
