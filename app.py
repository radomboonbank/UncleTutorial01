from flask import Flask , request
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# รับค่าจาก User ผ่าน Line แล้วมาค้นหาข้อมูลใน Google Sheet


list_result_search = []
result_text = []
reply_msg = []

def connect_google_sheet() :
	scope = ["https://www.googleapis.com/auth/spreadsheets"]
	credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials_google_api_mobile_operator.json', scope)
	gc = gspread.authorize(credentials)
	# Google Sheet name = linechatbot/google_api_mobile_operator
	sheet1 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1o9fPEjsk-D_c9j6WeYbwMQtmdsq-HTEbw3E7_rnuUSA/edit#gid=0')

	# # Google Sheet name = line_link_sheet
	# sheet1 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1XQXkBL_JDF26MMbm2MxRe68nVJsh3TYj9Uss8cET2Fo/edit#gid=0')
	worksheet = sheet1.get_worksheet(0) # sheet index in spreadsheets
	global list_data_sheet
	list_data_sheet = worksheet.get_all_values()

app = Flask(__name__)
line_access_token = 'apiNXSRhFfgIJ+ueODzpaYbWloo8mtcVvhp7n6fZAN4/yZ4DWbQChvwxOULpt0c3iUbw1gfvu8HotYNTmvwaCiWVZiGuMoq7mcLQezNZ9J9vlvcDt/1QJXmL1elGMqRX8xOvdSGYjzdeKmQnsMLP2gdB04t89/1O/w1cDnyilFU='

@app.route('/')

@app.route("/webhook", methods=["POST","GET"])
def webhook() :
	from reply_new import ReplyMessage  # ดึง Function จาก File ชื่อ reply_new.py
	if request.method == "GET" :
		return "Your = GET method from ngrok"
	elif request.method == "POST" : # Check Method ถ้าเป็น POST คือเราที่เราส่งข้อความไปในไลน์
		data = request.get_json()   # รับข้อมูลแบบ json
		connect_google_sheet()

		list_result_search = []
		text_from_line = data["events"][0]["message"]["text"]
		reply_token = data["events"][0]["replyToken"]

		for ii in range(len(list_data_sheet)) :
			# ตรวจสอบ
			if text_from_line in list_data_sheet[ii][0] : # ถ้ามี text_from_line (รับจาก User) มีค่าใน Google Sheet
				list_result_search.append([str(list_data_sheet[ii][0]),str(list_data_sheet[ii][1])])

		# กรณี เจอข้อมูล 1 ข้อมูล
		if len(list_result_search) == 0 :
			reply_msg = str(list_data_sheet[ii][0]) + ' : ' + str(list_data_sheet[ii][1])
			ReplyMessage(Reply_token=reply_token, TextMessage=reply_msg,Line_Access_Token=line_access_token)
		# กรณี เจอข้อมูล มากกว่า 1 ข้อมูล
		if len(list_result_search) != 0 :
			reply_msg = []
			for iii in range(len(list_result_search)) :
				result_text = str(list_result_search[iii][0]) + ' : ' + str(list_result_search[iii][1])
				reply_msg = str(reply_msg) + ' , ' + str(result_text)
			print(reply_msg)
			ReplyMessage(Reply_token=reply_token, TextMessage=reply_msg,Line_Access_Token=line_access_token)
		return "OK"

if __name__ == "__main__" :
	app.run(port = 200)