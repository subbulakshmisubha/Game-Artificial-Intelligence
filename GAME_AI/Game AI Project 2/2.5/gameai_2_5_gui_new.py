
from PySide import QtGui, QtCore
from PyQt4 import Qt

import sys
from PyQt4.QtGui import QApplication, QMainWindow
from PyQt4.QtGui import * 
from PyQt4.QtCore import *


##class to draw the table window where the path of the astar and dijstra algorithm are shown. 
class GridGUi(QtGui.QWidget):
    #This class takes arguments num which if 1 is dijkstra and if 2 is is Astar
    #map is the initial map which is provided.
    #path gives the path given my networkX implementation along which the path has to be draw on gui
    #rotated by default is True
    def __init__(self,num, _map, path,rotated=True):
        QtGui.QWidget.__init__(self)
        self._map = _map
        rowcnt, colcnt = self._map.shape
        self.rotated = rotated
        self.tablewidget = QtGui.QTableWidget(rowcnt, colcnt)
       
        #this brush is used to show the type of pattern that is used along the path and for the wall.         
        brush = QtGui.QBrush(QtGui.QColor(0,0,0),QtCore.Qt.Dense4Pattern)
        table 	= QTableWidget()
        tableItem 	= QTableWidgetItem()      
        tab=QWidget()
        ##this loop is to draw the rows and columns in the table and to set the width and height of each cell and to draw the wall as well which is greyish black.
        for row in xrange(0, rowcnt):
            self.tablewidget.setRowHeight(row, 40)
            for col in xrange(0, colcnt):
                self.tablewidget.setColumnWidth(col, 40)
                self.tablewidget.setItem(row, col, QtGui.QTableWidgetItem())
                if self._map[row, col]:
                    self.tablewidget.item(row, col).setBackground(brush)
        #if the num value is one which is meaning dijkstra algorithm then a text which says dijkstra is displayed in the table         
       
        if num==1:
        	self.setWindowTitle("DIJKSTRA ALGORITHM PATH")

        	self.tablewidget.setItem(0, 3,  QtGui.QTableWidgetItem("D"))
        	self.tablewidget.setItem(0, 4,  QtGui.QTableWidgetItem("I"))
        	self.tablewidget.setItem(0, 5,  QtGui.QTableWidgetItem("J"))
        	self.tablewidget.setItem(0, 6,  QtGui.QTableWidgetItem("K"))
        	self.tablewidget.setItem(0, 7,  QtGui.QTableWidgetItem("S"))
        	self.tablewidget.setItem(0, 8,  QtGui.QTableWidgetItem("T"))
        	self.tablewidget.setItem(0, 9,  QtGui.QTableWidgetItem("R"))
        	self.tablewidget.setItem(0,10,QtGui.QTableWidgetItem("A"))
        	self.tablewidget.setItem(0,12,QtGui.QTableWidgetItem("P"))
        	self.tablewidget.setItem(0,13,QtGui.QTableWidgetItem("A"))
        	self.tablewidget.setItem(0,14,QtGui.QTableWidgetItem("T"))
        	self.tablewidget.setItem(0,15,QtGui.QTableWidgetItem("H"))
        	
        else:
        	#if the num value is not one which is meaning astar algorithm then a text which says astar is displayed in the table
        	self.setWindowTitle("ASTAR ALGORITHM PATH")
        	self.tablewidget.setItem(0, 4,  QtGui.QTableWidgetItem("A"))
        	self.tablewidget.setItem(0, 5,  QtGui.QTableWidgetItem("S"))
        	self.tablewidget.setItem(0, 6,  QtGui.QTableWidgetItem("T"))
        	self.tablewidget.setItem(0, 7,  QtGui.QTableWidgetItem("A"))
        	self.tablewidget.setItem(0, 8,  QtGui.QTableWidgetItem("R"))	
        	self.tablewidget.setItem(0,10,QtGui.QTableWidgetItem("P"))
        	self.tablewidget.setItem(0,11,QtGui.QTableWidgetItem("A"))
        	self.tablewidget.setItem(0,12,QtGui.QTableWidgetItem("T"))
        	self.tablewidget.setItem(0,13,QtGui.QTableWidgetItem("H"))

        
        colour_num=0
        print("path is ",path)
        ##this loop is for showing the source destination and the path of the algorithm
        for i, e in enumerate(path):
            x, y = e
            if i == 0:
            	##for the source
                brush = QtGui.QBrush(QtGui.QColor(255,0,0),QtCore.Qt.Dense2Pattern)
                colour_num=1
            elif i == len(path) - 1:
            	##for the path
            	brush = QtGui.QBrush(QtGui.QColor(255,255,0),QtCore.Qt.Dense2Pattern)
                              
            else:
            	##for the destination
            	brush = QtGui.QBrush(QtGui.QColor(0,128,0),QtCore.Qt.Dense2Pattern)
                          
            if self.rotated:
                pos_of_x = colcnt - 1 - y
                pos_of_y = x
            else:
                pos_of_x, pos_of_y = x, y

            self.tablewidget.item(pos_of_x, pos_of_y).setBackground(brush)

            	
            

        #for resizing the window so that the table fits into it.This is not any random number but after multiple trial and errors found 44 to make sure to be the right value which makes the table fit right and display right to the user
        self.resize(44*rowcnt, 44*colcnt + 10)

        #The table has to be added to a layout .the table widget is added to the layout 
        layout = QtGui.QGridLayout()
        layout.addWidget(self.tablewidget, 0, 0)
        #layout.addWidget(self.button,0,0)
        self.setLayout(layout)
