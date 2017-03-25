import MySQLdb
def fun(): 
	db = MySQLdb.connect("localhost","sanyabt","12345678","lockerdb" )
	cursor = db.cursor()
	cursor.execute("update prime SET day0=day1,day1=day2")
	cursor.execute("update standard SET day0=day1,day1=day2, day2=day3, day3=day4, day4=day5")
	cursor.execute("update prime p, table1 t SET p.day2= t.prime_capacity")
	cursor.execute("update standard s, table1 t SET s.day5= t.standard_capacity")	
	db.commit()
	cursor.close()

