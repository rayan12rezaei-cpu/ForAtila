import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

try: json_path = f"{sys._MEIPASS}\\data.json"
except: json_path = f"{os.path.abspath('.')}\\data.json"

style = """

QWidget#Win {
    background-color: #212121;
    border-radius: 10px;
}
QPushButton {
    background-color: #f0f0f0;
    color: #212121;
    border-radius: 10px;
}
QPushButton#close {
    background-color: red;
    color: #212121;
    border-radius: 10px;
}
QLineEdit {
    background-color: #f0f0f0;
    color: #212121;
    border-radius: 10px;
}
QLabel {
    color: #212121;
}

"""

class ProvinceDetectorApp(QWidget):
    def __init__(self):

        global json_path
        
        super().__init__()

        detector = PrvinceDetector(json_path)

        self.setObjectName("Win")
        
        self.setWindowTitle("كدملي ياب براي آتيلا احمدزاده")

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.main_layout = QVBoxLayout()

        self.codeEntry = QLineEdit()
        self.main_layout.addWidget(self.codeEntry)
        
        self.detectBtn = QPushButton("بررسي")
        self.detectBtn.clicked.connect(self.detect)
        self.main_layout.addWidget(self.detectBtn)

        self.result = QLabel("استان")
        self.main_layout.addWidget(self.result)

        self.closeBtn = QPushButton("بستن")
        self.closeBtn.clicked.connect(self.close)
        self.closeBtn.setObjectName("close")
        self.main_layout.addWidget(self.closeBtn)
        
        self.setLayout(self.main_layout)

    def detect(self):
        self.result.setText(self.detector.detect(self.codeEntry.text()))
        self.update()

class ProvinceDetector:
    def __init__(self, json_file: str):
        self.provinces_data = self._load_data(json_file)

    def _load_data(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)['provinces']
        except FileNotFoundError:
            print("Can\'t load json | خطا در json")
            return []

    def is_valid_national_code(code: str) -> bool:
        if not (code.isdigit() and len(code) == 10):
            return False
        digits = [int(d) for d in code]
        checksum = sum(digits[i] * (10 - i) for i in range(9))
        remainder = checksum % 11
        if remainder < 2:
            return digits[9] == remainder
        else:
            return digits[9] == (11 - remainder)
  
    def detect(self, national_code: str):
        if not is_valid_national_code(national_code):
            return "not valid | نامعتبر"

        prefix = int(national_code[:3])

        for item in self.provinces_data:
            for start, end in item['ranges']:
                if start <= prefix <= end:

                    return item['name']
        
        return "unknow | نامشخص"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    win = ProvinceDetectorApp()
    win.show()
    sys.exit(app.exec_())
