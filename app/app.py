from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QLineEdit, QVBoxLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QDoubleValidator, QValidator
import sys
import design
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class SymbolValidator(QValidator):
    def validate(self, input_text, pos):
        for char in input_text:
            if char.isnumeric():
                return (QValidator.State.Invalid, input_text, pos)
        return (QValidator.State.Acceptable, input_text, pos)




class HistogramWindow(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle('Гистограмма по итоговой стоимости')
        self.layout = QVBoxLayout(self)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        self.close_histogram_button = QPushButton('Закрыть гистограмму', self)
        self.close_histogram_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_histogram_button)

        self.update_histogram(data)

    def update_histogram(self, data):
        self.ax.clear()

        countries, costs = zip(*data)
        self.ax.bar(countries, costs, color='green', edgecolor='black')
        self.ax.set_xlabel('Страна(город)')
        self.ax.set_ylabel('Итоговая стоимость')
        self.ax.set_title('Итоговая стоимость путешествия для стран')
        self.canvas.draw()

class App(design.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.table_travel.resizeColumnsToContents()
        self.row_in_table.clicked.connect(self.generate_table)
        self.load_in_table.clicked.connect(self.addFileDataToTable)
        self.res_cost.clicked.connect(self.itog_cost)
        self.graf_create.clicked.connect(self.create_histogram)
        self.histogram_window = None
        self.data = []

    def generate_table(self):
        self.table_travel.clear()
        row_in = self.spinBox.value()
        self.table_travel.setRowCount(row_in)
        double_validator = QDoubleValidator()
        self.table_travel.setColumnCount(5)
        sym_validator = SymbolValidator()
        columns_label = ["Страна(город) путешествия", "Стоимость билетов на транспорт", "Стоимость проживания", " Стоимость еды", "Стоимость пр. расходов"]
        self.table_travel.setHorizontalHeaderLabels(columns_label)
        for row in range(row_in):
            item = QLineEdit()
            item.setValidator(sym_validator)
            self.table_travel.setCellWidget(row, 0, item)
            for col in range(1, 5):
                item = QLineEdit()
                item.setValidator(double_validator)
                self.table_travel.setCellWidget(row, col, item)

    def addFileDataToTable(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text files (*.txt)")
        if filename:
            with open(filename, "r") as f:
                data = f.readlines()
                self.table_travel.clear()
                self.table_travel.setRowCount(len(data))
                columns_label = ["Страна(город) путешествия", "Стоимость билетов на транспорт", "Стоимость проживания", " Стоимость еды", "Стоимость пр. расходов"]
                self.table_travel.setHorizontalHeaderLabels(columns_label)
                for row, line in enumerate(data):
                    items = line.split()
                    for col, item in enumerate(items):
                        item_widget = QLineEdit()
                        if col == 0:
                            item_widget.setValidator(SymbolValidator())
                        else:
                            item_widget.setValidator(QDoubleValidator())
                        item_widget.setText(item)
                        self.table_travel.setCellWidget(row, col, item_widget)

    def itog_cost(self):
        self.data = []

        for row in range(self.table_travel.rowCount()):
            total = 0
            has_negative_value = False

            for col in range(1, 5):
                item_widget = self.table_travel.cellWidget(row, col)
                if item_widget:
                    value = item_widget.text().replace(",", ".")

                    if value:  # проверка на пустую строку
                        if "-" not in value:
                            total += float(value)
                        else:
                            has_negative_value = True

            if has_negative_value:
                QMessageBox.warning(self, "Ошибка", "Вы ввели отрицательное число")
                break

            if total != 0 and self.table_travel.cellWidget(row, 0).text() != "":
                self.table_travel.setColumnCount(6)
                self.table_travel.setHorizontalHeaderItem(5, QTableWidgetItem("Итог"))

                total_item = QLineEdit()
                total_item.setText(str(total).replace(".", ","))
                total_item.setReadOnly(True)

                self.table_travel.setCellWidget(row, 5, total_item)
                self.data.append([self.table_travel.cellWidget(row, 0).text(), total])
            else:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите данные в таблицу =_=")
                break

    def create_histogram(self):
        if not self.data:
            return

        if self.histogram_window:
            self.histogram_window.close()

        self.histogram_window = HistogramWindow(self.data)
        self.histogram_window.show()


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
