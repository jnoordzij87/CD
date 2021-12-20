from datetime import datetime
import os
from utils.paths import *
from zipfile import ZipFile
import zipfile
import glob
from shutil import *
import utils.zipFilters

class ZipBuilder:    
    
    #def CreateZipFiles(self):
    #    #make a lookup for created zipfiles so we can access them later
    #    self.ZipfileLookup = {}
    #    for program, sourcepath in self.Sources.items():
    #        #continue only if valid sourcepath
    #        if sourcepath:
    #            #get files to zip
    #            filesToZip = ZipFilters.FilterDir(sourcepath, program)
    #            #create zipfile and add to lookup
    #            self.ZipfileLookup[program] = self.BuildZip(sourcepath, filesToZip)
    #        
    #def BuildZip(self, sourcepath, filesToZip):
    #    print('Building ZIP ...')
    #    zipfilepath = os.path.join(sourcepath, ('update_' + self.StartTime))
    #    zf = ZipFile(zipfilepath, 'w')
    #    for file in filesToZip:
    #        #get archivename (i.e. filepath without zip root)
    #        archivename = file.split(sourcepath)[-1]
    #        #add to zip 
    #        zf.write(file, archivename) 
    #    zf.close()
    #    print('...complete')
    #    return zf