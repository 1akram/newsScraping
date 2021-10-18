import mysql.connector







def insertMovie(movie):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpass",
    database="movieslox"
  )
  cursor = mydb.cursor()
  sql = "INSERT INTO movies (name,year,duration,rating,image,ageRestriction,type,description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
  val =  (movie['name'],movie['datePublished'],movie['duration'],movie['ratingValue'],movie['image'],movie['ageRestriction'],movie['type'],movie['description'])
  cursor.execute(sql, val)
  mydb.commit()
  movieId=cursor.lastrowid
  sql = "INSERT INTO resources (name,url,movie_id) VALUES (%s,%s,%s)"
  val =  ('imdb','https://www.imdb.com'+movie['imdb'],movieId)
  cursor.execute(sql, val)
  mydb.commit()
  sql = "INSERT INTO resources (name,url,movie_id) VALUES (%s,%s,%s)"
  val =  ('shahid4u',movie['shahid4u'],movieId)
  cursor.execute(sql, val)
  mydb.commit()
  for tag in movie['tags'] :
    sql = "INSERT IGNORE INTO tags(name) VALUES (%s)"
    val =  (tag,)
    cursor.execute(sql, val)
    mydb.commit()

    sql = "SELECT id FROM tags WHERE name=%s"
    val =  (tag,)
    cursor.execute(sql, val)
    tagId=cursor.fetchone()[0]
    sql = "INSERT INTO movies_tags(movie_id,tag_id) VALUES (%s,%s)"
    val =  (movieId,tagId)
    cursor.execute(sql, val)
    mydb.commit()
  for season in movie['seasons']:
    sql = "INSERT INTO seasons(number,movie_id) VALUES (%s,%s)"
    val =  (season['number'],movieId)
    cursor.execute(sql, val)
    mydb.commit()
    seasonId=cursor.lastrowid
    for episode in season['episodes']:
      sql = "INSERT INTO episodes(number,season_id) VALUES (%s,%s)"
      val =  (episode['number'],seasonId)
      cursor.execute(sql, val)
      mydb.commit()
      episodeId=cursor.lastrowid
      for server in episode['servers']:
        sql = "INSERT INTO servers(url,episode_id) VALUES (%s,%s)"
        val =  (server,episodeId)
        cursor.execute(sql, val)
        mydb.commit()
  cursor.close()
  mydb.close()




def isExistMovie(urlImdb,shahid4u):
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rootpass",
  database="movieslox"
  )
  cursor = mydb.cursor(buffered=True)
  sql = "SELECT id FROM resources WHERE url=%s OR url =%s"
  val =  (urlImdb,shahid4u)
  cursor.execute(sql, val)
  result=cursor.fetchone()
  if result:
    cursor.close()
    mydb.close()
    return True
  cursor.close()
  mydb.close()
  return False




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