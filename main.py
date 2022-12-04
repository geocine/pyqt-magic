from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QBoxLayout, QSpacerItem, QSizePolicy, QStackedWidget


class VerticalTabWidget(QWidget):
    def __init__(self, parent=None):
        super(VerticalTabWidget, self).__init__(parent)

        # Create the main layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        # Create a list to store the tabs
        self.tabs = []
        self.tabButtonHeight = 40

        # Create a container widget to hold the tabs
        self.tabWidget = QWidget()
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setStyleSheet(
            "#tabWidget {background-color: #2196F3;}")
        self.mainLayout.addWidget(self.tabWidget)

        # Create a vertical layout to hold the tabs
        self.tabLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self.tabLayout.setSpacing(0)
        self.tabLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.setLayout(self.tabLayout)

        # Add a spacer item to the bottom of the layout
        self.tabLayout.addSpacerItem(QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Create a stack widget to hold the pages
        self.stack = QStackedWidget()
        self.mainLayout.addWidget(self.stack)

    def addTab(self, tab, page):
        # Set the tab width and height to be the same as the tabWidget
        tab.setFixedWidth(self.tabWidget.width())
        tab.setFixedHeight(self.tabButtonHeight)
        scale = 0.7
        # Set the icon size to be the same as the tabButtonHeight
        tab.setIconSize(QSize(int(scale * self.tabWidget.width()),
                              int(scale * self.tabButtonHeight)))

        # Set the size policy of the tab to be fixed
        tab.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Add the tab and page to the list
        self.tabs.append((tab, page))

        # Add the tab to the vertical layout
        self.tabLayout.insertWidget(len(self.tabs) - 1, tab)

        # Add the page to the stack widget
        self.stack.addWidget(page)

        # Create a signal to show the page when the tab is clicked
        tab.clicked.connect(self.showPage)

        # If this is the first tab, show it
        if len(self.tabs) == 1:
            tab.selected = True
            self.stack.setCurrentIndex(0)

    def showPage(self):
        # Get the sender of the signal
        sender = self.sender()

        # Loop through the tabs and find the one that was clicked
        for i, (tab, page) in enumerate(self.tabs):
            if tab == sender:
                tab.selected = True
                # Show the page
                self.stack.setCurrentIndex(i)

                # Set the tab text to bold to indicate it is selected
                # tab.setFont(QFont("Helvetica", 12, QFont.Bold))
            else:
                tab.selected = False
                # Set the tab text to normal weight
                # tab.setFont(QFont("Helvetica", 12))

    def resizeEvent(self, event):
        # Print the size of the window to the console
        print("Window size:", self.size())

    def show(self):
        # Show the widget
        super(VerticalTabWidget, self).show()

        # Set the window size to 800x500
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)

        # Call the resizeEvent method to trigger it when the widget is shown
        self.resizeEvent(None)

    def setTabWidth(self, width):
        self.tabWidget.setFixedWidth(width)

    def setTabButtonHeight(self, height):
        self.tabButtonHeight = height


class FlatButton(QPushButton):
    def __init__(self, icon, parent=None):
        super(FlatButton, self).__init__(parent)

        # Icon is an svg file
        # Create a QPixmap object from the icon file
        pixmap = QPixmap(icon)

        # Scale the pixmap to the size of the button
        scaled_pixmap = pixmap.scaled(
            self.size(), aspectRatioMode=Qt.KeepAspectRatio)

        # Create a QIcon object from the scaled pixmap
        scaled_icon = QIcon(scaled_pixmap)

        # Set the icon of the button
        self.setIcon(scaled_icon)

        # Set the button to be flat
        self.setFlat(True)

       # Set the default value for the 'selected' property
        self._selected = False

        # Set the button's style using a CSS string
        self.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:pressed {
                background-color: #1976D2;
            }
            QPushButton:hover:!pressed[selected="false"] {
                background-color: #64B5F6;
            }
            QPushButton[selected="true"] {
                background-color: #F44336;
            }
        """)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if isinstance(value, bool):
            self._selected = value
        else:
            raise TypeError("'selected' property must be a boolean")
        self.setProperty("selected", self._selected)
        self.style().unpolish(self)
        self.style().polish(self)


if __name__ == "__main__":
    app = QApplication([])

    # Create a vertical tab widget
    tabWidget = VerticalTabWidget()
    tabWidget.setTabWidth(50)
    tabWidget.setTabButtonHeight(50)

    # Create some tabs and pages
    tab1 = FlatButton("train_model.svg")
    page1 = QWidget()
    page1.setStyleSheet("background-color: red")
    tabWidget.addTab(tab1, page1)

    tab2 = FlatButton("infer_model.svg")
    page2 = QWidget()
    page2.setStyleSheet("background-color: green")
    tabWidget.addTab(tab2, page2)

    # create a tab and page for the third tab
    tab3 = FlatButton("interrogate.svg")
    page3 = QWidget()
    page3.setStyleSheet("background-color: blue")
    tabWidget.addTab(tab3, page3)

    # create a tab and page for the fourth tab
    tab4 = FlatButton("convert.svg")
    page4 = QWidget()
    page4.setStyleSheet("background-color: yellow")
    tabWidget.addTab(tab4, page4)

    # create a tab and page for the fifth tab
    tab5 = FlatButton("settings.svg")
    page5 = QWidget()
    page5.setStyleSheet("background-color: purple")
    tabWidget.addTab(tab5, page5)

    # Show the tab widget
    tabWidget.show()

    app.exec_()
