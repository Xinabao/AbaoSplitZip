"""
AbaoZip 入口
启动画面先于主窗口显示，掩盖 Python/Qt 的加载延迟
"""

import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPainter
from PyQt5.QtWidgets import QApplication, QSplashScreen


class AbaoSplash(QSplashScreen):
    """纯代码绘制的启动画面，不依赖外部图片"""

    def __init__(self):
        from PyQt5.QtGui import QPixmap
        pixmap = QPixmap(380, 200)
        pixmap.fill(QColor("#0078d4"))
        super().__init__(pixmap)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def drawContents(self, painter: QPainter):
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Microsoft YaHei UI", 22, QFont.Bold))
        painter.drawText(self.rect().adjusted(0, 30, 0, -40),
                         Qt.AlignCenter, "AbaoZip")
        painter.setFont(QFont("Microsoft YaHei UI", 10))
        painter.drawText(self.rect().adjusted(0, 40, 0, 0),
                         Qt.AlignCenter, "分卷独立解压打包工具")
        painter.setFont(QFont("Microsoft YaHei UI", 9))
        painter.setPen(QColor(255, 255, 255, 160))
        painter.drawText(self.rect().adjusted(0, 80, 0, 0),
                         Qt.AlignCenter, "正在加载...")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    splash = AbaoSplash()
    splash.show()
    app.processEvents()

    # 延迟导入主窗口，让启动画面先显示
    from gui.main_window import MainWindow

    window = MainWindow()

    def show_main():
        window.show()
        splash.finish(window)

    QTimer.singleShot(300, show_main)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
