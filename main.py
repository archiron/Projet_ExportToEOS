#! /usr/bin/env python
#-*-coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import os,sys
import ExportToEOS

from getEnv import env
		
def main(args):
    a=QApplication(args)
    # Creation d'un widget qui servira de fenetre
    a.setFont( QFont( "Latin", 11, QFont.Normal ) )
    
    fenetre = ExportToEOS.ExportToEOS()
    fenetre.move(100, 100)
    fenetre.show()
    r = a.exec_()
    return r

if __name__=="__main__":
    main(sys.argv)