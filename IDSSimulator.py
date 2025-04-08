import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QBrush

class IDSSimulator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Security+ IDS Simulator")
        self.resize(700, 500)

        self.log_display = QListWidget()
        self.log_display.setSelectionMode(QListWidget.SingleSelection)

        self.flag_button = QPushButton("Flag Selected as Suspicious")
        self.flag_button.clicked.connect(self.flag_selected_log)

        self.score_label = QLabel("Score: 0")
        self.results_label = QLabel("TP: 0 | FP: 0 | TN: 0 | FN: 0")

        layout = QVBoxLayout()
        layout.addWidget(self.log_display)
        layout.addWidget(self.flag_button)
        layout.addWidget(self.score_label)
        layout.addWidget(self.results_label)
        self.setLayout(layout)

        self.logs = [
            ("[INFO] 192.168.1.10 accessed port 22", 0),
            ("[ALERT] 10.0.0.5 sent SYN flood to 192.168.1.15", 5),
            ("[WARNING] 203.0.113.5 port scanning detected", 3),
            ("[INFO] 198.51.100.23 made DNS request for suspicious-domain.com", 4),
            ("[INFO] 192.168.1.50 failed login attempt x5", 2),
            ("[INFO] 10.1.1.1 accessed port 443", 0),
            ("[INFO] 203.0.113.99 accessed login.php", 0),
            ("[ALERT] SQL Injection attempt on login.php", 5),
            ("[INFO] 172.16.0.12 accessed port 80", 0),
            ("[INFO] Unusual outbound traffic to 47.88.22.1", 4),
            ("[INFO] Internal host 10.0.1.3 pinged 255.255.255.255", 2),
            ("[WARNING] Unexpected SMB traffic on port 445", 3),
            ("[INFO] Multiple failed SSH login attempts from 192.168.99.2", 3),
            ("[ALERT] Executable file uploaded via HTTP POST", 5),
            ("[INFO] Device 10.10.10.10 requested large volume of data from sensitive share", 4),
            ("[INFO] Host connected to blacklisted IP 185.244.25.1", 4),
            ("[INFO] Outbound traffic spike to unknown destination", 3),
            ("[INFO] ARP spoofing behavior detected on local subnet", 4),
            ("[INFO] Admin access granted to unknown user", 5),
            ("[INFO] DNS tunneling suspected from 192.0.2.1", 5)
        ]

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_next_log)
        self.timer.start(2000)

        self.displayed_logs = []
        self.score = 0

        self.true_positive = 0
        self.false_positive = 0
        self.true_negative = 0
        self.false_negative = 0

    def display_next_log(self):
        log = random.choice(self.logs)
        self.displayed_logs.append(log)
        item = QListWidgetItem(log[0])
        self.log_display.addItem(item)

    def flag_selected_log(self):
        selected_items = self.log_display.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        index = self.log_display.row(selected_item)
        if index >= len(self.displayed_logs):
            return

        log_text, severity = self.displayed_logs[index]

        if severity > 0:
            self.score += severity
            self.true_positive += 1
            selected_item.setText(f"✅ {log_text} [+{severity}]")
            selected_item.setBackground(QBrush(QColor(200, 255, 200)))  # soft green
            selected_item.setForeground(QBrush(QColor(0, 0, 0)))  # black text
        else:
            self.score -= 1
            self.false_positive += 1
            selected_item.setText(f"❌ {log_text} [-1]")
            selected_item.setBackground(QBrush(QColor(255, 200, 200)))  # soft red
            selected_item.setForeground(QBrush(QColor(0, 0, 0)))  # black text

        self.score_label.setText(f"Score: {self.score}")
        self.update_results()

    def update_results(self):
        total_flagged = self.true_positive + self.false_positive
        total_seen = len(self.displayed_logs)
        total_not_flagged = total_seen - total_flagged

        self.false_negative = sum(1 for i, log in enumerate(self.displayed_logs)
                                  if log[1] > 0 and not self.log_display.item(i).text().startswith("✅"))
        self.true_negative = sum(1 for i, log in enumerate(self.displayed_logs)
                                 if log[1] == 0 and not self.log_display.item(i).text().startswith("❌"))

        self.results_label.setText(
            f"TP: {self.true_positive} | FP: {self.false_positive} | TN: {self.true_negative} | FN: {self.false_negative}"
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IDSSimulator()
    window.show()
    sys.exit(app.exec_())
