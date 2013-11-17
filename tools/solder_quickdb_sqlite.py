import sqlite3,sys,os,re,datetime,hashlib

def hashfile(filepath):
    md5 = hashlib.md5()
    f = open(filepath, 'rb')
    try:
        md5.update(f.read())
    finally:
        f.close()
    return md5.hexdigest()

dbfile = sys.argv[1]
modsfolder = sys.argv[2]
prefix = sys.argv[3]
modverRE = re.compile(r"(\w+)\-(\S+)\.zip")

dbconn = sqlite3.connect(dbfile)

modvers = []
dirs = os.listdir(modsfolder)
for dir in dirs:
   for modfile in os.listdir(os.path.join(modsfolder,dir)):
      modver_match = modverRE.match(modfile)
      if modver_match:
         print "Found mod ", modver_match.group(1),modver_match.group(2)
         hash = hashfile(os.path.join(modsfolder,dir,modfile))
         modvers.append((modver_match.group(1),modver_match.group(2),hash))
curmodvers = []
res = dbconn.execute("SELECT * from main." + prefix + "mods;")
for row in res:
   # (3, u'furnituremod', u'', u'', u'', u'2013-11-17 09:18:45', u'2013-11-17 09:18:45', u'Furniture Mod')
   (id,slug,name,author,url,ctime,mtime,desc) = row
   verres = dbconn.execute("SELECT * from main." + prefix + "modversions where id = ?;",[str(id)])
   for verrow in verres:
      (verid,modid,ver,hash,ctime,atime) = verrow
      curmodvers.append((slug,ver))

newmods = set(modvers)-set(curmodvers)

for slug,ver,hash in newmods:
   mod_id = None
   res = dbconn.execute("SELECT * from main." + prefix + "mods where name = ?;",[slug])
   for (id,name,blah2,blah3,blah4,blah5,blah6,blah7) in res:
      if slug == name:
         mod_id = id
   if not mod_id:
      print "Creating new mod ", slug
      dbconn.execute("INSERT INTO main." + prefix + "mods values (NULL,?,?,?,?,?,?,?)",[slug,slug,slug,slug,datetime.datetime.now(),datetime.datetime.now(),slug])
      res = dbconn.execute("SELECT * from main." + prefix + "mods where name = ?;",[slug])
      for (id,name,blah2,blah3,blah4,blah5,blah6,blah7) in res:
         if slug == name:
            mod_id = id
      if not mod_id:
         print "Something broke"
         sys.exit(-1)
   verrow = dbconn.execute("SELECT count(*) from main." + prefix + "modversions where mod_id = ? and version = ? and md5 = ?;",[mod_id,ver,hash])
   for (count) in verrow:
      if int(count[0]) > 0:
         print "Duplicate mod found, not inserting"
      else:
         print "Inserting new version of ", str(mod_id) 
         dbconn.execute("INSERT INTO main." + prefix + "modversions values (NULL,?,?,?,?,?);",[mod_id,ver,hash,datetime.datetime.now(),datetime.datetime.now()]) 

dbconn.commit()
dbconn.close()
