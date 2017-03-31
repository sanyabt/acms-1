import MySQLdb

def fun(): 
	#db = MySQLdb.connect("localhost","sanyabt","12345678","lockerdb" )
	#db = MySQLdb.connect("utkarsha19.mysql.pythonanywhere-services.com","utkarsha19","nathulal","utkarsha19$amazon" )
	db = MySQLdb.connect("localhost","root","","21Mar2" )
	cursor = db.cursor()
	
	try:
		cursor.execute("SELECT p.locker_id, p.day2, t.locker_id, t.prime_capacity from prime as p, table1 as t WHERE t.locker_id=p.locker_id and p.day2 < t.prime_capacity")
		results_p = cursor.fetchall()
		for row in results_p:
			val = row[3]-row[1]
			try:
				sql_p = "INSERT INTO orders(locker_id, order_date, order_type, locker_used) VALUES ({},CURDATE(),{},{})".format(row[0], 1, val)
				cursor.execute(sql_p)
				db.commit()
			except:
				db.rollback()
		cursor.execute("SELECT s.locker_id, s.day5, t.locker_id, t.standard_capacity from standard as s, table1 as t WHERE t.locker_id=s.locker_id and s.day5 < t.standard_capacity")
		results_s = cursor.fetchall()
		for r in results_s:
			val = r[3]-r[1]
			try:
				sql_s = "INSERT INTO orders(locker_id, order_date, order_type, locker_used) VALUES ({},CURDATE(),{},{})".format(r[0], 2, val)
				cursor.execute(sql_s)
				db.commit()
			except:
				db.rollback()
	except:
		print ("Error: unable to fetch data")

	cursor.execute("update prime SET day0=day1,day1=day2")
	cursor.execute("update standard SET day0=day1,day1=day2, day2=day3, day3=day4, day4=day5")
	cursor.execute("update prime p, table1 t SET p.day2= t.prime_capacity WHERE t.locker_id=p.locker_id")
	cursor.execute("update standard s, table1 t SET s.day5= t.standard_capacity WHERE t.locker_id=s.locker_id")	
	db.commit()
	cursor.close()

