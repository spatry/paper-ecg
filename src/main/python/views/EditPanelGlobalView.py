from PyQt5 import QtCore, QtWidgets

from QtWrapper import *


class EditPanelGlobalView(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()

        self.editorWidget = parent

        self.sizePolicy().setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy().setVerticalPolicy(QtWidgets.QSizePolicy.Fixed)

        self.initUI()
        self.connectUI()

    def initUI(self):

        VerticalBoxLayout(owner=self, name="mainLayout", margins=(5, 5, 5, 5), contents=[
            GroupBox(owner=self, name="adjustmentsGroup", title="Image Adjustments", layout=
                VerticalBoxLayout(owner=self, name="adjustmentsGroupLayout", contents=[
                    Label("Brightness"),
                    HorizontalSlider(self, "brightnessSlider"),
                    Label("Contrast"),
                    HorizontalSlider(self, "contrastSlider"),
                    Label("Rotation"),
                    HorizontalSlider(self, "rotationSlider"),
                    PushButton(self, "autoRotateButton", text="Auto Rotate")
                ])
            ),
            FormLayout(owner=self, name="controlsLayout", contents=[
                [
                    Label(
                        owner=self,
                        name="timeScaleLabel",
                        text="Time Scale: "
                    ),
                    DoubleSpinBox(
                        owner=self,
                        name="timeScaleSpinBox",
                        minVal=0.01,
                        maxVal=1000.0,
                        suffix=" mm/s"
                    )
                ],
                [
                    Label(
                        owner=self,
                        name="voltScaleLabel",
                        text="Voltage Scale: "
                    ),
                    DoubleSpinBox(
                        owner=self,
                        name="voltScaleSpinBox",
                        minVal=0.01,
                        maxVal=1000.0,
                        suffix=" mm/mV"
                    )
                ]
            ]),
            PushButton(
                owner=self, 
                name="processDataButton", 
                text="Process Lead Data"
            )
        ])

        self.mainLayout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.setLayout(self.mainLayout)

        self.clearTimeSpinBox()
        self.clearVoltSpinBox()


    def connectUI(self):
        # Image editing controls
        self.brightnessSlider.sliderReleased.connect(self.editorWidget.adjustBrightness)
        self.brightnessSlider.sliderMoved.connect(self.editorWidget.adjustBrightness)
        self.brightnessSlider.setRange(-127,127)

        self.contrastSlider.sliderReleased.connect(self.editorWidget.adjustContrast)
        self.contrastSlider.sliderMoved.connect(self.editorWidget.adjustContrast)
        self.contrastSlider.setRange(-127,127)

        self.rotationSlider.sliderReleased.connect(self.editorWidget.adjustRotation)
        self.rotationSlider.sliderMoved.connect(self.editorWidget.adjustRotation)
        self.rotationSlider.setRange(-15 * 10, 15 * 10)

        self.autoRotateButton.clicked.connect(self.editorWidget.autoRotate)

        self.voltScaleSpinBox.valueChanged.connect(lambda: self.editorWidget.gridVoltScaleChanged.emit(self.voltScaleSpinBox.value()))
        self.timeScaleSpinBox.valueChanged.connect(lambda: self.editorWidget.gridTimeScaleChanged.emit(self.timeScaleSpinBox.value()))
        self.processDataButton.clicked.connect(lambda: self.editorWidget.processDataButtonClicked.emit())


    def clearVoltSpinBox(self):
        self.voltScaleSpinBox.setValue(1.0)

    def clearTimeSpinBox(self):
        self.timeScaleSpinBox.setValue(1.0)

    def setValues(self, voltScale, timeScale):
        self.voltScaleSpinBox.setValue(voltScale)
        self.timeScaleSpinBox.setValue(timeScale)
