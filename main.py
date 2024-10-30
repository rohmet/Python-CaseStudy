import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QMainWindow, QStackedWidget, QTableWidget, QTableWidgetItem,
    QCheckBox, QHeaderView, QListWidget, QListWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt

# Data akun
accounts = {
    "60900123031": "comel",
    "60900123042": "mahirG",
    "60900121050": "sat21nger",
    "1": "1"
}

# Data Mata Kuliah Semester 1
data_semester1 = [
    ("UIN122404", "Akidah Ahlak", "Hastuti S.Pd.I. M.Pd.I.", "W", 3),
    ("UIN122403", "Ilmu Fikih", "Hastuti S.Pd.I. M.Pd.I.", "W", 2),
    ("SIN122408", "Matematika Komputer", "Izmy Alwiah Musdar, S.Kom. M.Cs", "W", 2),
    ("SIN142410", "Computational Thinking", "FAISAL S.Kom.M.Kom; Rahman S. Kom. M.T.", "W", 4),
    ("SIN132409", "Konsep Sistem Informasi", "Asrul Azhari Muin S.Kom, M.Kom; Erfina S.Kom. M.Kom.", "W", 3),
    ("SIN132411", "Pengantar Teknologi Informasi", "M. Sya'rani Machrizzandi S.Kom. M.Kom; Erfina S.Kom. M.Kom", "W", 3),
    ("UIN122406", "Bahasa Indonesia", "Dr. Hj.RAHMIATI S.Pd. M.Pd", "W", 2),
    ("SIN012412", "Ilmu Tajwid & Hafalan Juz 30", "Hastuti S.Pd.I. M.Pd.I.", "W", 1)
]

# Load selected courses from JSON
def load_selected_courses(nim):
    try:
        with open("selected_courses.json", "r") as f:
            data = json.load(f)
            return data.get(nim, [])
    except FileNotFoundError:
        return []

# Save selected courses to JSON
def save_selected_courses(nim, selected_courses):
    try:
        with open("selected_courses.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    
    data[nim] = selected_courses
    
    with open("selected_courses.json", "w") as f:
        json.dump(data, f)

class LoginPage(QWidget):
    def __init__(self, switch_page):
        super().__init__()
        self.switch_page = switch_page
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)  # Add margins to the layout

        # Set background color
        self.setStyleSheet("background-color: #f0f0f0;")

        # Title
        self.title_label = QLabel("Selamat Datang")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 3vw; font-weight: bold; color: #333;")
        layout.addWidget(self.title_label)

        # NIM
        self.nim_label = QLabel("NIM:")
        self.nim_label.setStyleSheet("font-size: 2vw; color: #333;")
        self.nim_input = QLineEdit()
        self.nim_input.setPlaceholderText("Masukkan NIM Anda")
        self.nim_input.setStyleSheet(self.input_style())
        layout.addWidget(self.nim_label)
        layout.addWidget(self.nim_input)

        # Password
        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet("font-size: 2vw; color: #333;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Masukkan Password Anda")
        self.password_input.setStyleSheet(self.input_style())
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet(self.button_style())
        self.login_button.setCursor(Qt.PointingHandCursor)  # Change cursor to pointer
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        self.setMinimumSize(400, 300)  # Set minimum size for the login window

    def input_style(self):
        return """
            padding: 10px; 
            border: 1px solid #ccc; 
            border-radius: 5px; 
            font-size: 1.5vw;
        """

    def button_style(self):
        return """
            background-color: #4CAF50; 
            color: white; 
            font-weight: bold; 
            padding: 10px; 
            border-radius: 5px; 
            border: none; 
            font-size: 2vw;
        """

    def check_login(self):
        nim = self.nim_input.text()
        password = self.password_input.text()
        
        if nim in accounts and accounts[nim] == password:
            self.switch_page(nim)
        else:
            QMessageBox.warning(self, "Error", "NIM atau password salah!")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Adjust font sizes based on the window size
        size_factor = self.height() / 300  # Base height for calculations
        self.title_label.setStyleSheet(f"font-size: {3 * size_factor}vw; font-weight: bold; color: #333;")
        for widget in self.findChildren(QLabel):
            widget.setStyleSheet(f"font-size: {2 * size_factor}vw; color: #333;")
        self.nim_input.setStyleSheet(self.input_style())
        self.password_input.setStyleSheet(self.input_style())
        self.login_button.setStyleSheet(self.button_style())  # Refresh button style

class HomePage(QWidget):
    def __init__(self, nim, switch_to_semester_page):
        super().__init__()
        self.nim = nim
        self.switch_to_semester_page = switch_to_semester_page
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Add margins to the layout
        layout.setAlignment(Qt.AlignTop)

        # Set background color
        self.setStyleSheet("background-color: #e8f5e9;")  # Light green background

        # Welcome Label
        self.welcome_label = QLabel("Selamat datang di halaman beranda!")
        self.welcome_label.setStyleSheet("font-size: 2.5vw; font-weight: bold; color: #2e7d32;")
        layout.addWidget(self.welcome_label)

        # Semester 1 Button
        self.semester1_button = QPushButton("Semester 1")
        self.semester1_button.setStyleSheet(self.button_style())
        self.semester1_button.clicked.connect(lambda: self.switch_to_semester_page("Semester 1"))
        layout.addWidget(self.semester1_button)

        # Keranjang Mata Kuliah
        self.keranjang_label = QLabel("Keranjang Mata Kuliah")
        self.keranjang_label.setStyleSheet("font-size: 2vw; color: #2e7d32;")
        layout.addWidget(self.keranjang_label)

        self.keranjang_list = QListWidget()
        self.load_keranjang()
        self.keranjang_list.setStyleSheet("font-size: 1.5vw;")  # Responsive font size
        layout.addWidget(self.keranjang_list)

        # Hapus Mata Kuliah Button
        self.hapus_button = QPushButton("Hapus Mata Kuliah")
        self.hapus_button.setStyleSheet(self.button_style())
        self.hapus_button.clicked.connect(self.hapus_matakuliah)
        layout.addWidget(self.hapus_button)

        self.setLayout(layout)

    def button_style(self):
        return """
            background-color: #4CAF50; 
            color: white; 
            font-weight: bold; 
            padding: 10px; 
            border-radius: 5px; 
            border: none; 
            font-size: 2vw;
        """
    
    def load_keranjang(self):
        selected_courses = load_selected_courses(self.nim)
        self.keranjang_list.clear()
        for course in selected_courses:
            item = QListWidgetItem(course)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.keranjang_list.addItem(item)

    def hapus_matakuliah(self):
        selected_courses = load_selected_courses(self.nim)
        updated_courses = []
        
        for i in range(self.keranjang_list.count()):
            item = self.keranjang_list.item(i)
            if item.checkState() != Qt.Checked:
                updated_courses.append(item.text())
        
        save_selected_courses(self.nim, updated_courses)
        self.load_keranjang()
        QMessageBox.information(self, "Info", "Mata kuliah yang dipilih berhasil dihapus.")

class SemesterPage(QWidget):
    def __init__(self, nim, switch_to_homepage):
        super().__init__()
        self.nim = nim
        self.switch_to_homepage = switch_to_homepage
        self.initUI()

    def initUI(self):
        # Set layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title Label
        title_label = QLabel("Pilih Mata Kuliah - Semester 1")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)

        # Table for courses
        self.table = QTableWidget(len(data_semester1), 6)
        self.table.setHorizontalHeaderLabels(["Kode", "Mata Kuliah", "Dosen", "Kelas", "SKS", "Pilih"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Customize the table
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                font-size: 16px;
                selection-background-color: #e3f2fd;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
            }
        """)

        # Populate the table with courses
        for row, course in enumerate(data_semester1):
            for col, item in enumerate(course):
                self.table.setItem(row, col, QTableWidgetItem(str(item)))
            # Add checkbox in the last column for selection
            checkbox = QCheckBox()
            self.table.setCellWidget(row, 5, checkbox)
        
        layout.addWidget(self.table)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Button to select courses
        self.select_button = QPushButton("Ambil Mata Kuliah")
        self.select_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        self.select_button.clicked.connect(self.add_selected_courses)
        buttons_layout.addWidget(self.select_button)

        # Back button to go back to the homepage
        self.back_button = QPushButton("Kembali ke Beranda")
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        self.back_button.clicked.connect(self.switch_to_homepage)
        buttons_layout.addWidget(self.back_button)

        layout.addLayout(buttons_layout)

        # Add layout to the main widget
        self.setLayout(layout)
    
    def add_selected_courses(self):
        selected_courses = load_selected_courses(self.nim)
        
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 5)
            if checkbox.isChecked():
                course_name = self.table.item(row, 1).text()
                if course_name not in selected_courses:
                    selected_courses.append(course_name)
        
        save_selected_courses(self.nim, selected_courses)
        QMessageBox.information(self, "Sukses", "Mata kuliah berhasil diambil dan disimpan.")
        self.switch_to_homepage()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Login dan Beranda")
        
        # Stack of Pages
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pages
        self.login_page = LoginPage(self.show_home_page)
        self.stack.addWidget(self.login_page)
        
    def show_home_page(self, nim):
        self.home_page = HomePage(nim, self.show_semester_page)
        self.stack.addWidget(self.home_page)
        self.stack.setCurrentWidget(self.home_page)

    def show_semester_page(self, semester):
        self.semester_page = SemesterPage(self.home_page.nim, lambda: self.show_home_page(self.home_page.nim))
        self.stack.addWidget(self.semester_page)
        self.stack.setCurrentWidget(self.semester_page)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
