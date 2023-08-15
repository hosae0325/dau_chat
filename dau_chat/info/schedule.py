#!/usr/bin/python3
# -*- coding: utf-8 -*-
print("Content-type:text/html;charset=utf-8\r\n")

# text/html -> 일반 html
# application/json -> json 출력 시
#######################################################

import sys
import codecs
import cgitb
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime


sys.stdout=codecs.getwriter("utf-8") (sys.stdout.detach())
cgitb.enable()
week = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)']

#######################################################


try:
	response = requests.get('http://sosowel.donga.ac.kr/sosowel/1115/subview.do', timeout=15)
	response.encoding = None
except requests.exceptions.Timeout:
	print("Timeout Error")
else:
	html = response.text
	soup = BeautifulSoup(html, 'html.parser', from_encoding = 'cp949')

filePath = 'calender.txt'
# C:\Apache24\htdocs\DongAgpt\info\calender.txt
with open(filePath, "w+", encoding="cp949") as f: #UTF-8 #cp949

	for num in range(0, 3, 2):
		if num == 0 :
			f.write("다음은 1학기 일정입니다. \n")
		elif num == 2 :
			f.write("\n\n다음은 2학기 일정입니다. \n")
		cal_Tables = soup.find('table', attrs={'border':'1', 'cellpadding':'3', 'cellspacing':'1', 'width':'99%'})

		cal_Table = cal_Tables.find_all('table')
			
		cal_Date = cal_Table[num].find_all('p') 

		cal_Schedule = cal_Table[num+1].find_all('p') 

		cal_Schedule_count = len(cal_Schedule)
		cal_Schedule_list = []


		for i in range(cal_Schedule_count) :
			a = cal_Schedule[i].get_text(strip=True) 
			cal_Schedule_list.append(a)

		for i in range(cal_Schedule_count) :
			cal_Date_text = cal_Date[i].get_text()
			cal_Date_text = cal_Date_text.replace('.', '-')

			cal_Date_text = re.sub(r'\s+', '', cal_Date_text)

			cal_Date_text = cal_Date_text.replace('∙', '')

			if(cal_Date_text.find('~') != -1): #가공해야하는 일정이 2개
				cal_Date_text = cal_Date_text.split('~')

				cal_First = cal_Date_text[0].split('-')
				cal_First_Text = cal_First[0] + '년' + cal_First[1] + '월' + cal_First[2] + '일'

					#string -> datetime 
				cal_First_Datetime = datetime.strptime(cal_First_Text, '%Y년%m월%d일')
					#datetime -> string
				cal_First_Text = cal_First_Datetime.strftime('%Y년%m월%d일')

				cal_Week1 = cal_First_Datetime.weekday()
				cal_First_Text += week[cal_Week1]

				cal_Second = cal_Date_text[1].split('-')
				if len(cal_Second) > 3 :
					cal_Second_Text = cal_Second[0] + '년' + cal_Second[1] + '월' + cal_Second[2] + '일'

				else :
					cal_Second_Text = cal_First[0] + '년' + cal_Second[0] + '월' + cal_Second[1] + '일'

				cal_Second_Datetime = datetime.strptime(cal_Second_Text, '%Y년%m월%d일')
				cal_Second_Text = cal_Second_Datetime.strftime('%Y년%m월%d일')

				cal_Week2 = cal_Second_Datetime.weekday()
				cal_Second_Text += week[cal_Week2]

				cal_Date_Result = cal_First_Text + '부터 ' +cal_Second_Text
				
				output = cal_Date_Result + "의 일정은 " + cal_Schedule_list[i] + "입니다. \n"
				f.write(output)

				
				
					
			else :  # 가공해야하는 일정이 1개
				cal_Date_text = cal_Date_text.split('~')

				cal_First = cal_Date_text[0].split('-')
				cal_First_Text = cal_First[0] + '년' + cal_First[1] + '월' + cal_First[2] + '일'

					#string -> datetime 
				cal_First_Datetime = datetime.strptime(cal_First_Text, '%Y년%m월%d일')
					#datetime -> string
				cal_First_Text = cal_First_Datetime.strftime('%Y년%m월%d일')
					
				cal_Week1 = cal_First_Datetime.weekday()
				cal_First_Text += week[cal_Week1]
				cal_Date_Result = cal_First_Text
				
				output = cal_Date_Result + "의 일정은 " + cal_Schedule_list[i] + "입니다. \n"
				f.write(output)
