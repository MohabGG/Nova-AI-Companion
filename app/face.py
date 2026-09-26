
import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRectF, QPointF
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QPainterPath
)


class FaceWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.emotion = "neutral"
        self.frame = 0

        self.setMinimumHeight(220)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(60)

    def set_emotion(self, emotion):
        self.emotion = emotion
        self.update()

    def animate(self):
        self.frame += 1
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.fillRect(
            self.rect(),
            QColor("#121827")
        )

        w = self.width()
        h = self.height()

        cx = w / 2

        # Floating idle movement
        float_offset = math.sin(self.frame * 0.035) * 3

        cy = h / 2 + float_offset

        # Face background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#222D46"))

        painter.drawRoundedRect(
            QRectF(cx - 115, cy - 94, 230, 188),
            42,
            42
        )

        # Eyes
        painter.setBrush(QColor("#78E9ED"))

        eye_y = cy - 28

        blinking = (self.frame % 100) < 4

        if blinking:

            painter.drawRoundedRect(
                QRectF(cx - 69, eye_y, 43, 4),
                2,
                2
            )

            painter.drawRoundedRect(
                QRectF(cx + 26, eye_y, 43, 4),
                2,
                2
            )

        else:

            eye_height = 29

            if self.emotion == "surprised":
                eye_height = 39

            painter.drawEllipse(
                QRectF(
                    cx - 67,
                    eye_y - eye_height / 2,
                    39,
                    eye_height
                )
            )

            painter.drawEllipse(
                QRectF(
                    cx + 28,
                    eye_y - eye_height / 2,
                    39,
                    eye_height
                )
            )

        # Mouth
        pen = QPen(
            QColor("#78E9ED"),
            5,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        mouth_y = cy + 34

        if self.emotion == "surprised":

            painter.drawEllipse(
                QRectF(cx - 10, mouth_y - 7, 20, 25)
            )

        else:

            path = QPainterPath(
                QPointF(cx - 25, mouth_y)
            )

            if self.emotion == "happy":

                path.cubicTo(
                    QPointF(cx - 13, mouth_y + 20),
                    QPointF(cx + 13, mouth_y + 20),
                    QPointF(cx + 25, mouth_y)
                )

            elif self.emotion == "concerned":

                path.cubicTo(
                    QPointF(cx - 13, mouth_y - 12),
                    QPointF(cx + 13, mouth_y - 12),
                    QPointF(cx + 25, mouth_y)
                )

            elif self.emotion == "curious":

                path.cubicTo(
                    QPointF(cx - 10, mouth_y + 2),
                    QPointF(cx + 10, mouth_y + 8),
                    QPointF(cx + 25, mouth_y + 3)
                )

            else:

                path.lineTo(cx + 25, mouth_y)

            painter.drawPath(path)

        painter.end()
