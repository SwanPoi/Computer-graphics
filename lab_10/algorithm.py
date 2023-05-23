from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen, QBrush, QPixmap, QImage, QColor, QVector3D

from typing import List

class hidden_line:
    def __init__(self, scene: QGraphicsScene, func, xRange, zRange, transform):
        self.EPS = 1e-7
        self.canvas = scene
        self.left: int = -1000
        self.right: int = 1000
        self.bottom: int = -1000
        self.top: int = 1000
        self.func = func
        self.xRange: List[float] = xRange
        self.zRange: List[float] = zRange
        self.transform = transform

    def drawFloatingHorizon(self):
        width = self.right - self.left + 1
        highHorizon: List[int] = [self.bottom] * width
        lowHorizon: List[int] = [self.top] * width

        self.check_direction()

        curL = None
        curR = None

        for z in self.zRange:
            prev: QVector3D = QVector3D(self.xRange[0], self.func(self.xRange[0], z), z)
            prev = self.transform(prev)
            if curL is not None:
                self.drawHorizonLine(prev, curL, lowHorizon, highHorizon)

            curL = prev

            self.drawHorizon(z, lowHorizon, highHorizon)

            prev = QVector3D(self.xRange[-1], self.func(self.xRange[-1], z), z)
            prev = self.transform(prev)

            if curR is not None:
                self.drawHorizonLine(prev, curR, lowHorizon, highHorizon)
            curR = prev

    def check_direction(self):
        start: QVector3D = self.transform(
            QVector3D(self.xRange[0], self.func(self.xRange[0], self.zRange[0]), self.zRange[0]))
        end: QVector3D = self.transform(
            QVector3D(self.xRange[0], self.func(self.xRange[0], self.zRange[-1]), self.zRange[-1]))
        if start.z() < end.z():
            self.zRange.reverse()

    def drawHorizon(self, z, lowHorizon, highHorizon):
        prev = None
        for x in self.xRange:
            curr = QVector3D(x, self.func(x, z), z)
            curr = self.transform(curr)
            if prev is not None:
                self.drawHorizonLine(prev, curr, lowHorizon, highHorizon)
            prev = curr

    def drawHorizonLine(self, prev: QVector3D, curr: QVector3D, lowHorizon, highHorizon):
        if not self.inCanvas(prev) and not self.inCanvas(curr):
            return

        if not self.inCanvas(prev):
            prev, curr = curr, prev

        x = prev.x()
        y = prev.y()
        dx = curr.x() - prev.x()
        dy = curr.y() - prev.y()

        if abs(dx) <= self.EPS and abs(dy) <= self.EPS:
            self.drawPoint(round(x), round(y), lowHorizon, highHorizon)
            return

        l = max(abs(dx), abs(dy))
        dx /= l
        dy /= l

        while l > 0:
            ix = round(x)
            iy = round(y)
            if not self._inCanvas(x, y):
                break
            self.drawPoint(ix, iy, lowHorizon, highHorizon)
            l -= 1
            x += dx
            y += dy

    def drawPoint(self, x: int, y: int, lowHorizon, highHorizon):
        xInd = x - self.left
        if highHorizon[xInd] > y > lowHorizon[xInd]:
            return
        highHorizon[xInd] = max(y, highHorizon[xInd])
        lowHorizon[xInd] = min(y, lowHorizon[xInd])
        #self.drawPixmapPoint(QPoint(x, y), QColor(Qt.red))
        self.canvas.addLine(x, y, x, y, Qt.blue)

    def _inCanvas(self, x: float, y: float) -> bool:
        return self.left <= x <= self.right and self.top >= y >= self.bottom

    def inCanvas(self, p: QVector3D) -> bool:
        return self._inCanvas(p.x(), p.y())