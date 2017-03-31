import MySQLdb
db = MySQLdb.connect("utkarsha19.mysql.pythonanywhere-services.com","utkarsha19","nathulal","utkarsha19$amazon" )
#db = MySQLdb.connect("localhost","root","","21Mar2")
cursor = db.cursor()
cursor.execute("update prime SET day0=day1,day1=day2")
cursor.execute("update standard SET day0=day1,day1=day2,day2=day3,day3=day4,day4=day5")
cursor.execute("update prime p, table1 t SET p.day2= t.prime_capacity WHERE t.locker_id=p.locker_id")
cursor.execute("update standard s, table1 t SET s.day5= t.standard_capacity WHERE t.locker_id=s.locker_id")	
db.commit()
cursor.close()

