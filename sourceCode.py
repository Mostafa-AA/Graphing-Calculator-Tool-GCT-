import csv
import sys
import numpy as np
import pyqtgraph as pg
from PySide2.QtGui import *
from PySide2.QtWidgets import *

xx_list = []
yy_list = []


def remove_spacing(string):
    string_no_spacing = ""
    for l in string:
        if l not in " ":
            string_no_spacing = string_no_spacing + l
        else:
            continue
    return string_no_spacing


def extract_terms(fun):
    fun = remove_spacing(fun)
    if fun[0] != "-":
        fun = "+" + fun
    fun = fun + "+"
    ret_ = []
    i_c = 0
    while i_c in range(len(fun) - 1):
        temp = ""
        if fun[i_c] == "+":
            i_c = i_c + 1
            temp = temp + "+"
            while fun[i_c] not in "+-":
                temp = temp + fun[i_c]
                i_c = i_c + 1
            i_c = i_c - 1
            ret_.append(temp)
        elif fun[i_c] == "-":
            i_c = i_c + 1
            temp = temp + "-"
            while fun[i_c] not in "+-":
                temp = temp + fun[i_c]
                i_c = i_c + 1
            i_c = i_c - 1
            ret_.append(temp)
        i_c = i_c + 1
    for r in range(len(ret_)):
        ret_[r] = ret_[r].replace("sin", "np.sin")
        ret_[r] = ret_[r].replace("exp", "np.exp")
        ret_[r] = ret_[r].replace("cos", "np.cos")
        ret_[r] = ret_[r].replace("tan", "np.tan")
        ret_[r] = ret_[r].replace("cosec", "np.arcsin")
        ret_[r] = ret_[r].replace("cot", "np.arctan")
        ret_[r] = ret_[r].replace("sec", "np.arccos")
        ret_[r] = ret_[r].replace("cos_h", "np.cosh")
        ret_[r] = ret_[r].replace("sin_h", "np.sinh")
        ret_[r] = ret_[r].replace("tan_h", "np.tanh")
        ret_[r] = ret_[r].replace("sqrt", "np.sqrt")
        ret_[r] = ret_[r].replace("arccos_h", "np.arccosh")
        ret_[r] = ret_[r].replace("arcsin_h", "np.arcsinh")
        ret_[r] = ret_[r].replace("arctan_h", "np.arctanh")
        if ret_[r].find("^") != -1:
            ret_[r] = ret_[r].replace("x^", "pow(x,")
            ret_[r] = ret_[r] + ")"
    ret_1 = ""
    for el in ret_:
        ret_1 = ret_1 + el
    ret_1 = ret_1.replace("+", "", 1)
    return ret_1


def create_x_range(min_, max_, step_):
    x_range = []
    x_ = min_
    while min_ <= x_ <= max_:
        x_range.append(x_)
        x_ = x_ + step_
    return x_range


def create_y_range(fun, x_List):
    y_list = []
    for el in x_List:
        x = el
        y = eval(fun)
        y_list.append(y)
    return y_list


def plot():
    read_file = open("History.txt", "r")
    rtx = read_file.readlines()
    try:
        in_put = rtx[0]
        in_put = in_put.replace("\n", "")
        mini = float(rtx[1])
        maxi = float(rtx[2])
        step = float(rtx[3])
        step = abs(step)
        if step == 0:
            step = 0.01
    except:
        return 1

    try:
        funct_ = extract_terms(in_put)
        global xx_list
        global yy_list
        xx_list = create_x_range(mini, maxi, step)
        yy_list = create_y_range(funct_, xx_list)
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'b')
        pg.plot(xx_list, yy_list, pen=(255, 0, 0))

        return 3
    except:
        return 2


def Export():
    data = [['x', 'y']]
    for i in range(len(xx_list)):
        lis = [xx_list[i], yy_list[i]]
        data.append(lis)
    file = open('Data.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(data)


class Main_window(QMainWindow):

    def __init__(self, parent=None):
        super(Main_window, self).__init__(parent)
        self.setWindowTitle("  Graphing Calculator Tool (GCT)")
        self.setWindowIcon(QIcon(".img\\ICON.png"))
        self.setGeometry(200, 100, 395, 400)
        self.icon_modes()
        self.setFixedHeight(400)
        self.setFixedWidth(395)
        # Create widgets
        self.function = QLineEdit("Enter function in X", self)
        self.function.move(80, 50)
        self.function.setFixedWidth(290)
        self.label = QLabel("Function: ", self)
        self.label.move(25, 50)
        self.label = QLabel("X-Range: ", self)
        self.label.move(25, 100)
        self.min_box = QLineEdit("Min", self)
        self.min_box.move(80, 100)
        self.min_box.setFixedWidth(104)
        self.label = QLabel("to", self)
        self.label.move(191, 100)
        self.max_box = QLineEdit("Max", self)
        self.max_box.move(210, 100)
        self.max_box.setFixedWidth(104)
        self.label = QLabel("Step size: ", self)
        self.label.move(25, 150)
        self.step_box = QLineEdit("", self)
        self.step_box.move(80, 150)
        self.step_box.setFixedWidth(104)
        self.log_out = QLineEdit("", self)
        self.log_out.move(210, 150)
        self.log_out.setFixedWidth(160)
        self.log_out.setDisabled(True)
        tex = ">>Enter valid inputs,Press Enter,Press Plot for plotting,Check Help..."
        self.log_box = QLineEdit(tex, self)
        self.log_box.move(25, 295)
        self.log_box.setFixedWidth(346)
        self.log_box.setFixedHeight(50)
        self.header = QLabel("GCT® GRAPHING ", self)
        self.header.setFont(QFont('Times', 7))
        self.header.move(200, 10)
        self.header2 = QLabel("CALCULATOR TOOL... ", self)
        self.header2.setFont(QFont('Times', 7))
        self.header2.move(275, 10)
        # ---------------------------------------------------
        self.Enter_button = QPushButton("Enter", self)
        self.Enter_button.move(25, 200)
        self.Enter_button.setFixedWidth(160)
        self.Exit_button = QPushButton("Exit", self)
        self.Exit_button.move(270, 360)
        self.helpButton = QPushButton("Help", self)
        self.helpButton.move(147, 360)
        self.aboutButton = QPushButton("About", self)
        self.aboutButton.move(25, 360)
        self.Evaluate_button = QPushButton("Plot", self)
        self.Evaluate_button.move(210, 200)
        self.Evaluate_button.setFixedWidth(160)
        self.Evaluate_button.setEnabled(False)
        self.Export_button = QPushButton("Export data in CSV file", self)
        self.Export_button.move(25, 250)
        self.Export_button.setFixedWidth(346)
        self.Export_button.setEnabled(False)

        # Create layout and add widgets
        # layout = QVBoxLayout()
        # layout.addWidget(self.Enter_button)
        # layout.addWidget(self.button)
        # layout.addWidget(self.Exit_button)
        # Set dialog layout
        # self.setLayout(layout)
        # Add button signal to greetings slot
        self.Enter_button.clicked.connect(self.return_inputText)
        self.Exit_button.clicked.connect(self.ExitApp)
        self.aboutButton.clicked.connect(self.AboutApp)
        self.helpButton.clicked.connect(self.HelpApp)
        self.Evaluate_button.clicked.connect(self.error_detect)
        self.Export_button.clicked.connect(Export)
        self.succ_message = QLabel(self)
        self.succ_message.setText("<font color='blue'>*Ready to plot</font>")
        self.succ_message.move(256, 150)

    def return_inputText(self):
        flag = 1
        flag_ = 1
        write_ = open("History.txt", "w")
        text_ = ["", "", "", ""]
        text_[0] = text_[0] + self.function.text() + "\n"
        text_[1] = text_[1] + self.min_box.text() + "\n"
        text_[2] = text_[2] + self.max_box.text() + "\n"
        text_[3] = text_[3] + self.step_box.text() + "\n"
        try:
            if float(text_[3]) <= 0:
                flag_ = 0
                self.succ_message.clear()
                self.succ_message.setText("<font color='orange'>*Warning...</font>")
                self.succ_message.show()
                QMessageBox.warning(self, "Warning",
                                    "Negative or zero step size is illegal\nstep size is set by default value")

        except:
            flag = 0
            self.succ_message.clear()
            self.succ_message.setText("<font color='red'>*Invalid input...</font>")
            self.succ_message.show()
            self.Evaluate_button.setEnabled(False)
            self.Export_button.setEnabled(False)
            QMessageBox.critical(self, ' ERROR', 'Invalid step size input', QMessageBox.StandardButton.Abort)
        try:
            if float(text_[2]) < float(text_[1]):
                flag = 0
                self.succ_message.clear()
                self.succ_message.setText("<font color='red'>*Invalid input...</font>")
                self.succ_message.show()
                QMessageBox.critical(self, ' ERROR', 'Invalid X-Range input\nMin value is larger than Max value', QMessageBox.StandardButton.Abort)
                self.Evaluate_button.setEnabled(False)
                self.Export_button.setEnabled(False)

        except:
            flag = 0
            self.succ_message.clear()
            self.succ_message.setText("<font color='red'>*Invalid input...</font>")
            self.succ_message.show()
            QMessageBox.critical(self, ' ERROR', 'Invalid X-Range input', QMessageBox.StandardButton.Abort)
            self.Evaluate_button.setEnabled(False)
            self.Export_button.setEnabled(False)
        write_.writelines(text_)
        if flag == 1:
            if flag_ == 1:
                self.succ_message.clear()
                self.succ_message.setText("<font color='blue'>*Click plot</font>")
                self.succ_message.show()
            self.Evaluate_button.setEnabled(True)

    def ExitApp(self):
        userInput = QMessageBox.question(self, "  Confirm Exit", "Are you sure want to exit GCT ?",
                                         QMessageBox.Yes | QMessageBox.No)
        if userInput == QMessageBox.Yes:
            app.quit()
        elif userInput == QMessageBox.No:
            pass

    def AboutApp(self):
        text = "GCT 2020. 1.0v (Free version) \nGCT is a garphical calculator tool which is used in visualizing " \
               "functions.\nCreated by: M.A.A "
        QMessageBox.about(self, " About GCT", text)

    def HelpApp(self):
        text = "*Steps:\n1) Enter a function in x\n2) Enter the min and max values of x\n3) Enter step size which must be larger than zero\n4) Click on Enter to confirm your inputs\n5) Click on plot to plot input function with x-axis\n\n*GCT supports polynomials, trigonmetric, hyberbolic and exponential functions.\n\n*GCT supports only x as an idependant variable.\n\n*The inputs are stored in a txt file with name (History.txt)\n\n*To export data points in CSV file, Click on Export Button and the exported file will be found in App`s directory with name (Data.csv)\n\n"
        QMessageBox.information(self, " Help", text)

    def error_detect(self):
        fr = plot()
        if fr == 1:
            pass
        elif fr == 2:
            self.succ_message.clear()
            self.succ_message.setText("<font color='red'>*Invalid input...</font>")
            self.succ_message.show()
            self.Evaluate_button.setEnabled(False)
            self.Export_button.setEnabled(False)
            QMessageBox.critical(self, ' ERROR', 'Invalid input function\nPlease check help', QMessageBox.StandardButton.Abort)
        elif fr == 3:
            self.Export_button.setEnabled(True)
            self.succ_message.clear()
            self.succ_message.setText("<font color='green'>*Successfully...</font>")
            self.succ_message.move(250,150)
            self.succ_message.show()

    def icon_modes(self):
        icon = QIcon(".img\\logo_size_invert.jpg")
        label1 = QLabel('sample', self)
        pixmap = icon.pixmap(150, 25, QIcon.Active, QIcon.On)
        label1.setPixmap(pixmap)
        label1.setToolTip("Graphing Calculator Tool")
        label1.move(80, 10)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    Window = Main_window()
    Window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
