import copy
import sqlite3
import zlib

class dbConnector():
  def __init__(self, db):
    self.db = db
    self.openDB()

  # Functions
  # connection & db actions
  def getConnection(self):
    conn=sqlite3.connect(self.db)
    conn.execute('''CREATE TABLE IF NOT EXISTS Wiki
                   (id       INTEGER  PRIMARY KEY  AUTOINCREMENT,
                    title    TEXT     NOT NULL,
                    content  BLOB     NOT NULL     UNIQUE,
                    sha1     TEXT     NOT NULL);''')
    conn.execute('''CREATE TABLE IF NOT EXISTS Refs
                   (title    TEXT     PRIMARY KEY,
                    refTo    INT      NOT NULL,
                    FOREIGN KEY(refTo) REFERENCES Wiki(id));''')
    return (conn, conn.cursor())

  def openDB(self):
    self.conn, self.curs = self.getConnection()

  def closeDB(self):
    self.conn.close()

  # temp table for db creation
  def createTmpRefs(self):
    self.conn.execute('''CREATE TABLE IF NOT EXISTS TmpRefs
                        (title  TEXT  PRIMARY KEY,
                         refTo  TEXT  NOT NULL);''')

  def dropTmpRefs(self):
    self.conn.execute('DROP TABLE IF EXISTS TmpRefs')

  def addTmpRef(self, title, redirect):
    self.curs.execute('''INSERT OR REPLACE INTO TmpRefs(title, refTo)
                         VALUES(?, ?)''',(title, redirect))
    self.conn.commit()

  def getTempRefs(self):
    return self.selectAllFrom("TmpRefs")

  # adding data
  def addRef(self, title, refTo):
    self.curs.execute('''INSERT OR REPLACE INTO Refs(title, refTo)
                           SELECT ?, id
                           FROM Wiki
                           WHERE Wiki.title == ?''',(title, title))
    self.conn.commit()    

  def addPage(self, page):
    curs=self.curs
    entry=copy.copy(page)
    entry['text'] = zlib.compress(page['text'].encode("utf-8"))
    curs.execute('''INSERT OR REPLACE INTO Wiki(title, content, sha1)
                    VALUES(:title,:text,:sha1)''', entry)
    self.conn.commit()

  # query data
  def searchPages(self, text):
    curs=self.curs
    wh=("title LIKE ?", "%"+text+"%")
    data = self.selectAllFrom('Wiki', where=wh)
    for entry in data:
      entry['text']=zlib.decompress(entry['content']).decode('utf-8')
      entry.pop('content')
    return data

  def openPage(self, index):
    page=self.selectAllFrom('Wiki', where=("id = ?", index))
    if page:
      return zlib.decompress(page[0]['content']).decode('utf-8')
    else:
      return None

  def selectAllFrom(self, table, where=None):
    if where: where=list(where)
    if where and type(where[0]) is str: where[0]=[where[0]]
    if where and type(where[1]) is str: where[1]=[where[1]]
    vals = where[1] if where else ()
    wh="where "+" and ".join(where[0]) if where and where[0] else ""
    data=list(self.curs.execute("SELECT * FROM %s %s;"%(table, wh), vals))
    dataArray=[]
    names = list(map(lambda x: x[0], self.curs.description))
    for d in data:
      j={}
      for i in range(0,len(names)):
        j[names[i].lower()]=d[i]
      dataArray.append(j)
    return dataArray

