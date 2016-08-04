#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess
import urllib2
import re
from getEnv import env
   
  
def auth_wget2(url, chunk_size=1048576):
    from os.path import basename, isfile
    from optparse import OptionParser
    from urllib2 import build_opener, Request
    """Returns the content of specified URL, which requires authentication.
    If the content is bigger than 1MB, then save it to file.
    """
    try:
        from Utilities.RelMon.authentication import X509CertOpen
    except ImportError:
        from authentication import X509CertOpen

    opener = build_opener(X509CertOpen())
    url_file = opener.open(Request(url))
    size = int(url_file.headers["Content-Length"])

    if size < 1048576:   # if File size < 1MB
        filename = basename(url)    #still download
        readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
        if filename != '':
            outfile = open(filename, 'wb')  #then write File to local system
            outfile.write(readed)
        return readed

    filename = basename(url)

    if isfile("./%s" % filename):
        print '%s. Exists on disk. Skipping.' % (filename)
        return

    print ' Downloading... %s' % (filename)
    file = open(filename, 'wb')
    chunk = url_file.read(chunk_size)
    while chunk:
        file.write(chunk)
        chunk = url_file.read(chunk_size)
    print '%s.  Done.' % (filename)
    file.close()

def cmd_fetch(option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run):
    # fetchall_from_DQM_v2.py -r CMSSW_7_0_0 -e='TTbar,PU,25' --mc --dry
    import re
    import sys
    import os

    from multiprocessing import Pool, Queue, Process
    from Queue import Empty
    from os.path import basename, isfile
    from optparse import OptionParser
    from urllib2 import build_opener, Request
    
    cmsenv = env()
   
    ## Define options
#    option_is_from_data = "mc" # mc ou data
#    option_release = cmsenv.getCMSSWBASECMSSWVERSION()
#    option_regexp = 'TTbar,PU,25'
#    option_mthreads = 3
#    option_dry_run = True
#    print option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    try:
        from Utilities.RelMon.authentication import X509CertOpen
    except ImportError:
        from authentication import X509CertOpen

    def auth_wget(url, chunk_size=1048576):
        """Returns the content of specified URL, which requires authentication.
        If the content is bigger than 1MB, then save it to file.
        """
        opener = build_opener(X509CertOpen())
        url_file = opener.open(Request(url))
        size = int(url_file.headers["Content-Length"])

        if size < 1048576:   # if File size < 1MB
            filename = basename(url)    #still download
            readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
            if filename != '':
                outfile = open(filename, 'wb')  #then write File to local system
                outfile.write(readed)
            return readed

        filename = basename(url)
        file_id = selected_files.index(filename)

        if isfile("./%s" % filename):
            print '%d. Exists on disk. Skipping.' % (file_id +1)
            return

        print '%d. Downloading...' % (file_id +1)
        file = open(filename, 'wb')
        # progress = 0
        chunk = url_file.read(chunk_size)
        while chunk:
            file.write(chunk)
            # progress += chunk_size
            chunk = url_file.read(chunk_size)
        print '%d.  Done.' % (file_id +1)
        file.close()

    ## Use options
    relvaldir = "RelVal"
    if option_is_from_data == 'data':
        relvaldir = "RelValData"
    print "relvaldir : ", relvaldir
    release = re.findall('(CMSSW_\d*_\d*_)\d*(?:_[\w\d]*)?', option_release)
    if not release:
        parser.error('No such CMSSW release found. Please check the ``--release`` commandline option value.')
    releasedir = release[0] + "x"
#    print "releasedir : ", releasedir
    base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
#    base_url = 'https://cmsweb.cern.ch/dqm/relval-test/data/browse/ROOT/'
    filedir_url = base_url + relvaldir + '/' + releasedir + '/'
#    filedir_url = 'http://cms-project-relval.web.cern.ch/cms-project-relval/relval_stats/'
    filedir_html = auth_wget(filedir_url)

    file_list_re = re.compile(r"<a href='[-./\w]*'>([-./\w]*)<")
    all_files = file_list_re.findall(filedir_html)[1:]  # list of file names

    ### Fetch the files, using multi-processing
    print "cmd_fetch : ", option_regexp.split(',') + [option_release]
    file_res = [re.compile(r) for r in option_regexp.split(',') + [option_release]]

    selected_files = [f for f in all_files if all([r.search(f) for r in file_res])]

    print 'Downloading files:'
    for i, name in enumerate(selected_files):
        print '%d. %s' % (i+1, name)
        
    if option_dry_run:
        print "done"
        return selected_files
    if not option_dry_run:
        print '\nProgress:'
        pool = Pool(option_mthreads)
        pool.map(auth_wget2, [filedir_url + name for name in selected_files])
    
    return 

def list_search(self):
    # on fera la fonction par un appel a cmd_fetchall(options)
    # ou options regroupera option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run
        
    ## Define options
    option_is_from_data = "mc" # mc ou data
    option_release_1 = str(self.lineedit1.text()) # self.cmsenv.getCMSSWBASECMSSWVERSION()
    option_regexp = '_RelValTTbar_13' # str( self.lineedit4.text() ) to be removed
    option_mthreads = 3
    option_dry_run = True # False for loading files
    self.gccs = 'Full' # 'Fast' 'PU'
    
    # get collections list to do (Pt35, Pt10, TTbar, .... if checked)
    
    self.rel_list = []
    
    for items in self.coll_list:
        print "ITEMS : ", items
        option_regexp = str( items ) + '__'
        if ( self.gccs != 'Full' ):
            option_regexp += ',' + str(self.gccs)
        (liste_fichiers_1) = cmd_fetch(option_is_from_data, option_release_1, option_regexp, option_mthreads, option_dry_run)
        self.rel_list += liste_fichiers_1
        
    return 

def explode_item(item):
    # initial file name : DQM_V0001_R000000001__RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
    # prefix in DQM_V0001_R000000001__ removed : RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
    # suffix in __DQMIO.root removed : RelVal
    # new prefix in RelVal removed : TTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    # splitting with __ : TTbar_13 CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    # splitting second term with - : TTbar_13 CMSSW_7_4_0_pre8 PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
    
#    print "explode item : ", item
    temp_item = item[22:] # DQM_V0001_R000000001__ removed
    temp_item = temp_item[:-12] # __DQMIO.root removed
    temp_item = temp_item[6:] # RelVal removed
    temp_item = temp_item.split('__')
#    print "coucou : ", temp_item
    temp_item2 = temp_item[1].split('-', 1)
    temp_item = [ temp_item[0] ]
    for it in temp_item2:
        temp_item.append(it)
#    print "coucou : ", temp_item

    return temp_item

def list_folders(self):
    import os
    
    local_path = os.getcwd()
    list_folder = []
    for it in os.listdir(local_path):
        if os.path.isdir(it):
            list_folder.append(it)
    return list_folder