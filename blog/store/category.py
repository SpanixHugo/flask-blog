def get_all_categories(cursor, descending=False):
  query = "SELECT * FROM category"
  if descending: query = "SELECT * FROM category ORDER BY id DESC"
  cursor.execute(query)
  return cursor.fetchall()
  

def get_one_category(cursor, id):
  query = "SELECT * FROM category WHERE id = %s"
  cursor.execute(query, [id])
  return cursor.fetchone()
  
