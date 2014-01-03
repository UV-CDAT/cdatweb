import os,sys
import metrics.fileio.findfiles
from metrics.diagnostic_groups import *
import metrics.frontend.uvcdat

from django.conf import settings

tmppath=os.path.join(os.environ["HOME"],"tmp")

class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance

class ObsMenu(object):
    __metaclass__ = SingletonType

    def __init__(self):
        path2=settings.DIAG_OBS_PATH
        datafile2 = metrics.fileio.findfiles.dirtree_datafiles( path2)
        self.obs_menu=datafile2.check_filespec()

def get_filetable1():
    path1=settings.DIAG_MODEL_PATH
    if not os.path.exists(tmppath):
        os.makedirs(tmppath)
    datafiles = metrics.fileio.findfiles.dirtree_datafiles( path1 )
    filetable1 = datafiles.setup_filetable( tmppath, "model" )
    print "filetable1=", filetable1
    return filetable1

def get_observations():
    obs=None
    obs_menu=ObsMenu().obs_menu
    #path2=settings.DIAG_OBS_PATH
    #datafile2 = metrics.fileio.findfiles.dirtree_datafiles( path2)
    #obs_menu=datafile2.check_filespec()
    if type(obs_menu) is dict:
        obs=obs_menu.keys()
    return obs

def get_filetable2(obs):
    if not os.path.exists(tmppath):
        os.makedirs(tmppath)
    obs_menu=ObsMenu().obs_menu
    if obs_menu:
        filt2 = obs_menu[obs]
        path2=settings.DIAG_OBS_PATH
        datafile2 = metrics.fileio.findfiles.dirtree_datafiles(path2,filt2)
        print "datafile2=", datafile2
        filetable2 = datafile2.setup_filetable(tmppath,"obs")
    else:
        path2=settings.DIAG_OBS_PATH
        datafile2 = metrics.fileio.findfiles.dirtree_datafiles( path2)
        obs_menu=datafile2.check_filespec()
        filt2 = obs_menu[obs]
        datafile2 = metrics.fileio.findfiles.dirtree_datafiles(path2,filt2)
        filetable2 = datafile2.setup_filetable(tmppath,"obs")
    return filetable2

def get_input_parameter(package, plot_set, seasonID, variableID,obsID):
    dg_menu=diagnostics_menu()[str(package)]()
    plot_set_obj=dg_menu.list_diagnostic_sets()[str(plot_set)]
    filetable1=get_filetable1()
    filetable2=get_filetable2(obsID)
    return plot_set_obj,filetable1,filetable2, variableID, seasonID


