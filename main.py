import sys
from PyQt5.QtWidgets import QApplication
import kiltis
import visualisointi


def main():
    kilta = kiltis.Kiltis()

    global app
    app = QApplication(sys.argv)
    gui = visualisointi.Window(kilta)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
