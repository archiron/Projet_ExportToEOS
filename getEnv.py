#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import urllib2

class env:
    def __init__(self): 
        # os.getenv is equivalent, and can also give a default value instead of `None`
        print os.getenv('CMSSW_BASE', "RIEN")
        self.CMSSWBASE = os.getenv('CMSSW_BASE', "CMSSW_BASE")
        self.CMSSWBASECMSSWRELEASEBASE = os.getenv('CMSSW_RELEASE_BASE', "CMSSW_RELEASE_BASE")
        self.CMSSWBASECMSSWVERSION = os.getenv('CMSSW_VERSION', "CMSSW_VERSION")

    def getCMSSWBASE(self):
        CMSSWBASE = os.getenv('CMSSW_BASE', "CMSSW_BASE")
        return CMSSWBASE
		
    def getCMSSWBASECMSSWRELEASEBASE(self):
        return self.CMSSWBASECMSSWRELEASEBASE
		
    def getCMSSWBASECMSSWVERSION(self):
        return self.CMSSWBASECMSSWVERSION
		
    def cmsAll(self):
        cmsAll="<strong>CMSSW_BASE</strong> : " + self.getCMSSWBASE()
        cmsAll+="<br /><strong>CMSSW_RELEASE_BASE</strong> : " + self.getCMSSWBASECMSSWRELEASEBASE()
        cmsAll+="<br /><strong>CMSSW_VERSION</strong> : " + self.getCMSSWBASECMSSWVERSION()
        return cmsAll

    def eosText(self):
        eosText="/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select"
        eosText+=' ls /eos/cms/store/relval/' 
        return eosText

    def eosFind(self):
        eosFind="http://cms-project-relval.web.cern.ch/cms-project-relval/relval_stats/"
        return eosFind

