import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                                QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence

class KalkulatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_shortcuts()

    def init_ui(self):
        self.setWindowTitle("Kalkulator")
        self.setFixedWidth(380)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5) 
        main_layout.setContentsMargins(15, 15, 15, 15)

        lbl_style = "font-weight: 500; margin-top: 5px;"

        lbl1 = QLabel("Angka Pertama")
        lbl1.setStyleSheet(lbl_style)
        main_layout.addWidget(lbl1)
        
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("0")
        self.input1.setFixedHeight(30)
        main_layout.addWidget(self.input1)
        
        self.err_label1 = QLabel("⚠ Input harus berupa angka")
        self.err_label1.setStyleSheet("color: red; font-size: 10px;")
        self.err_label1.hide() 
        main_layout.addWidget(self.err_label1)

        lbl_op = QLabel("Operasi")
        lbl_op.setStyleSheet(lbl_style)
        main_layout.addWidget(lbl_op)
        
        self.combo_ops = QComboBox()
        self.combo_ops.addItems(["+ Tambah", "- Kurang", "× Kali", "÷ Bagi"])
        self.combo_ops.setFixedHeight(30)
        main_layout.addWidget(self.combo_ops)

        lbl2 = QLabel("Angka Kedua")
        lbl2.setStyleSheet(lbl_style)
        main_layout.addWidget(lbl2)
        
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("0")
        self.input2.setFixedHeight(30)
        main_layout.addWidget(self.input2)
        
        self.err_label2 = QLabel("⚠ Input harus berupa angka")
        self.err_label2.setStyleSheet("color: red; font-size: 10px;")
        self.err_label2.hide() 
        main_layout.addWidget(self.err_label2)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.setContentsMargins(0, 10, 0, 5)
        
        self.btn_hitung = QPushButton("Hitung (Enter)")
        self.btn_clear = QPushButton("Clear (Esc)")
        self.btn_hitung.setFixedHeight(35)
        self.btn_clear.setFixedHeight(35)
        
        self.btn_clear.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 4px;")
        self.update_button_style(False)
        
        btn_layout.addWidget(self.btn_hitung)
        btn_layout.addWidget(self.btn_clear)
        main_layout.addLayout(btn_layout)

        self.lbl_hasil = QLabel("Hasil: —")
        self.lbl_hasil.setAlignment(Qt.AlignCenter)
        self.lbl_hasil.setStyleSheet("""
            background-color: #f8f9fa; 
            border-radius: 4px; 
            padding: 10px; 
            font-weight: bold;
            border: 1px solid #eee;
        """)
        main_layout.addWidget(self.lbl_hasil)

        self.status_msg = QLabel("⚠ Input tidak valid — tombol Hitung dinonaktifkan")
        self.status_msg.setStyleSheet("""
            background-color: #f2dede; 
            color: #a94442; 
            padding: 8px; 
            border-radius: 4px;
            margin-top: 5px;
        """)
        self.status_msg.hide() 
        main_layout.addWidget(self.status_msg)

        self.input1.textChanged.connect(self.validasi_realtime)
        self.input2.textChanged.connect(self.validasi_realtime)
        self.btn_hitung.clicked.connect(self.proses_hitung)
        self.btn_clear.clicked.connect(self.proses_clear)

        self.setLayout(main_layout)

    def setup_shortcuts(self):
        QShortcut(QKeySequence(Qt.Key_Return), self, self.proses_hitung)
        QShortcut(QKeySequence(Qt.Key_Escape), self, self.proses_clear)

    def is_number(self, s):
        if not s: return True
        try:
            float(s.replace(',', '.'))
            return True
        except ValueError:
            return False

    def update_button_style(self, active):
        if active:
            self.btn_hitung.setEnabled(True)
            self.btn_hitung.setStyleSheet("background-color: #3498db; color: white; border-radius: 4px;")
        else:
            self.btn_hitung.setEnabled(False)
            self.btn_hitung.setStyleSheet("background-color: #bdc3c7; color: white; border-radius: 4px;")

    def validasi_realtime(self):
        txt1 = self.input1.text().strip()
        txt2 = self.input2.text().strip()
        
        val1 = self.is_number(txt1)
        val2 = self.is_number(txt2)
        
        self.input1.setStyleSheet("border: 1px solid red;" if not val1 else "")
        self.err_label1.setVisible(not val1)
        
        self.input2.setStyleSheet("border: 1px solid red;" if not val2 else "")
        self.err_label2.setVisible(not val2)

        input_salah = (not val1 and txt1 != "") or (not val2 and txt2 != "")
        self.status_msg.setVisible(input_salah)

        bisa_hitung = False
        if txt1 != "" and txt2 != "":
            try:
                float(txt1.replace(',', '.')); float(txt2.replace(',', '.'))
                bisa_hitung = True
            except:
                bisa_hitung = False
        
        self.update_button_style(bisa_hitung)

    def proses_hitung(self):
        if not self.btn_hitung.isEnabled(): return
        
        try:
            n1 = float(self.input1.text().replace(',', '.'))
            n2 = float(self.input2.text().replace(',', '.'))
            op_text = self.combo_ops.currentText()
            
            if "+ Tambah" in op_text: hasil = n1 + n2
            elif "- Kurang" in op_text: hasil = n1 - n2
            elif "× Kali" in op_text: hasil = n1 * n2
            elif "÷ Bagi" in op_text:
                if n2 == 0: raise ZeroDivisionError
                hasil = n1 / n2
            
            self.lbl_hasil.setText(f"Hasil: {hasil:g}")
            
        except ZeroDivisionError:
            QMessageBox.critical(self, "Error", "Tidak dapat membagi dengan nol!")
            self.lbl_hasil.setText("Hasil: Error")

    def proses_clear(self):
        self.input1.clear()
        self.input2.clear()
        self.lbl_hasil.setText("Hasil: —")
        self.input1.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KalkulatorApp()
    window.show()
    sys.exit(app.exec())