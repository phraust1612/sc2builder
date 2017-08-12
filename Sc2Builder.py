import sys
import error
import os
import json
from engine import *
from unit import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

VERSION = 1.0

def SecondToStr(sec):
    m = sec // 60
    sec -= 60*m
    return "%02d : %02d"%(m,sec)

def IconPath(name):
    path = 'jpgFiles'
    if os.path.exists('jpgFiles'):
        path = 'jpgFiles'
    elif os.path.exists('../../jpgFiles'):
        path = '../../jpgFiles'
    else:
        return error.NoPathExists

    for root, dirs, files in os.walk(path):
        if name+".jpg" in files:
            return os.path.join(root, name)+".jpg"
        if name+".png" in files:
           return os.path.join(root, name)+".png"
        if name+".gif" in files:
            return os.path.join(root, name)+".gif"
    return error.NoPathExists

class sc2buildUI(QMainWindow):
    def __init__(self, race, filename=''):
        super().__init__()
        self.race = race
        self.savefilename = filename
        self.cursor = 0
        self.inputNo = []
        self.engine = Engine(race)
        self.initUI()

# initialize main interface
    def initUI(self):
        self.setFixedSize(1280,635)
        self.center()
        self.setWindowTitle('sc2builder')
        filename = IconPath('sc2icon')
        if filename != error.NoPathExists:
            self.setWindowIcon(QIcon(filename))

        menu = self.menuBar()
        # this works on for several kinds of OS
        menu.setNativeMenuBar(False)

        menu_file = menu.addMenu('File')

        menu_file_new = QMenu('New',self)
        menu_file_new_protoss = QAction('Protoss',self)
        menu_file_new_protoss.setShortcut('Ctrl+P')
        menu_file_new_protoss.triggered.connect(lambda state,x='protoss':self.NewWindow(x))
        menu_file_new_terran = QAction('Terran',self)
        menu_file_new_terran.setShortcut('Ctrl+T')
        menu_file_new_terran.triggered.connect(lambda state,x='terran':self.NewWindow(x))
        menu_file_new_zerg = QAction('Zerg',self)
        menu_file_new_zerg.setShortcut('Ctrl+Z')
        menu_file_new_zerg.triggered.connect(lambda state,x='zerg':self.NewWindow(x))
        menu_file_new.addAction(menu_file_new_protoss)
        menu_file_new.addAction(menu_file_new_terran)
        menu_file_new.addAction(menu_file_new_zerg)
        menu_file.addMenu(menu_file_new)

        menu_file_open = QAction('Open',self)
        menu_file_open.setShortcut('Ctrl+O')
        menu_file_open.triggered.connect(self.Open)
        menu_file.addAction(menu_file_open)

        menu_file_save = QAction('Save',self)
        menu_file_save.setShortcut('Ctrl+S')
        menu_file_save.triggered.connect(self.Save)
        menu_file.addAction(menu_file_save)

        menu_file_saveas = QAction('Save As',self)
        menu_file_saveas.setShortcut('Ctrl+A')
        menu_file_saveas.triggered.connect(self.SaveAs)
        menu_file.addAction(menu_file_saveas)

        menu_file_exit = QAction('Exit',self)
        menu_file_exit.setShortcut('Ctrl+X')
        menu_file_exit.triggered.connect(self.close)
        menu_file.addAction(menu_file_exit)

        menu_help = menu.addMenu('Help')
        menu_help_about = QAction('About',self)
        menu_help_about.setShortcut('Ctrl+H')
        menu_help_about.triggered.connect(self.About)
        menu_help.addAction(menu_help_about)
        
        self.label = QLabel(self)
        self.label.move(820,30)
        self.label.resize(450,30)

        self.inputTable = QTableWidget(self)
        self.inputTable.resize(800, 45)
        self.inputTable.move(10,30)
        self.inputTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.inputTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.inputTable.horizontalHeader().hide()
        self.inputTable.verticalHeader().hide()
        self.inputTable.setRowCount(1)
        self.inputTable.setRowHeight(0,30)
        self.inputTable.cellClicked.connect(self.eraseInputItem)

        self.board = QTableWidget(self)
        self.board.resize(960,540)
        self.board.move(10,85)
        self.board.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.board.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.board.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.board.horizontalHeader().hide()
        self.board.verticalHeader().hide()
        self.board.setColumnCount(10000)
        self.board.setRowCount(50)
        for i in range(self.board.columnCount()):
            self.board.setColumnWidth(i,5)
        for i in range(self.board.rowCount()):
            self.board.setRowHeight(i,20)
        self.board.horizontalScrollBar().valueChanged.connect(self.moveCursor)
        self.board.cellClicked.connect(self.eraseItem)

        self.cursorLine = QWidget(self.board)
        self.cursorLine.setStyleSheet("background-color: rgb(0,0,0)")
        self.cursorLine.resize(2,540)
        self.cursorLine.move(0,0)

        self.unitList = QTableWidget(self)
        self.unitList.resize(130, 265)
        self.unitList.move(1140, 85)
        self.unitList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.unitList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.unitList.horizontalHeader().hide()
        self.unitList.verticalHeader().hide()
        self.unitList.setColumnCount(1)
        self.unitList.setRowCount(50)
        self.unitList.setColumnWidth(0, 120)

        self.buildingList = QTableWidget(self)
        self.buildingList.resize(130, 265)
        self.buildingList.move(1140, 360)
        self.buildingList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.buildingList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.buildingList.horizontalHeader().hide()
        self.buildingList.verticalHeader().hide()
        self.buildingList.setColumnCount(1)
        self.buildingList.setRowCount(50)
        self.buildingList.setColumnWidth(0, 120)

        self.unitButton = []
        self.buildingButton = []
        self.upgradeButton = []
        self.mineralButton = QPushButton(self)
        self.gasButton = QPushButton(self)
        self.mineralButton.resize(30,30)
        self.gasButton.resize(30,30)
        self.mineralButton.move(980, 85)
        self.gasButton.move(1010,85)
        filename = IconPath('mineral')
        if filename != error.NoPathExists:
            self.mineralButton.setIcon(QIcon(filename))
        self.mineralButton.setIconSize(QSize(28,28))
        filename = IconPath('gas')
        if filename != error.NoPathExists:
            self.gasButton.setIcon(QIcon(filename))
        self.gasButton.setIconSize(QSize(28,28))
        self.mineralButton.clicked.connect(lambda: self.gatherMineral())
        self.gasButton.clicked.connect(lambda: self.gatherGas())
        self.skillButton = []
        for x in range(3):
            self.skillButton.append(QPushButton(self))
            self.skillButton[-1].resize(30,30)
            self.skillButton[-1].move(1040+30*x, 85)
            self.skillButton[x].clicked.connect(lambda state, xx = x: self.useSkill(xx))
        if self.race == "protoss":
            filename = IconPath('chronoboost')
            if filename != error.NoPathExists:
                self.skillButton[0].setIcon(QIcon(filename))
            self.skillButton[0].setIconSize(QSize(28,28))

        unit_ = list(unit_dict['unit'][self.race].items())
        for y in range(6):
            for x in range(5):
                self.unitButton.append(QPushButton(self))
                self.unitButton[-1].resize(30,30)
                self.unitButton[-1].move(980+30*x,125+30*y)
                self.unitButton[-1].clicked.connect(lambda state,i=5*y+x: self.unitBuild(i))
        for i in range(len(unit_)):
            filename = IconPath(unit_[i][0])
            if filename == error.NoPathExists:
                continue
            if type(filename) == type(""):
                self.unitButton[unit_[i][1]['no']].setIcon(QIcon(filename))
                self.unitButton[unit_[i][1]['no']].setIconSize(QSize(28,28))

        building_ = list(unit_dict['building'][self.race].items())
        for y in range(4):
            for x in range(5):
                self.buildingButton.append(QPushButton(self))
                self.buildingButton[-1].resize(30,30)
                self.buildingButton[-1].move(980+30*x,315+30*y)
                self.buildingButton[-1].clicked.connect(lambda state,i=5*y+x: self.structureBuild(i))
        for i in range(len(building_)):
            filename = IconPath(building_[i][0])
            if filename == error.NoPathExists:
                continue
            if type(filename) == type(""):
                self.buildingButton[building_[i][1]['no']].setIcon(QIcon(filename))
                self.buildingButton[building_[i][1]['no']].setIconSize(QSize(28,28))

        upgrade_ = list(unit_dict['upgrade'][self.race].items())
        for y in range(6):
            for x in range(5):
                self.upgradeButton.append(QPushButton(self))
                self.upgradeButton[-1].resize(30,30)
                self.upgradeButton[-1].move(980+30*x,445+30*y)
                self.upgradeButton[-1].clicked.connect(lambda state,i=5*y+x: self.upgradeBuild(i))
        for i in range(len(upgrade_)):
            filename = IconPath(upgrade_[i][0])
            if filename == error.NoPathExists:
                continue
            if type(filename) == type(""):
                self.upgradeButton[upgrade_[i][1]['no']].setIcon(QIcon(filename))
                self.upgradeButton[upgrade_[i][1]['no']].setIconSize(QSize(28,28))

        self.show()

# move the window to the center
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def Save(self):
        if self.savefilename == "":
            self.SaveAs()
        else:
            with open(self.savefilename, 'w') as f:
                f.write(str(VERSION)+"\n")
                f.write(self.race+"\n")
                json.dump(self.engine.input,f)

    def SaveAs(self):
        savefilename = QFileDialog.getSaveFileName(self, 'Save File', '.', '*.s2b')
        if savefilename[0]:
            if len(savefilename[0]) < 5 or savefilename[0][-4:] != '.s2b':
                self.savefilename = savefilename[0] + '.s2b'
            else:
                self.savefilename = savefilename[0]
            self.Save()

    def Open(self):
        savefilename = QFileDialog.getOpenFileName(self, 'Open File', '.', '*.s2b')
        if savefilename[0]:
            self.savefilename = savefilename[0]
            with open(self.savefilename, 'r') as f:
                text = f.readlines()
                if len(text)<3:
                    err = error.WrongFileFormat
                    errmsg = error.ErrorMsg(err)
                    msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
                    return err

                if text[0]:
                    try:
                        version = float(text[0])
                    except ValueError:
                        err = error.WrongFileFormat
                        errmsg = error.ErrorMsg(err)
                        msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
                        return err
                    if version > VERSION or version<1.0:
                        err = error.IncompatibleVersion
                        errmsg = error.ErrorMsg(err)
                        msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
                        return err
                else:
                    err = error.WrongFileFormat
                    errmsg = error.ErrorMsg(err)
                    msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
                    return err

                if version == 1.0:
                    if text[1]:
                        race = text[1]
                        race = race[:-1]
                        if race not in ["protoss","terran","zerg"]:
                            err = error.WrongRace
                            errmsg = error.ErrorMsg(err)
                            msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
                            return err
                    else:
                        err = error.WrongFileFormat
                        errmsg = error.ErrorMsg(err)
                        msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
                        return err

                    if text[2]:
                        newinput = json.loads(text[2])
                    else:
                        err = error.WrongFileFormat
                        errmsg = error.ErrorMsg(err)
                        msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
                        return err

                    self.close()
                    newMD = sc2buildUI(race,self.savefilename)
                    newMD.engine.input = newinput
                    err = newMD.engine.Rearrange()

                    if err < 0:
                        errmsg = error.ErrorMsg(err)
                        msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
                        return err
                    else:
                        newMD.drawBoard()
                        newMD.newCursor(err)
                        return newMD.cursor
        return 0

    def NewWindow(self, race, filename=''):
        self.close()
        newMD = sc2buildUI(race)

    def About(self):
        msg = QMessageBox.information(self,"About...",\
            "sc2builder ver %1.1f\n"%VERSION+\
            "Made by 민병욱(Min Byeonguk)\n"+\
            "contact me : phraust1612@gmail.com\n"+\
            "https://github.com/phraust1612",\
            QMessageBox.Ok, QMessageBox.Ok)

# called when scroller moved (event)
    def moveCursor(self):
        HScroll = self.board.horizontalScrollBar().value()
        self.cursorLine.move(5*(self.cursor - HScroll), 0)

# order a worker to gather minerals who used to mine gases
    def gatherMineral(self):
        self.engine.AddItem("mineral", "mineral")
        err = self.engine.Rearrange()
        if err < 0:
            errmsg = error.ErrorMsg(err)
            msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
            self.engine.DeleteItem(-1)
            return err

        self.drawBoard()
        return 0

# order a worker to gather gases who used to mine minerals
    def gatherGas(self):
        self.engine.AddItem("gas", "gas")
        err = self.engine.Rearrange()
        if err < 0:
            errmsg = error.ErrorMsg(err)
            msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
            self.engine.DeleteItem(-1)
            return err

        self.drawBoard()
        self.newCursor(err)
        return 0

    def useSkill(self,no):
        if self.race == "protoss" and no == 0:
            self.engine.AddItem("chronoboost","skill")

    def unitBuild(self, no):
        k = unit_dict['unit'][self.race].keys()
        item = 0
        for i in k:
            if unit_dict['unit'][self.race][i]['no'] == no and unit_dict['unit'][self.race][i]['race'] == self.race:
                item = i
                break
        if item == 0:
            # unit doesn't exist
            msg = QMessageBox.warning(self,'error!!!','Unappropriate unit!!!', QMessageBox.Ok, QMessageBox.Ok)
            return error.WrongUnitName

        self.engine.AddItem(item, "unit")
        err = self.engine.Rearrange()
        if err < 0:
            errmsg = error.ErrorMsg(err)
            msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
            self.engine.DeleteItem(-1)
            return err
        else:
            self.drawBoard()
            self.newCursor(err)
            return self.cursor

    def structureBuild(self, no):
        k = unit_dict['building'][self.race].keys()
        item = 0
        for i in k:
            if unit_dict['building'][self.race][i]['no'] == no and unit_dict['building'][self.race][i]['race'] == self.race:
                item = i
                break
        
        if item == 0:
            # unit doesn't exist
            msg = QMessageBox.warning(self,'error!!!','Unappropriate building!!!', QMessageBox.Ok, QMessageBox.Ok)
            return error.WrongBuildingName

        self.engine.AddItem(item, "building")
        err = self.engine.Rearrange()
        if err < 0:
            errmsg = error.ErrorMsg(err)
            msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
            self.engine.DeleteItem(-1)
            return err
        else:
            self.drawBoard()
            self.newCursor(err)
            return self.cursor

    def upgradeBuild(self, no):
        k = unit_dict['upgrade'][self.race].keys()
        item = 0
        for i in k:
            if unit_dict['upgrade'][self.race][i]['no'] == no and unit_dict['upgrade'][self.race][i]['race'] == self.race:
                item = i
                break
        if item == 0:
            # unit doesn't exist
            msg = QMessageBox.warning(self,'error!!!','Upgrade doesn\'t exist!!!', QMessageBox.Ok, QMessageBox.Ok)
            return error.WrongUpgradeName

        self.engine.AddItem(item, "upgrade")
        err = self.engine.Rearrange()
        if err < 0:
            errmsg = error.ErrorMsg(err)
            msg = QMessageBox.warning(self,'error!!!',errmsg, QMessageBox.Ok, QMessageBox.Ok)
            self.engine.DeleteItem(-1)
            return err
        else:
            self.drawBoard()
            self.newCursor(err)
            return self.cursor

    def drawBoard(self):
        self.board.clearSpans()
        self.inputTable.clearSpans()

        # draw inputTable items
        self.inputTable.setColumnCount(len(self.engine.input))
        for i in range(len(self.engine.input)):
            self.inputTable.setColumnWidth(i, 30)
            filename = IconPath(self.engine.input[i][0])
            if filename == error.NoPathExists:
                continue
            if type(filename) == type(""):
                self.inputTable.setItem(0, i, QTableWidgetItem())
                icon = QIcon(filename)
                self.inputTable.item(0,i).setIcon(icon)

        # draw items from engine.queue
        # this includes units, buildings, upgrades
        self.inputNo = []
        for item in self.engine.queue:
            if item.state != "start":
                continue
            level = 0
            while self.board.columnSpan(level, item.starttime) != 1:
                level += 1

            self.board.setSpan(level, item.starttime, 1, item.endtime - item.starttime)
            self.board.setItem(level, item.starttime, QTableWidgetItem(item.name))

            # for the case of chronoboosted units or upgrades would have blue background color
            # and if it was boosted partially, it gets little lighter blue background
            if item.type == 'unit' or item.type == 'upgrade':
                if item.boosted > 1:
                    self.board.item(level, item.starttime).setBackground(QColor(0,0,255,50))
                elif item.boosted == 1:
                    self.board.item(level, item.starttime).setBackground(QColor(0,0,255,25))
                else:
                    self.board.item(level, item.starttime).setBackground(QColor(255,255,255))
            else:
                self.board.item(level, item.starttime).setBackground(QColor(255,255,255))
            self.inputNo.append( (level, item.starttime, item.inputlink) )

        # draw items from engine.worker for the case of gathering gases/minerals
        for i in range(len(self.engine.worker.time)):
            if self.engine.worker.gas[i] == 0:
                continue
            elif self.engine.worker.gas[i] < 0:
                text = "gas"+str(self.engine.worker.gas[i])
            else:
                text = "gas+"+str(self.engine.worker.gas[i])
            level = 0
            while self.board.columnSpan(level, self.engine.worker.time[i]) != 1 \
                or self.board.columnSpan(level, self.engine.worker.time[i]+11) != 1:
                level += 1
            self.board.setSpan(level, self.engine.worker.time[i], 1, 12)
            self.board.setItem(level, self.engine.worker.time[i], QTableWidgetItem(text))

    def eraseItem(self, row, col):
        err = error.NoItemToDelete
        for i in self.inputNo:
            if i[0] == row and i[1] == col:
                err = self.engine.DeleteItem(i[2])
                break

        # if there was no item clicked, move cursor to there
        if err <0:
            self.newCursor(col)
            self.board.clearSelection()
            return err
        self.board.item(row, col).setBackground(QColor(255,255,255))
        self.newCursor(err)
        self.drawBoard()
        self.board.clearSelection()
        return 0

    def eraseInputItem(self, row, col):
        err = error.NoItemToDelete
        err = self.engine.DeleteItem(col)
        if err <0:
            return err
        self.newCursor(err)
        self.drawBoard()
        return 0

# set cursor value and show current status
    def newCursor(self, val):
        self.cursor = val
        HScroll = self.board.horizontalScrollBar().value()
        self.cursorLine.move(5*(self.cursor - HScroll), 0)

        mineral, gas = self.engine.AccResources(self.cursor)
        curSup, maxSup = self.engine.CurrentSupply(self.cursor)
        text = "time : "+SecondToStr(self.cursor)+", mineral : "+str(mineral)+", gas : "+str(gas)+", supply : "+str(curSup)+"/"+str(maxSup)
        self.label.setText(text)

        ind = 0
        for i in unit_dict['unit'][self.race]:
            count = self.engine.unitCount(i, self.cursor)
            if count <= 0:
                continue
            text = i + " : " + str(count)
            self.unitList.setItem(ind, 0, QTableWidgetItem(text))
            ind += 1

        ind = 0
        for i in unit_dict['building'][self.race]:
            count = self.engine.buildingCount(i, self.cursor)
            if count <= 0:
                continue
            text = i + " : " + str(count)
            self.buildingList.setItem(ind, 0, QTableWidgetItem(text))
            ind += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        MD = sc2buildUI(sys.argv[1])
    else:
        MD = sc2buildUI('protoss')
    sys.exit(app.exec_())

