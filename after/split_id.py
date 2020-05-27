import pymysql

db = pymysql.connect("localhost","root","hh0326lpj","after" )
cursor = db.cursor()

sql='select course_id from course_information'
cursor.execute(sql)
data=cursor.fetchall()

# ~ for row in data:
	# ~ print(row)

# ~ split=[]
# ~ for row in data:
	# ~ course_id=row[0]
	# ~ print(course_id)
	# ~ i=len(course_id)-1
	# ~ find=False
	# ~ while True:
		# ~ if course_id[i]=='+':
			# ~ find=True
			# ~ break
		# ~ i=i-1
		# ~ if i==0:
			# ~ break
	
	# ~ if find:
		# ~ course=course_id[:i]
		# ~ term=course_id[i+1:]
	# ~ else:
		# ~ course=course_id
		# ~ term=''
	
	# ~ split.append([course_id,course,term])


# ~ for row in split:
	# ~ print(row)
	# ~ sql='insert into course_split (course_term_id,course_id,term_id) values(\"'+row[0]+'\",\"'+row[1]+'\",\"'+row[2]+'\")'
	# ~ print(sql)
	# ~ db = pymysql.connect("localhost","root","hh0326lpj","after" )
	# ~ cursor = db.cursor()
	# ~ cursor.execute(sql)
	# ~ db.commit()
	
sql='select distinct course_id from ci'
cursor.execute(sql)
data=cursor.fetchall()
course=[]
for row in data:
	course.append(row[0])

for row in course:
	print(row)

ci=[]
for row in course:
	sql='select course_id,course_name,course_type,team,org_eng,org_chi from ci where course_id=\"'+row+'\"'
	cursor.execute(sql)
	data=cursor.fetchall()
	ci.append(data[0])

for row in ci:
	print(row)
	
	sql='insert into course values(\"'+row[0]+'\",\"'+row[1]+'\",\"'+row[2]+'\",\"'+row[3]+'\",\"'+row[4]+'\",\"'+row[5]+'\")'
	print(sql)
	db = pymysql.connect("localhost","root","hh0326lpj","after" )
	cursor = db.cursor()
	cursor.execute(sql)
	db.commit()

print(len(ci))
