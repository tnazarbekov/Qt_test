import sys

from PyQt6 import uic, QtCore, QtGui, QtWidgets
import datetime
import requests
from requests.exceptions import HTTPError
import json


class MainWindow(QtWidgets.QMainWindow):
    ServerAdress = "http://localhost:5000"
    MessageID = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('messenger.ui', self)
        self.pushButton.clicked.connect(self.pushButton_clicked)

    def pushButton_clicked(self):
        self.SendMessage()

    def SendMessage(self):
        UserName = self.lineEdit1.text()
        MessageText = self.lineEdit2.text()
        TimeStamp = str(datetime.datetime.today())
        msg = f"{{\"UserName\": \"{UserName}\", \"MessageText\": \"{MessageText}\", \"TimeStamp\": \"{TimeStamp}\"}}"
        # {"UserName": "RusAl", "MessageText": "Privet na sto let!!!", "TimeStamp": "2021-03-05T18:23:10.932973Z"}
        print("Отправлено сообщение: " + msg)
        url = self.ServerAdress + "/api/Messanger"
        data = json.loads(msg)  # string to json
        r = requests.post(url, json=data)
        # print(r.status_code, r.reason)

    def GetMessage(self, id):
        id = str(id)
        url = self.ServerAdress + "/api/Messanger/" + id
        # print(url)
        try:
            response = requests.get(url)
            # если ответ успешен, исключения задействованы не будут
            response.raise_for_status()
        except HTTPError as http_err:
            # print(f'HTTP error occurred: {http_err}')  # Python 3.6
            return None
        except Exception as err:
            # print(f'Other error occurred: {err}')  # Python 3.6
            return None
        else:
            text = response.text
            return text

    def timerEvent(self):
        msg = self.GetMessage(self.MessageID)
        if msg is not None:
            msg = json.loads(msg)
            UserName = msg["UserName"]
            MessageText = msg["MessageText"]
            TimeStamp = msg["TimeStamp"]
            msgtext =f"{TimeStamp} : <{UserName}> : {MessageText}"
            print(msgtext)
            self.listWidget.insertItem(  self.MessageID, msgtext)
            self.MessageID+=1
            msg = self.GetMessage(self.MessageID)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)
    timer.timeout.connect(w.timerEvent)
    timer.start(5000)
    sys.exit(app.exec())