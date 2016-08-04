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
        self.setWindowTitle('CheckRootFiles publish v0.1.2')

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

		# creation label resume
        self.labelResume = QLabel(self.trUtf8(self.texte), self)
        # creation du grpe Folders paths
        self.QGBoxFinal = QGroupBox("Folders paths")
        vbox8 = QVBoxLayout()
        vbox8.addWidget(self.labelResume)
        self.QGBoxFinal.setLayout(vbox8)

        #Layout intermediairy : ComboBox + labelcombo
        self.layoutV_combobox = QVBoxLayout()
        self.layoutV_combobox.addWidget(self.QGBoxFinal)
        
        # creation des onglets
        self.onglets = QTabWidget()
        self.onglets.setMinimumHeight(150)
        self.onglets.setMaximumHeight(200)
        self.generalTab = QWidget()
        self.onglets.insertTab(0, self.generalTab, "General")
        #Set Layout for Tabs Pages
        self.generalTab.setLayout(self.layoutV_combobox)   

        #Layout principal
        self.layout_general = QVBoxLayout()
        self.layout_general.addLayout(self.QHL)
        self.layout_general.addLayout(self.layoutH_release)
        self.layout_general.addWidget(self.onglets)
        self.layout_general.addLayout(self.layoutH_boutons)
        self.setLayout(self.layout_general)       

        print "end"

    def Export_1(self):
        import subprocess
        import os
    
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
            cmssw_version = self.lineedit1.text()
            print "CMSSW VERSION : ", cmssw_version
            cmd_eos = self.cmsenv.eosCopy() + os.getcwd() + '/' + self.lineedit1.text() + '/ ' + self.cmsenv.eosTarget() + self.lineedit1.text() + '/' #  
            print "cmde eos : ", cmd_eos
            proc = subprocess.Popen([cmd_eos], stdout=subprocess.PIPE, shell=True) 
            (out, err) = proc.communicate()

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

 # list_DataSets_FULL -> liste_datasets