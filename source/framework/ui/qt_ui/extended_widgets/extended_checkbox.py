from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter
from PyQt5.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
    pyqtSlot, pyqtProperty)


class ExtendedCheckBox(QCheckBox):
    
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self,
        parent=None,
        bar_color=Qt.gray,
        checked_color="#00B0FF",
        handle_color=Qt.white,
        pulse_unchecked_color="#44999999",
        pulse_checked_color="#4400B0EE",
        **kwargs):
        super(ExtendedCheckBox, self).__init__(parent, **kwargs)
        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))

        # Setup the rest of the widget.
        self.setContentsMargins(0, 0, 0, 0)
        self._handle_position = 0

        self._pulse_radius = 0

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)  # time in ms

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(100)  # time in ms
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(15)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        # self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)

    def sizeHint(self):
        return QSize(58, 25)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @pyqtSlot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        handleRadius = round(0.35 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 5,
            4 * handleRadius, 2 * handleRadius
        )
        barRect.moveLeft(contRect.left())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @pyqtProperty(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_position = pos
        self.update()

    @pyqtProperty(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()
# ===========================================



    def setValue(self, val, **kwargs):
        if isinstance(val, bool):
            self.setChecked(val)
        else:
            self.setChecked(bool(val))

    def getValue(self):
        if self.isHidden(): return None
        else: return int(self.isChecked())

    def setReadOnly(self, val):
        val = not bool(val)
        self.setEnabled(val)