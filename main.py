"""
Nama    : Cindy Natasya Aulia Putri
NIM     : F1D02310109
Kelas   : C
"""

import sys

from PySide6.QtWidgets import QApplication

from dashboard_window import DashboardWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())