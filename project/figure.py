from project import UI
from project.common import *
import matplotlib

import tkinter.messagebox
from tkinter import *
from datetime import datetime
import matplotlib.pyplot as plt
from project.randomData import get_data
from PyQt5.QtWidgets import *
import json

matplotlib.use("Qt5Agg")  # Declare the use of QT5


class MainDialogImgBW(QMainWindow, UI.Ui_MainWindow):
    """
    A window to inform the user and allow the user to select an answer.
    """
    def __init__(self):
        # create  manDialog windows
        super(MainDialogImgBW, self).__init__()
        # init ui
        self.setupUi(self)
        self.setWindowTitle("Main Window")
        self.setMinimumSize(0, 0)

        # init params
        # init current trail
        self.curStep = 0
        # paths data
        self.pathData = get_data()
        # answer result
        self.answerData = []

        # initialization
        self.lastTime = datetime.now()
        self.last_image_type = ''
        self.last_color = ''
        self.last_target_name = ''
        self.last_target_value = ''
        self.last_data = {}

        # add answer list
        self.comboBox.addItems(PATH)
        # reset comboBox select
        self.comboBox.setCurrentIndex(-1)
        # bind trigger event
        self.pushButton.clicked.connect(self.nextClick)
        self.pushButton_2.clicked.connect(self.start)

        # set color
        self.color_list = DIFFERENT_COLORS
        self.color_list2 = SAME_COLORS

    def draw_bar(self, x, y, color):
        """
        Plotting a bar chart based on incoming X, Y and color
        :param x: path way list
        :param y: path cost
        :param color: column color  can be null
        :return:
        """
        plt.figure(figsize=(12, 8), dpi=100)
        plt.title('The cost of patients choosing different pathways')
        if color is None:
            plt.barh(x, y, color=color)
            plt.yticks(x, None, fontsize=8)
        else:
            for i in range(11):
                plt.barh(x[i], y[i], color=self.color_list[i])
                plt.yticks([], None, fontsize=8)
                plt.legend(x, ncol=2, loc="best", fontsize=10, bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.show()

    # column chart
    def draw_column(self, x, y, color):
        """
        Plotting a column chart based on incoming X, Y and color
        :param x: path way list
        :param y: path cost
        :param color: column color    can be null
        :return:
        """
        plt.figure(figsize=(12, 8), dpi=100)
        plt.title('The cost of patients choosing different pathways')
        if color is None:
            plt.bar(x, y)
            plt.xticks(x, None, rotation=45, fontsize=8)
        else:
            for i in range(11):
                plt.bar(x[i], y[i], color=self.color_list[i])
                plt.xticks([], None, rotation=45, fontsize=8)
                plt.legend(x, ncol=2, loc="best", fontsize=10, bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.show()

    def draw_pie(self, x, y, colors):
        """
        Draws a pie chart of the specified color based on the incoming X, Y. Hide labels
        :param x:
        :param y:
        :param color:
        :return:
        """
        plt.figure(figsize=(12, 8), dpi=100)
        plt.title('The cost of a single path as a percentage of the cost of 11 paths')
        plt.pie(y, labels=None, colors=colors)
        plt.legend(x, loc="best", fontsize=10, bbox_to_anchor=(0.1, 1))
        plt.show()
        plt.tight_layout()

    def draw_pie2(self, x, y, colors):
        """
        Draws a pie chart of the specified color based on the incoming X, Y.     No hidden labels.
        :param x:
        :param y:
        :param colors:
        :return:
        """
        plt.figure(figsize=(12, 8), dpi=100)
        plt.title('The cost of a single path as a percentage of the cost of 11 paths')
        plt.pie(y, labels=x, colors=colors, wedgeprops={'linewidth': 3, "edgecolor": "black"})
        plt.show()
        plt.tight_layout()

    def start(self):
        """
        Start Button: Initialize the current image, path, color and other information.
        :return:
        """
        if self.curStep > 0:
            tkinter.messagebox.showinfo("Remind", "The experiment has already started.")
            return

        # initialization
        self.lastTime = datetime.now()
        self.last_image_type = self.pathData[self.curStep].get("image_type")
        self.last_color = self.pathData[self.curStep].get("color")
        self.last_target_name = self.pathData[self.curStep].get("target_name")
        self.last_target_value = self.pathData[self.curStep].get("target_value")
        self.last_data = self.pathData[self.curStep]

        image_type = self.pathData[self.curStep].get("image_type")
        color = self.pathData[self.curStep].get("color")

        x = []
        y = []

        # Traverse the data to prepare drawing data.
        for item in self.pathData[self.curStep].get("data"):
            name = item.get("name")
            value = item.get("value")
            x.append(name)
            y.append(value)

        # Draw charts according to preset parameters.
        self.draw(image_type, color, x, y)

        # Reset the selection box.
        self.comboBox.clear()
        self.comboBox.clearEditText()

        # Add collection of answers.
        self.comboBox.addItems(PATH)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.setCurrentText('')

        self.curStep += 1

    # Next
    def nextClick(self):
        """
        Switch to the next question.
        :return:
        """
        if self.curStep == 0:
            tkinter.messagebox.showinfo("Remind", "Please click start.")
            return

        # Check if the answer is selected
        if self.comboBox.currentIndex() == -1 and len(self.comboBox.currentText()) == 0:
            tkinter.messagebox.showinfo("Remind", "Please select an answer.")
            return

        last_time = self.lastTime
        now = datetime.now()
        duration = (now - last_time).seconds

        select = self.comboBox.currentText()

        if select == self.last_target_name:
            result = 'right'
        else:
            result = 'wrong'

        if self.last_target_value == 660 and self.last_image_type == 'column' and self.last_color == 'text':
            condition = 1
        if self.last_target_value == 1200 and self.last_image_type == 'column' and self.last_color == 'text':
            condition = 2
        if self.last_target_value == 660 and self.last_image_type == 'column' and self.last_color == 'color':
            condition = 3
        if self.last_target_value == 1200 and self.last_image_type == 'column' and self.last_color == 'color':
            condition = 4
        if self.last_target_value == 660 and self.last_image_type == 'bar' and self.last_color == 'text':
            condition = 5
        if self.last_target_value == 1200 and self.last_image_type == 'bar' and self.last_color == 'text':
            condition = 6
        if self.last_target_value == 660 and self.last_image_type == 'bar' and self.last_color == 'color':
            condition = 7
        if self.last_target_value == 1200 and self.last_image_type == 'bar' and self.last_color == 'color':
            condition = 8
        if self.last_target_value == 660 and self.last_image_type == 'pie' and self.last_color == 'none':
            condition = 9
        if self.last_target_value == 1200 and self.last_image_type == 'pie' and self.last_color == 'none':
            condition = 10
        if self.last_target_value == 660 and self.last_image_type == 'pie' and self.last_color == 'color':
            condition = 11
        if self.last_target_value == 1200 and self.last_image_type == 'pie' and self.last_color == 'color':
            condition = 12

        answer = {
            'condition': condition,
            'duration': duration,
            'result': result,
            'customer_select': select,
            'last_target_name': self.last_target_name,
            'last_target_value': self.last_target_value,
            'last_image_type': self.last_image_type,
            'last_color': self.last_color,
            'last_data': self.last_data
        }
        self.answerData.append(answer)

        if self.curStep < len(self.pathData):
            self.lastTime = datetime.now()
            self.last_image_type = self.pathData[self.curStep].get("image_type")
            self.last_color = self.pathData[self.curStep].get("color")
            self.last_target_name = self.pathData[self.curStep].get("target_name")
            self.last_target_value = self.pathData[self.curStep].get("target_value")
            self.last_data = self.pathData[self.curStep]

            image_type = self.pathData[self.curStep].get("image_type")
            color = self.pathData[self.curStep].get("color")

            x = []
            y = []

            for item in self.pathData[self.curStep].get("data"):
                name = item.get("name")
                value = item.get("value")
                x.append(name)

                y.append(value)

            self.curStep += 1

            self.draw(image_type, color, x, y)

            # add answer
            self.comboBox.clear()
            self.comboBox.clearEditText()
            self.comboBox.addItems(PATH)
            self.comboBox.setCurrentIndex(-1)
            self.comboBox.setCurrentText('')
        else:
            tkinter.messagebox.askyesno("Thanks", "The experiment is complete, thanks for participating.")
            # Convert the test results into json and store them in a local file.
            answer_data = json.dumps(self.answerData)
            # Write the local txt file with time name.
            txt = "./answer" + str(datetime.now()) + ".txt"
            file = open(txt, 'w')
            file.write(answer_data)
            file.close()

    # draw charts
    def draw(self, image_type, color, x, y):
        """
        According to the type and color to draw the customized graphics.
        :param image_type: type of chart
        :param color: color
        :param x: path
        :param y: cost of path
        :return:
        """
        if image_type == "bar":
            if color == 'color':
                self.draw_bar(x, y, self.color_list)
            else:
                self.draw_bar(x, y, None)
        if image_type == "column":
            if color == 'color':
                self.draw_column(x, y, self.color_list)
            else:
                self.draw_column(x, y, None)
        if image_type == "pie":
            if color == "color":
                self.draw_pie(x, y, self.color_list)
            else:
                self.draw_pie2(x, y, self.color_list2)


if __name__ == "__main__":

    tk = Tk()
    tk.withdraw()

    askyesno = tkinter.messagebox.askyesno("Hi", "Please make sure you have informed consent.")
    if askyesno:
        app = QApplication(sys.argv)
        main = MainDialogImgBW()
        main.show()
        sys.exit(app.exec_())
    else:
        tkinter.messagebox.showinfo("Bye", "Have a good day.")
        sys.exc_info()
