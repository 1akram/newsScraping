import mysql.connector





 

def isExistArticle(link):
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rootpass",
  database="bladna_page"
  )
  cursor = mydb.cursor(buffered=True)
  sql = "SELECT link FROM bladna WHERE link=%s"
  val =  (link,)
  cursor.execute(sql, val)
  result=cursor.fetchone()
  if result:
    cursor.close()
    mydb.close()
    return True
  cursor.close()
  mydb.close()
  return False



def insertArticle(link,image_id,post_id):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpass",
    database="bladna_page"
  )
  cursor = mydb.cursor()
  sql = "INSERT INTO bladna (link,image_id,post_id) VALUES (%s,%s,%s)"
  val =  (link,image_id,post_id)
  cursor.execute(sql, val)
  mydb.commit()
  cursor.close()
  mydb.close()