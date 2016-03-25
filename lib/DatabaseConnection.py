import copy
import sqlite3
import zlib

class dbConnector():
  def __init__(self, db):
    self.db = db
    self.openDB()

  # Functions
  def getConnection(self):
    conn=sqlite3.connect(self.db)
    conn.execute('''CREATE TABLE IF NOT EXISTS Wiki
                   (id       INTEGER  PRIMARY KEY  AUTOINCREMENT,
                    title    TEXT     NOT NULL,
                    content  BLOB     NOT NULL     UNIQUE,
                    sha1     TEXT     NOT NULL);''')
    return (conn, conn.cursor())

  def addPage(self, page):
    curs=self.curs
    entry=copy.copy(page)
    entry['text'] = zlib.compress(page['text'].encode("utf-8"))
    curs.execute('''INSERT OR REPLACE INTO Wiki(title, content, sha1)
                    VALUES(:title,:text,:sha1)''', entry)
    self.conn.commit()

  def searchPages(self, text):
    curs=self.curs
    wh=("title LIKE ?", "%"+text+"%")
    data = self.selectAllFrom('Wiki', where=wh)
    for entry in data:
      entry['text']=zlib.decompress(entry['content']).decode('utf-8')
      entry.pop('content')
    return data

  def openDB(self):
    self.conn, self.curs = self.getConnection()
    
  def closeDB(self):
    self.conn.close()

  def selectAllFrom(self, table, where=None):
    if where: where=list(where)
    if where and type(where[0]) is str: where[0]=[where[0]]
    if where and type(where[1]) is str: where[1]=[where[1]]
    vals = where[1] if where else ()
    wh="where "+" and ".join(where[0]) if where[0] else ""
    data=list(self.curs.execute("SELECT * FROM %s %s;"%(table, wh), vals))
    dataArray=[]
    names = list(map(lambda x: x[0], self.curs.description))
    for d in data:
      j={}
      for i in range(0,len(names)):
        j[names[i].lower()]=d[i]
      dataArray.append(j)
    return dataArray
