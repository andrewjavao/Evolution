import sys, random, thread,time
from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from PyQt5 import QtGui

# locks ---------------
PAINT_LOCK = thread.allocate_lock()

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Points')
        self.show()

    def paintEvent(self, e):
        #PAINT_LOCK.acquire()

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

        #PAINT_LOCK.release()

    def drawPoints(self, qp):
        qp.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0)))
        size = self.size()
        for i in range(1000):
            x = random.randint(1, size.width()-1)
            y = random.randint(1, size.height()-1)
            qp.drawRect(x, y, 3, 3)


def repaint_repeat(ex, interval):
    while(True):
        ex.update()

        time.sleep(interval)

    thread.exit_thread()

app = QApplication(sys.argv)

ex = Example()

thread.start_new_thread(repaint_repeat, (ex, 0.04))
#window = QDialog()
#window.show()

sys.exit(app.exec_())