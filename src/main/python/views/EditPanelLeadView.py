from PyQt5 import QtCore, QtWidgets

from QtWrapper import *


class EditPanelLeadView(QtWidgets.QWidget):
    leadStartTimeChanged = QtCore.pyqtSignal(str, float)
    deleteLeadRoi = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()

        self.parent = parent # the editor widget

        self.leadId = None

        self.sizePolicy().setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy().setVerticalPolicy(QtWidgets.QSizePolicy.Fixed)

        self.initUI()

    def initUI(self):

        VerticalBoxLayout(owner=self, name="mainlayout", margins=(5, 5, 5, 5), contents=[
            Label(
                owner=self,
                name="title",
                text=""
            ),
            FormLayout(owner=self, name="controlsLayout", contents=[
                [
                    Label(
                        owner=self,
                        name="leadStartTimeLabel",
                        text="Start time: "
                    ),
                    DoubleSpinBox(
                        owner=self,
                        name="leadStartTimeSpinBox",
                        suffix=" sec",
                        minVal=0,
                        maxVal=1000
                    )
                ]
            ]),
            PushButton(
                owner=self,
                name="deleteLeadButton",
                text="Delete Lead"
            )
        ])

        self.mainlayout.setAlignment(QtCore.Qt.AlignTop)
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(self.mainlayout)
        self.leadStartTimeSpinBox.valueChanged.connect(lambda: self.leadStartTimeChanged.emit(self.leadId, self.leadStartTimeSpinBox.value()))
        self.deleteLeadButton.clicked.connect(lambda: self.deleteLeadRoi.emit(self.leadId))


    def setValues(self, leadId, startTime=0.0):
        self.leadId = leadId
        self.setTitle(leadId)
        self.leadStartTimeSpinBox.setValue(startTime)

    def setTitle(self, leadId):
        self.title.setText("Lead " + leadId)

    def startTimeChanged(self):
        print("start time changed: " + str(self.leadStartTimeSpinBox.value()))
        self.parent.leadStartTimeChanged.emit(self.leadId, self.leadStartTimeSpinBox.value())


class EditPanelXScaleView(QtWidgets.QWidget):
    XScalemsecChanged = QtCore.pyqtSignal(float)
    deleteXScale = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()

        self.parent = parent # the editor widget

        self.sizePolicy().setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy().setVerticalPolicy(QtWidgets.QSizePolicy.Fixed)

        self.initUI()

    def initUI(self):

        VerticalBoxLayout(owner=self, name="mainlayout", margins=(5, 5, 5, 5), contents=[
            Label(
                owner=self,
                name="title",
                text="Time Scale"
            ),
            FormLayout(owner=self, name="controlsLayout", contents=[
                [
                    Label(
                        owner=self,
                        name="XScalemsecLabel",
                        text="msec: "
                    ),
                    DoubleSpinBox(
                        owner=self,
                        name="XScalemsecSpinBox",
                        suffix=" msec",
                        minVal=0,
                        maxVal=1000
                    )
                ]
            ]),
            PushButton(
                owner=self,
                name="deleteXScaleButton",
                text="Delete X Scale"
            )
        ])

        self.mainlayout.setAlignment(QtCore.Qt.AlignTop)
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(self.mainlayout)
        self.XScalemsecSpinBox.valueChanged.connect(lambda: self.XScalemsecChanged.emit(self.XScalemsecSpinBox.value()))
        self.deleteXScaleButton.clicked.connect(lambda: self.deleteXScale.emit())


    def setValues(self, msec=200.0):
        self.setTitle("X")
        self.XScalemsecSpinBox.setValue(msec)

    def setTitle(self, leadId):
        self.title.setText("Time Scale")

    def startTimeChanged(self):
        print("start time changed: " + str(self.XScalemsecSpinBox.value()))
        self.parent.XScalemsecChanged.emit(self.XScalemsecSpinBox.value())

class EditPanelYScaleView(QtWidgets.QWidget):
    XScalemsecChanged = QtCore.pyqtSignal(float)
    deleteXScale = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()

        self.parent = parent # the editor widget

        self.sizePolicy().setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy().setVerticalPolicy(QtWidgets.QSizePolicy.Fixed)

        self.initUI()

    def initUI(self):

        VerticalBoxLayout(owner=self, name="mainlayout", margins=(5, 5, 5, 5), contents=[
            Label(
                owner=self,
                name="title",
                text=""
            ),
            FormLayout(owner=self, name="controlsLayout", contents=[
                [
                    Label(
                        owner=self,
                        name="XScalemsecLabel",
                        text="msec: "
                    ),
                    DoubleSpinBox(
                        owner=self,
                        name="XScalemsecSpinBox",
                        suffix=" msec",
                        minVal=0,
                        maxVal=1000
                    )
                ]
            ]),
            PushButton(
                owner=self,
                name="deleteXScaleButton",
                text="Delete X Scale"
            )
        ])

        self.mainlayout.setAlignment(QtCore.Qt.AlignTop)
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(self.mainlayout)
        self.XScalemsecSpinBox.valueChanged.connect(lambda: self.XScalemsecChanged.emit(self.XScalemsecSpinBox.value()))
        self.deleteXScaleButton.clicked.connect(lambda: self.deleteXScale.emit())


    def setValues(self, msec=200.0):
        self.setTitle("X")
        self.XScalemsecSpinBox.setValue(msec)

    def setTitle(self, leadId):
        self.title.setText("Time Scale")

    def startTimeChanged(self):
        print("start time changed: " + str(self.XScalemsecSpinBox.value()))
        self.parent.XScalemsecChanged.emit(self.XScalemsecSpinBox.value())
