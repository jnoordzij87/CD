from datetime import datetime
import os
from utils.paths import *
from zipfile import ZipFile
import zipfile
import glob
from shutil import *
from utils.zipFilters import *

class ZipBuilder:
    
    def __init__(self, tasks):
        self.Tasks = tasks
    
    def CreateZipFiles(self):
        for task in self.Tasks:
            isZippingNecessary, zipSrcPath = self.IsMakingZipFileNecessary(task)
            if isZippingNecessary:
                binarysource = task.BinSourcePath
                #get files to zip
                filesToZip = FilterDir(task)
                #create zip
                zipFile = self.CreateZipFile(task, filesToZip)
                #register that zip has been made for this task
                task.HasACreatedZipfile = True
                #store reference to zipfile location
                task.ZipFileCopySrcPath = zipFile.filename
            else:
                #store reference to zipfile location
                task.ZipFileCopySrcPath = zipSrcPath
                    
            
    def CreateZipFile(self, task, filesToZip):
        print("Building ZIP for {} {} ...".format(task.Program, task.Version))
        zipfilepath = os.path.join(task.BinSourcePath, (self.StartTime + ".zip"))
        zf = ZipFile(zipfilepath, 'w')
        for file in filesToZip:
            #get archivename (i.e. filepath without zip root)
            archivename = file.split(sourcepath)[-1]
            #add to zip 
            zf.write(file, archivename) 
        zf.close()
        print('...complete')
        return zf

    def IsMakingZipFileNecessary(self, thistask):
        #only necessary if there is not already a task that has created a zipfile for the same program and version  
        for task in self.Tasks:
            sameProgram = task.Program == thistask.Program
            sameVersion = task.Version == thistask.Verion
            if task.HasACreatedZipfile and sameProgram and sameVersion:
                #zip already available
                return False, task.ZipFileCopySrcPath
        #if we are here, zip doesnt exist yet
        return True, None
