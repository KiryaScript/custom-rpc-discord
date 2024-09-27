import sys
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QMessageBox, QListWidget, 
                             QListWidgetItem, QComboBox, QTabWidget)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer
from pypresence import Presence
import random

class CustomButton(QPushButton):
    def __init__(self, icon_path, size=40, *args, **kwargs):
        super(CustomButton, self).__init__(*args, **kwargs)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QPixmap(icon_path).scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation).size())
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #36393f;
                border-radius: {size // 2}px;
                min-height: {size}px;
                max-height: {size}px;
                min-width: {size}px;
                max-width: {size}px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: #40444b;
            }}
        """)

class DiscordLikeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.RPC = None
        self.initUI()
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_random_status)
        self.status_timer.start(5000)

    def initUI(self):
        self.setWindowTitle('Custom RPC By Devik')
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #36393f; color: #ffffff;")

        main_widget = QWidget()
        main_layout = QHBoxLayout()

        left_panel = QWidget()
        left_panel.setStyleSheet("background-color: #202225; max-width: 70px; min-width: 70px;")
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        server_icons = [
            "icons\discord.png", "icons\github.png", "icons\reddit.png", "icons\twitter.png", "icons\youtube.png"
        ]
        for icon in server_icons:
            button = CustomButton(f"icons/{icon}")
            left_layout.addWidget(button)

        left_layout.addStretch()

        github_button = CustomButton("icons/mygithub.png", 30)
        github_button.clicked.connect(lambda: webbrowser.open("https://github.com/KiryaScript"))
        left_layout.addWidget(github_button)

        friend_github_button = CustomButton("icons/friend.png", 30)
        friend_github_button.clicked.connect(lambda: webbrowser.open("https://github.com/sekalYT"))
        left_layout.addWidget(friend_github_button)

        central_widget = QTabWidget()
        central_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #40444b;
                background: #36393f;
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
            QTabBar::tab {
                background: #202225;
                color: #ffffff;
                padding: 5px;
            }
            QTabBar::tab:selected {
                background: #40444b;
            }
        """)

        rpc_tab = QWidget()
        rpc_layout = QVBoxLayout()

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Enter Client ID")
        self.style_input(self.client_id_input)
        rpc_layout.addWidget(self.client_id_input)

        connect_button = QPushButton("Connect to Discord")
        self.style_button(connect_button)
        connect_button.clicked.connect(self.connect_to_discord)
        rpc_layout.addWidget(connect_button)

        self.state_input = QLineEdit()
        self.details_input = QLineEdit()
        self.large_image_input = QLineEdit()
        self.large_text_input = QLineEdit()
        self.small_image_input = QLineEdit()
        self.small_text_input = QLineEdit()

        for input_field in [self.state_input, self.details_input, self.large_image_input, 
                            self.large_text_input, self.small_image_input, self.small_text_input]:
            self.style_input(input_field)
            rpc_layout.addWidget(QLabel(input_field.objectName().capitalize().replace('_', ' ')))
            rpc_layout.addWidget(input_field)

        update_button = QPushButton("Update Presence")
        self.style_button(update_button)
        update_button.clicked.connect(self.update_presence)
        rpc_layout.addWidget(update_button)

        rpc_tab.setLayout(rpc_layout)
        central_widget.addTab(rpc_tab, "Rich Presence")

        # имитация чата
        chat_tab = QWidget()
        chat_layout = QVBoxLayout()

        self.chat_display = QListWidget()
        self.chat_display.setStyleSheet("background-color: #40444b; border: none;")
        chat_layout.addWidget(self.chat_display)

        chat_input = QLineEdit()
        self.style_input(chat_input)
        chat_input.setPlaceholderText("Type a message...")
        chat_input.returnPressed.connect(lambda: self.send_message(chat_input.text()))
        chat_layout.addWidget(chat_input)

        chat_tab.setLayout(chat_layout)
        central_widget.addTab(chat_tab, "Chat")

        # пользователи справа
        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: #2f3136; max-width: 240px; min-width: 240px;")
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        users = [
            ("Devik", "Online"),
            ("очко влагалище", "Idle"),
            ("sekal", "Do Not Disturb"),
            ("Въетнам", "Offline"),
            ("кондиции", "Online"),
        ]
        for name, status in users:
            user_widget = QWidget()
            user_layout = QHBoxLayout()
            user_widget.setLayout(user_layout)

            avatar = QLabel()
            avatar.setPixmap(QPixmap("icons/user_avatar.png").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            user_layout.addWidget(avatar)

            user_info = QVBoxLayout()
            user_info.addWidget(QLabel(name))
            status_label = QLabel(status)
            status_label.setStyleSheet("color: #999;")
            user_info.addWidget(status_label)
            user_layout.addLayout(user_info)

            right_layout.addWidget(user_widget)

        right_layout.addStretch()

        # Добавляем все панели в главный layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(central_widget)
        main_layout.addWidget(right_panel)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def style_input(self, widget):
        widget.setStyleSheet("""
            QLineEdit {
                background-color: #40444b;
                border: none;
                padding: 5px;
                margin: 5px;
                color: #ffffff;
            }
        """)

    def style_button(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #7289da;
                color: white;
                border: none;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #677bc4;
            }
        """)

    def connect_to_discord(self):
        client_id = self.client_id_input.text()
        if not client_id:
            QMessageBox.warning(self, "Error", "Please enter a Client ID")
            return

        try:
            self.RPC = Presence(client_id)
            self.RPC.connect()
            QMessageBox.information(self, "Success", "Connected to Discord successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to Discord: {str(e)}")

    def update_presence(self):
        if not self.RPC:
            QMessageBox.warning(self, "Error", "Please connect to Discord first")
            return

        state = self.state_input.text()
        details = self.details_input.text()
        large_image = self.large_image_input.text()
        large_text = self.large_text_input.text()
        small_image = self.small_image_input.text()
        small_text = self.small_text_input.text()

        try:
            self.RPC.update(
                state=state,
                details=details,
                large_image=large_image,
                large_text=large_text,
                small_image=small_image,
                small_text=small_text
            )
            QMessageBox.information(self, "Success", "Presence updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error updating presence: {str(e)}")

    def send_message(self, message):
        if message:
            item = QListWidgetItem(f"You: {message}")
            item.setTextAlignment(Qt.AlignRight)
            self.chat_display.addItem(item)
            self.chat_display.scrollToBottom()
            QTimer.singleShot(1000, self.bot_reply)

    # фразы в чате от бота
    def bot_reply(self):
        replies = [
            "Interesting point!",
            "I'm not sure I understand. Can you elaborate?",
            "That's a great idea!",
            "I'll have to think about that.",
            "Thanks for sharing!",
            "How does that relate to our previous discussion?",
            "Can you provide an example?",
            "I hadn't considered that perspective before.",
            "That's a complex issue. What do you think is the best approach?",
            "I appreciate your input on this matter."
        ]
        bot_message = random.choice(replies)
        item = QListWidgetItem(f"Bot: {bot_message}")
        item.setTextAlignment(Qt.AlignLeft)
        self.chat_display.addItem(item)
        self.chat_display.scrollToBottom()

    # рандомные статусы
    def update_random_status(self):
        statuses = ["Playing a game", "Listening to Spotify", "Watching a stream", "In a meeting", "Coding"]
        new_status = random.choice(statuses)
        self.state_input.setText(new_status)
        if self.RPC:
            try:
                self.RPC.update(state=new_status)
            except:
                pass

    def closeEvent(self, event):
        if self.RPC:
            self.RPC.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DiscordLikeApp()
    ex.show()
    sys.exit(app.exec_())