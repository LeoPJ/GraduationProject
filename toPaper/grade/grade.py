import pandas as pd
import numpy as np
import scipy

def get_total_score(df):
	question_ids = list(set(df['question_id']))

	total_score = 0
	exe_total_score = 0
	exam_total_score = 0

	for question_id in question_ids:
		ques_df = df[df['question_id']==question_id]
		score = list(ques_df['total_score'])[0]
		if score != score:
			continue
		total_score = total_score + score
		if list(ques_df['is_exam'])[0]==False:
			exe_total_score = exe_total_score + score
		else:
			exam_total_score = exam_total_score + score

	return total_score, exe_total_score, exam_total_score

def get_grade(df):
	question_ids = list(set(df['question_id']))

	total_grade = 0
	exe_grade = 0
	exam_grade = 0

	for question_id in question_ids:
		ques_df = df[df['question_id']==question_id]
		grade = list(ques_df['grade'])[0]
		if grade != grade:
			continue
		total_grade = total_grade + grade
		if list(ques_df['is_exam'])[0]==False:
			exe_grade = exe_grade + grade
		else:
			exam_grade = exam_grade + grade

	return total_grade, exe_grade, exam_grade



if __name__ == '__main__':
	grade_df = pd.read_csv("/home/cuper/python_work/GraduationProject/toPaper/grade/exercise_java.csv", low_memory=False)

	grade_df['user_id'] = grade_df['user_id'].astype('str')

	course_id = 'course-v1:TsinghuaX+00740123X+2017_T1'
	course_df = grade_df[grade_df['course_id']==course_id]
	user_ids = list(set(course_df['user_id']))
	print(len(user_ids))

	total_score, exe_total_score, exam_total_score = get_total_score(course_df)
	
	score={}
	
	i=1
	for user_id in user_ids:
		
		user_df = course_df[course_df['user_id']==user_id]
		total_grade, exe_grade, exam_grade = get_grade(user_df)

		per_grade = 0.00
		per_exe = 0.00
		per_exam = 0.00

		if total_score != 0:
			per_grade = float(total_grade)/float(total_score)
		if exe_total_score != 0:
			per_exe = float(exe_grade)/float(exe_total_score)
		if exam_total_score != 0:
			per_exam = float(exam_grade)/float(exam_total_score)
		
		print(per_grade)
		score[user_id]=per_grade*100
		
		print("第{0}个学生：id:{1},score:{2}".format(i,user_id,score[user_id]))
		
		i+=1
	
	print(score)
	print(len(score))
	data_file=open("java_score.txt",'w+') 
	print(score,file=data_file)
	

