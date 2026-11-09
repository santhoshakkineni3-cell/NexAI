from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget,
    QPushButton, QLabel, QStackedWidget, QFrame, QSizePolicy, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QMovie, QPixmap, QFont, QTextCharFormat, QColor
from PyQt5.QtCore import Qt, QTimer, QSize
from dotenv import dotenv_values
import sys
import os

# Load environment variables
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname", "Assistant")
current_dir = os.getcwd()
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics")

old_chat_message = ""

def AnswerModifier(Answer):
    return '\n'.join(line for line in Answer.split('\n') if line.strip())

def QueryModifier(Query):
    new_query = Query.lower().strip()
    question_words = {"how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"}
    new_query += "?" if any(new_query.startswith(word) for word in question_words) else "."
    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(os.path.join(TempDirPath, 'Mic.data'), 'w', encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(os.path.join(TempDirPath, 'Mic.data'), 'r', encoding='utf-8') as file:
        return file.read()

def SetAssistantStatus(Status):
    with open(os.path.join(TempDirPath, 'Status.data'), 'w', encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(os.path.join(TempDirPath, 'Status.data'), 'r', encoding='utf-8') as file:
        return file.read()

def GraphicsDirectoryPath(Filename):
    return os.path.join(GraphicsDirPath, Filename)

def TempDirectoryPath(Filename):
    return os.path.join(TempDirPath, Filename)

def ShowTextToScreen(Text):
    with open(os.path.join(TempDirPath, 'Responses.data'), "w", encoding='utf-8') as file:
        file.write(Text)

class ChatSection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        self.chat_text_edit.setFont(QFont("Arial", 13))

        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        self.gif_label.setMovie(movie)
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        movie.start()
        layout.addWidget(self.gif_label)

        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-right: 195px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def loadMessages(self):
        global old_chat_message
        with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
            messages = file.read().strip()
            if messages and messages != old_chat_message:
                self.addMessage(messages, 'White')
                old_chat_message = messages

    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
            self.label.setText(file.read())

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format_text = QTextCharFormat()
        format_text.setForeground(QColor(color))
        cursor.setCharFormat(format_text)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        self.gif_label.setMovie(movie)
        self.gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)
        self.setStyleSheet("background-color: black;")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        stacked_widget = QStackedWidget(self)
        stacked_widget.addWidget(InitialScreen())
        stacked_widget.addWidget(ChatSection())
        self.setCentralWidget(stacked_widget)

        top_bar = QHBoxLayout()
        home_button = QPushButton("Home")
        message_button = QPushButton("Chat")
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        top_bar.addWidget(home_button)
        top_bar.addWidget(message_button)
        top_bar.addWidget(close_button)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addLayout(top_bar)
        layout.addWidget(stacked_widget)
        self.setCentralWidget(container)

        home_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))

        self.setStyleSheet("background-color: black;")
        self.showFullScreen()

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()
