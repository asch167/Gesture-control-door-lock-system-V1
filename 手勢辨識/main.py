from flask import Flask,render_template,request
from FingerCounter import *
import time
import threading


#密碼有效期限(秒)
survivaltime = 15
password= ""
entered=""
app = Flask(__name__)

def resetpasswd():
    timer = 0
    global password,entered
    while True:
        if timer == survivaltime:
            password = ""
            entered=""
            print("密碼效用期已過")
            break
        time.sleep(1)
        timer += 1

@app.route('/',methods=['POST','GET'])
def index():
    global password,timer,survivaltime
    if request.method =='POST':
        if request.values['send']=='送出':
            password = request.values['pass']
            threading.Thread(target=resetpasswd).start()
            print(f"密碼已設定成{password}")
            if survivaltime <= 60:
                return render_template('index.html',tip=f"密碼已設定完成為:{request.values['pass']} 有效時間為{survivaltime}秒")
            if survivaltime > 60 and (survivaltime % 60) == 0:
                return render_template('index.html',tip=f"密碼已設定完成為:{request.values['pass']} 有效時間為{int(survivaltime/60)}分")
            else:
                return render_template('index.html',tip=f"密碼已設定完成為:{request.values['pass']} 有效時間為{int(survivaltime/60)}分{survivaltime%60}秒")
    return render_template('index.html',tip="請輸入你要設定的密碼")

def Gesture_detection():
    global password,entered
    while True:
        time.sleep(1)
        a = detect()
        if a != None:
            if a != "Great":
                entered += a
            print("目前已經輸入的密碼:" + entered)
            print("pass:",password,"enter:",entered)
            if a == "Great" and len(password) != 0:
                if entered == password:
                    print("通過")
                    entered = ""
                    password = ""
                else:
                    print("不通過")
                    entered = ""
                    password = ""
            elif len(password)==0:
                print("請重新生成密碼")
                entered = ""
                password = ""

if __name__ == '__main__':
    t1 = threading.Thread(target=Gesture_detection)
    t1.setDaemon(True)
    t1.start()
    app.run(host='0.0.0.0',port=8080)