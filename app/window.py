
import html

from PySide6.QtCore import QThread, Signal, Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QCheckBox,
    QInputDialog,
    QMessageBox
)

from app.brain import Brain
from app.face import FaceWidget
from app.memory import Memory
from app.personality import COMPANION_NAME
from app.voice import record_and_transcribe, speak


class ChatWorker(QThread):

    completed = Signal(str, str)
    failed = Signal(str)

    def __init__(self, brain, message):
        super().__init__()

        self.brain = brain
        self.message = message

    def run(self):

        try:
            reply, emotion = self.brain.respond(
                self.message
            )

            self.completed.emit(reply, emotion)

        except Exception as error:
            self.failed.emit(str(error))


class MicrophoneWorker(QThread):

    completed = Signal(str)
    failed = Signal(str)

    def run(self):

        try:
            transcript = record_and_transcribe()
            self.completed.emit(transcript)

        except Exception as error:
            self.failed.emit(str(error))


class SpeechWorker(QThread):

    failed = Signal(str)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):

        try:
            speak(self.text)

        except Exception as error:
            self.failed.emit(str(error))


class CompanionWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.memory = Memory()
        self.brain = Brain(self.memory)

        self.workers = []

        self.chat_busy = False
        self.mic_busy = False
        self.speech_busy = False

        self.setup_ui()

    def setup_ui(self):

        self.setWindowTitle("AI Companion")

        self.resize(650, 740)

        self.setStyleSheet("""
            QWidget {
                background-color: #121827;
                color: #F0F4FA;
                font-size: 14px;
            }

            QTextEdit, QLineEdit {
                background-color: #1E2940;
                border: 1px solid #34415C;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton {
                background-color: #31415E;
                border-radius: 8px;
                padding: 10px;
            }

            QPushButton:hover {
                background-color: #405779;
            }

            QPushButton:disabled {
                color: #7E8798;
                background-color: #242D3D;
            }
        """)

        layout = QVBoxLayout(self)

        title = QLabel(COMPANION_NAME)

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(
            "font-size: 23px; font-weight: bold;"
        )

        layout.addWidget(title)

        # Animated character
        self.face = FaceWidget()

        layout.addWidget(self.face)

        # Conversation window
        self.chat = QTextEdit()

        self.chat.setReadOnly(True)

        layout.addWidget(self.chat)

        # Text input
        input_row = QHBoxLayout()

        self.text_input = QLineEdit()

        self.text_input.setPlaceholderText(
            "Say something..."
        )

        self.text_input.returnPressed.connect(
            self.send_message
        )

        input_row.addWidget(self.text_input)

        self.send_button = QPushButton("Send")

        self.send_button.clicked.connect(
            self.send_message
        )

        input_row.addWidget(self.send_button)

        layout.addLayout(input_row)

        # Voice and memory controls
        controls = QHBoxLayout()

        self.mic_button = QPushButton("Record 5s")

        self.mic_button.clicked.connect(
            self.record_voice
        )

        controls.addWidget(self.mic_button)

        self.voice_checkbox = QCheckBox("Speak replies")

        controls.addWidget(self.voice_checkbox)

        self.memory_button = QPushButton(
            "Remember a fact"
        )

        self.memory_button.clicked.connect(
            self.remember_fact
        )

        controls.addWidget(self.memory_button)

        layout.addLayout(controls)

        # Status indicator
        self.status = QLabel("Ready")

        self.status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(self.status)

        self.add_message(
            "System",
            f"{COMPANION_NAME} is ready. Say hello!"
        )

    def add_message(self, sender, message):

        sender = html.escape(sender)

        message = html.escape(message)

        message = message.replace("\n", "<br>")

        self.chat.append(
            f"<b>{sender}:</b> {message}"
        )

    def keep_worker(self, worker):

        self.workers.append(worker)

        def release_worker():

            if worker in self.workers:
                self.workers.remove(worker)

            worker.deleteLater()

        worker.finished.connect(release_worker)

        worker.start()

    def update_buttons(self):

        busy = self.chat_busy or self.mic_busy

        self.send_button.setEnabled(not busy)

        self.mic_button.setEnabled(not busy)

    def send_message(self):

        if self.chat_busy or self.mic_busy:
            return

        message = self.text_input.text().strip()

        if not message:
            return

        self.text_input.clear()

        self.add_message("You", message)

        self.chat_busy = True

        self.update_buttons()

        self.status.setText(
            f"{COMPANION_NAME} is thinking..."
        )

        self.face.set_emotion("curious")

        worker = ChatWorker(
            self.brain,
            message
        )

        worker.completed.connect(
            self.receive_response
        )

        worker.failed.connect(
            self.chat_error
        )

        worker.finished.connect(
            self.finish_chat
        )

        self.keep_worker(worker)

    def receive_response(self, reply, emotion):

        self.add_message(
            COMPANION_NAME,
            reply
        )

        self.face.set_emotion(emotion)

        self.status.setText(
            f"Emotion: {emotion}"
        )

        if self.voice_checkbox.isChecked():
            self.start_speech(reply)

    def chat_error(self, error):

        self.add_message(
            "System",
            "AI error: " + error
        )

        self.face.set_emotion("concerned")

        self.status.setText("AI error")

    def finish_chat(self):

        self.chat_busy = False

        self.update_buttons()

    def record_voice(self):

        if self.chat_busy or self.mic_busy:
            return

        self.mic_busy = True

        self.update_buttons()

        self.status.setText(
            "Recording for five seconds..."
        )

        worker = MicrophoneWorker()

        worker.completed.connect(
            self.receive_transcript
        )

        worker.failed.connect(
            self.microphone_error
        )

        self.keep_worker(worker)

    def receive_transcript(self, transcript):

        self.mic_busy = False

        self.update_buttons()

        if not transcript:

            self.status.setText(
                "No speech detected. Please try again."
            )

            return

        self.text_input.setText(transcript)

        self.status.setText(
            "Speech recognized"
        )

        self.send_message()

    def microphone_error(self, error):

        self.mic_busy = False

        self.update_buttons()

        self.status.setText(
            "Microphone error"
        )

        self.add_message(
            "System",
            error
        )

    def start_speech(self, text):

        # Avoid playing two spoken replies simultaneously.
        if self.speech_busy:
            return

        self.speech_busy = True

        worker = SpeechWorker(text)

        worker.failed.connect(
            lambda error: self.add_message(
                "System",
                "Voice error: " + error
            )
        )

        worker.finished.connect(
            self.finish_speech
        )

        self.keep_worker(worker)

    def finish_speech(self):
        self.speech_busy = False

    def remember_fact(self):

        fact, accepted = QInputDialog.getText(
            self,
            "Save Memory",
            "What should the AI remember?"
        )

        if accepted and fact.strip():

            self.memory.remember(fact)

            self.add_message(
                "System",
                "Memory saved locally."
            )

            self.status.setText(
                "Memory updated"
            )

    def closeEvent(self, event):

        if any(worker.isRunning() for worker in self.workers):

            event.ignore()

            QMessageBox.information(
                self,
                "AI Companion",
                "An operation is still running. "
                "Close the window after it finishes."
            )

            return

        event.accept()
