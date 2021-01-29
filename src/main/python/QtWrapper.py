"""
QtWrapper.py
Created November 7, 2020

Wrapper to simplify interacting with Qt
"""

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QAction, QGroupBox, QHBoxLayout, QLayout, QMenu, QMenuBar, QMainWindow, QPushButton, QRadioButton, QSizePolicy, QSlider, QSplitter, QVBoxLayout, QWidget

from typing import cast, List, Optional, Tuple, Union


class IncompatibleFunction(Exception):
    """Thrown when a decorated function is incompatible with the decorator."""
    pass


def bindsToClass(createWidgetFunction):
    """
    Decorator for binding a created widget to the owner using the given name.
    Decorated functions must have the first 2 parameters: (owner, name, ...).

    Example:
        @bindsToClass
        def createWidget(owner, name, other, parameters)
            pass

        class Window():
            def __init__(self):
                createWidget(self, "example", foo, bar)
                print(self.example)
    """
    def createAndBind(*args, **kwargs):
        # Try to extract the `owner` and `name` parameters
        if "owner" in kwargs and "name" in kwargs:
            owner, name = kwargs["owner"], kwargs["name"]
        elif len(args) == 1 and "name" in kwargs:
            owner, name = args[0], kwargs["name"]
        elif len(args) >= 2:
            owner, name = args[:2]
        else:
            # If `owner` and `name` can't be found, just throw an
            # error to explain what happened
            raise IncompatibleFunction(f"Function '{createWidgetFunction.__name__}' missing 'owner' and 'name' parameters required by @bindsToClass decorator.")

        # Create the widget by calling the decorated function
        widget = createWidgetFunction(*args, **kwargs)

        if owner is not None and name is not None and name != "":
            # Set `owner.name = widget` so the owner class is able to access the widget
            setattr(owner, name, widget)

        return widget

    return createAndBind


@bindsToClass
def MenuAction(owner: QWidget, name:str, displayName:str, shortcut:Optional[Union[str, QtGui.QKeySequence]], statusTip: Optional[str]) -> QAction:
    """Creates a MenuAction

    Args:
        owner (QWidget): The class to which the Menu property will be added
        name (str): The property name of the Menu in the class (not seen by users)
        displayName (str): The name displayed to the user in the menu list for this action
        shortcut (Union[str, QtGui.QKeySequence]): The keyboard shortcut to trigger the action
        statusTip (str): ???
    """
    action = QAction('&' + displayName, owner) # In this case the owner is the main window
    if shortcut:
        action.setShortcut(shortcut)
    if statusTip:
        action.setStatusTip(statusTip)

    return action


class Separator():
    """A dummy type to represent a menu separator
    """
    pass


@bindsToClass
def Menu(owner: QWidget, name:str, displayName:str, items:List[Union[QAction, Separator]]) -> QMenu:
    """Creates a QMenu

    Args:
        owner (QWidget): The class to which the Menu property will be added
        name (str): The property name of the Menu in the class (not seen by users)
        displayName (str): The Menu name displayed to the user
        items (List[Union[QAction, Separator]]): Items to display in the menu

    Returns:
        QMenu: Menu
    """
    menu = QMenu(displayName) # In this case the `owner` is the main window
    for item in items:
        if type(item) is Separator: menu.addSeparator()
        # Cast `item` : `Union[QAction, Separator] -> QAction` for mypy
        elif type(item) is QAction: menu.addAction(cast(QAction, item))

    return menu


@bindsToClass
def MenuBar(owner: QMainWindow, name:str, menus: List[QMenu]) -> QMenuBar:
    """Creates a QMenuBar

    Args:
        owner (QMainWindow): The MainWindow to which the MenuBar will be added
        name (str): The name of the MenuBar property
        menus (List[QMenu]): Menus container in the MenuBar

    Returns:
        QMenuBar: The menubar created
    """
    # In this case the `owner` is the main window
    menuBar = owner.menuBar() # type: QMenuBar
    for menu in menus:
        menuBar.addMenu(menu)

    return menuBar


@bindsToClass
def VerticalBoxLayout(
    owner: QWidget,
    name:str,
    margins: Optional[Tuple[int, int, int, int]]=None,
    contents: List[Union[QWidget, QLayout]]=[]
) -> QVBoxLayout:
    """[summary]

    Args:
        owner (QWidget): The class to which the property will be added
        name (str): The property name of the created object in the class (not seen by users)
        margins (Tuple[int, int, int, int]): left, top, right, bottom
        contents (List[Union[QWidget, QLayout]])

    Returns:
        QVBoxLayout
    """
    verticalBoxLayout = QVBoxLayout()

    if margins is not None:
        left, top, right, bottom = margins
        verticalBoxLayout.setContentsMargins(left, top, right, bottom)

    for item in contents:
        if issubclass(type(item), QWidget):
            verticalBoxLayout.addWidget(cast(QWidget, item))
        elif issubclass(type(item), QLayout):
            verticalBoxLayout.addLayout(cast(QLayout, item))

    return verticalBoxLayout


@bindsToClass
def HorizontalBoxLayout(
    owner: QWidget,
    name:str,
    margins: Optional[Tuple[int, int, int, int]]=None,
    contents: List[Union[QWidget, QLayout]]=[]
) -> QHBoxLayout:
    """[summary]

    Args:
        owner (QWidget): The class to which the property will be added
        name (str): The property name of the created object in the class (not seen by users)
        margins (Tuple[int, int, int, int]): left, top, right, bottom
        contents (List[Union[QWidget, QLayout]])

    Returns:
        QVBoxLayout
    """
    horizontalBoxLayout = QHBoxLayout()

    if margins is not None:
        left, top, right, bottom = margins
        horizontalBoxLayout.setContentsMargins(left, top, right, bottom)

    for item in contents:
        if issubclass(type(item), QWidget):
            horizontalBoxLayout.addWidget(cast(QWidget, item))
        elif issubclass(type(item), QLayout):
            horizontalBoxLayout.addLayout(cast(QLayout, item))

    return horizontalBoxLayout


@bindsToClass
def GroupBox(
    owner: QWidget,
    name:str,
    title:str, # Shown to user
    layout: QLayout
) -> QGroupBox:
    horizontalBoxLayout = QGroupBox(title)
    horizontalBoxLayout.setLayout(layout)

    return horizontalBoxLayout


@bindsToClass
def RadioButton(owner: QWidget, name: str, text:str) -> QRadioButton:
    return QRadioButton(text)


@bindsToClass
def PushButton(owner: QWidget, name: str, icon:Optional[QtGui.QIcon]=None, text:str="") -> QPushButton:
    if icon is not None:
        button = QPushButton(icon, text)
    else:
        button = QPushButton(text)

    return button


class SplitterOrientation:
    Horizontal = QtCore.Qt.Horizontal
    Vertical   = QtCore.Qt.Vertical


@bindsToClass
def HorizontalSplitter(owner: QWidget, name: str, contents=List[QWidget]) -> QSplitter:
    splitter = QSplitter(QtCore.Qt.Horizontal)

    # NOTE: Splitters can only have QWidgets as children---not QLayouts
    for widget in contents:
        splitter.addWidget(widget)

    return splitter


@bindsToClass
def VerticalSplitter(owner: QWidget, name: str, contents=List[QWidget]) -> QSplitter:
    splitter = QSplitter(QtCore.Qt.Vertical)

    # NOTE: Splitters can only have QWidgets as children---not QLayouts
    for widget in contents:
        splitter.addWidget(widget)

    return splitter


@bindsToClass
def Widget(
    owner: QWidget,
    name: str,
    horizontalPolicy: Optional[QSizePolicy.Policy] =None,
    verticalPolicy: Optional[QSizePolicy.Policy] =None,
    layout: Optional[QLayout] = None
) -> QWidget:
    """[summary]

    Args:
        owner (QWidget): [description]
        name (str): [description]
        layout (QLayout): [description]
        horizontalPolicy (QSizePolicy.Policy, optional): [description]. Defaults to None.
        verticalPolicy (QSizePolicy.Policy, optional): [description]. Defaults to None.

    Returns:
        QWidget: [description]
    """
    widget = QWidget()

    sizePolicy = widget.sizePolicy()

    if horizontalPolicy is not None:
        sizePolicy.setHorizontalPolicy(horizontalPolicy)

    if verticalPolicy is not None:
        sizePolicy.setVerticalPolicy(verticalPolicy)

    widget.setSizePolicy(sizePolicy)

    if layout is not None:
        widget.setLayout(layout)

    return widget


@bindsToClass
def HorizontalSlider(
    owner: QWidget,
    name: str,
) -> QSlider:
    """[summary]"""
    return QSlider(QtCore.Qt.Horizontal)