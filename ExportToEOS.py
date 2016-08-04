#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore

import os,sys,subprocess
from getEnv import env
		
#############################################################################
class ExportToEOS(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('CheckRootFiles publish v0.2.1')

        self.cmsenv = env()
        self.texte = self.cmsenv.cmsAll()
        self.coll_list = []
        self.working_dir_base = os.getcwd()
        self.liste_folders = self.list_folders()
        print self.cmsenv.CMSSWBASECMSSWVERSION
						
		# creation of texEdit for the folder to export
        self.QGBox1 = QGroupBox("Selected folder")
        self.QGBox1.setMaximumHeight(80)
        self.QGBox1.setMinimumHeight(80)
        self.QGBox1.setMinimumWidth(800)
        self.lineedit1 = QLineEdit(self)
        self.lineedit1.setText(self.cmsenv.CMSSWBASECMSSWVERSION) # default
        self.lineedit1.setMinimumWidth(450)
        self.label1 = QLabel("Folder : ", self)
        self.label1.setMaximumWidth(50)
        self.label1.setMinimumWidth(50)
        # Création of Export button
        self.bouton1 = QPushButton(self.trUtf8("Export !"),self)
        self.bouton1.setFont(QFont("Comic Sans MS", 10,QFont.Bold,True))
        self.bouton1.setIcon(QIcon("../images/smile.png"))
        self.bouton1.setMinimumWidth(50)
        self.connect(self.bouton1, SIGNAL("clicked()"), self.Export_1) 

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.lineedit1)
        hbox1.addWidget(self.bouton1)
        vbox1 = QVBoxLayout()
        vbox1.addLayout(hbox1)
        vbox1.addStretch(1)
        self.QGBox1.setLayout(vbox1)

        #Layout intermediairy 1
        self.layoutH_release = QHBoxLayout()
        self.layoutH_release.addStretch(1)
        self.layoutH_release.addWidget(self.QGBox1)
      
        self.QHL = QHBoxLayout()
        self.QGBox1 = QGroupBox("List")
        self.QGBox1.setMinimumWidth(800)
        self.vbox1 = QVBoxLayout()
        self.QLW1 = QListWidget()
        for it in self.liste_folders:
            item = QListWidgetItem("%s" % it)
            self.QLW1.addItem(item)
        self.connect(self.QLW1, SIGNAL("itemSelectionChanged()"),self.ItemRelClicked1)
        self.vbox1.addWidget(self.QLW1)        
        self.QGBox1.setLayout(self.vbox1)
        self.QHL.addWidget(self.QGBox1)

        # Creation of quit button
        self.boutonQ = QPushButton(self.trUtf8("Quitter ?"),self)
        self.boutonQ.setFont(QFont("Comic Sans MS", 14,QFont.Bold,True))
        self.boutonQ.setIcon(QIcon("../images/smile.png"))
        self.connect(self.boutonQ, SIGNAL("clicked()"), qApp, SLOT("quit()"))
        
        #Layout intermediairy with buttons
        self.layoutH_boutons = QHBoxLayout()
        self.layoutH_boutons.addStretch(1)
        self.layoutH_boutons.addWidget(self.boutonQ)

        #Layout principal
        self.layout_general = QVBoxLayout()
        self.layout_general.addLayout(self.QHL)
        self.layout_general.addLayout(self.layoutH_release)
        self.layout_general.addLayout(self.layoutH_boutons)
        self.setLayout(self.layout_general)       

        print "end"

    def Export_1(self):
        import subprocess
        import os, glob
    
        self.cmsenv = env()
        local_path = os.getcwd()
        
        if ( self.lineedit1.text() == '' ):
            BoiteMessage = QMessageBox()
            BoiteMessage.setText("There is no folder to export.")
            BoiteMessage.setWindowTitle("WARNING !")
            BoiteMessage.exec_()
        elif ( not os.path.isdir(self.lineedit1.text()) ):
            BoiteMessage = QMessageBox()
            BoiteMessage.setText("There is a pbm with this folder name.")
            BoiteMessage.setWindowTitle("WARNING !")
            BoiteMessage.exec_()
        else:
            print "Export for " + self.lineedit1.text()
            folder_name = self.lineedit1.text()
            folder_path = os.getcwd() + '/' + str(folder_name)
#            print "Folder Name : ", folder_name
#            print "Folder Path : ", folder_path
            
            [number_of_dirs, number_of_files] = self.get_walk(folder_path)
            print "there is %d files to copy" % number_of_files
            print "there is %d dirs to create" % number_of_dirs
           
            cmd_eos = self.cmsenv.eosCopy() + os.getcwd() + '/' + folder_name + '/ ' + self.cmsenv.eosTarget() + folder_name + '/' #  
#            print "cmde eos : ", cmd_eos
            proc = subprocess.Popen([cmd_eos], stdout=subprocess.PIPE, shell=True) 
            (out, err) = proc.communicate()
#            print "out : %s" % out
            
            BoiteMessage = QMessageBox()
            BoiteMessage.setText("All is done.")
            BoiteMessage.setWindowTitle("INFORMATION !")
            BoiteMessage.exec_()            

    def ItemRelClicked1(self):
        print "ItemRelClicked1 : self.liste_folders : %s " % self.QLW1.currentItem().text()
        self.lineedit1.setText(self.QLW1.currentItem().text()) 

    def list_folders(self):
        import os
    
        local_path = os.getcwd()
        list_folder = []
        for it in os.listdir(local_path):
            if os.path.isdir(it):
                list_folder.append(it)
        return list_folder

    def get_walk(self, folder_path):
        number_of_dirs = 0
        number_of_files = 0
        for path, dirs, files in os.walk(folder_path):
            number_of_files += len(files)
            print "nb of files %d" % number_of_files
            for name in files:
                print(os.path.join(path, name))
            for name in dirs:
                number_of_dirs += len(dirs)
                print "nb of files %d" % number_of_dirs
                print(os.path.join(path, name))
                self.get_walk(os.path.join(path, name))
        return [number_of_dirs, number_of_files]
       