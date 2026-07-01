#!/usr/bin/env python

import rospy
from papillarray_ros_v2.msg import SensorState # Assumes PillarState is inside this or imported
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject

class CommSignal(QObject):
    # This signal will carry the full list of 18 booleans to the UI thread
    refresh_all = pyqtSignal(list)

class MatrixGUI(QWidget):
    def __init__(self):
        super(MatrixGUI, self).__init__()
        # State storage for 18 pillars (9 for sensor_0, 9 for sensor_1)
        self.contacts = [False] * 18
        
        self.initUI()
        
        # ROS Signal Setup
        self.sig = CommSignal()
        self.sig.refresh_all.connect(self.update_all_cells)
        
        rospy.init_node('matrix_gui_node', anonymous=True)
        
        # Subscribers
        rospy.Subscriber("/hub_0/sensor_0", SensorState, self.callback_0)
        rospy.Subscriber("/hub_0/sensor_1", SensorState, self.callback_1)

    def initUI(self):
        main_layout = QHBoxLayout()
        self.all_cells = []

        main_layout.addLayout(self.create_matrix_layout("Sensor 0"))
        main_layout.addSpacing(40)
        main_layout.addLayout(self.create_matrix_layout("Sensor 1"))

        self.setLayout(main_layout)
        self.setWindowTitle('PapillArray Tactile Monitor')
        self.setStyleSheet("background-color: #1e1e1e;")
        self.show()

    def create_matrix_layout(self, title):
        container = QVBoxLayout()
        # Optional: Add a title label here if you want
        grid = QGridLayout()
        for i in range(9):
            cell = QLabel()
            cell.setFixedSize(50, 50)
            cell.setStyleSheet("background-color: white; border-radius: 25px; border: 2px solid #555;")
            grid.addWidget(cell, i // 3, i % 3)
            self.all_cells.append(cell)
        container.addLayout(grid)
        return container

    def callback_0(self, msg):
        # Update first 9 elements
        for i, pillar in enumerate(msg.pillars[:9]):
            self.contacts[i] = pillar.in_contact
        # Tell the UI to update using the current state of self.contacts
        self.sig.refresh_all.emit(list(self.contacts))

    def callback_1(self, msg):
        # Update last 9 elements (index 9 to 17)
        for i, pillar in enumerate(msg.pillars[:9]):
            self.contacts[i+9] = pillar.in_contact
        # Tell the UI to update
        self.sig.refresh_all.emit(list(self.contacts))

    def update_all_cells(self, data_list):
        # This runs in the Main Thread (Qt Thread)
        for i in range(18):
            color = "#ff4444" if data_list[i] else "white"
            self.all_cells[i].setStyleSheet(
                f"background-color: {color}; border-radius: 25px; border: 2px solid #333;"
            )

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = MatrixGUI()
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())