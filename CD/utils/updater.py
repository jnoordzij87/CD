from datetime import datetime
import os
from utils.paths import *
from zipfile import ZipFile
import zipfile
import glob
from shutil import *
import subprocess
from subprocess import *
from utils.unzipper import *
from utils.zipFilters import *
import utils.zipBuilder

class Updater:

    def __init__(self):
        self.CopiedZips = {}
        pass
    
    def Update(self, tasks):
        
        self.StartTime = self.GetTime()
        self.Tasks = tasks
        
        #stop if no working vpn connection
        if not self.TestVPN():
            return
        
        #create ZIP files 
        self.CreateZipFiles()
        
        #execute task on server 
        for task in self.Tasks:
           task = self.ExecuteTaskOnServer(taskId)

        print('All tasks completed.')
    
    def TestVPN(self):
        print('Testing VPN...')
        if not os.path.exists(r"\\demo-ts-2\DEMO\Demonstratie"):
            print('...VPN not working, aborted!')
            return False
        else:
            print('...working.')
            return True

    def ExecuteTaskOnServer(self, task):

        print('Starting distribution for', program, environment)

        #get updatefolderpath and zipfilepath from timestamp
        task.UpdateFolderPath = task.GetUpdateFolderPath(timeSuffix)
        task.ZipFileCopyDstPath = os.path.join(updateFolder, os.path.basename(task.ZipFileCopySrcPath))

        #copy zip to server, but only once per program/version/server
        #if 2 envs on 1 server need the same binaries, copy zip once and use for both envs
        hasProgramUpdateBeenCopiedToServer = self.HasProgramUpdateBeenCopiedToServer(task)
        copySuccess = False
        doUnzip = False
        if hasProgramUpdateBeenCopiedToServer:
            #copying not needed, proceed to unzip file
            doUnzip = True
        else:
            #do copy
            copySuccess = self.CopyZipToServer(task)
            doUnzip = copySuccess
            
        #unzip on server
        if doUnzip:
            #get the file to unzip
            fileToUnzip = self.CopiedZips[program][version][server]
            
            #unzip into update folder
            print('Proceeding to unzip in update folder: ', environment, program)
            self.UnzipOnServer(fileToUnzip, updateFolder)
            
            #TODO NEXT:
            #unzip into live folder
            #print('Proceeding to unzip in update folder: ', environment, program)
            #self.Unpack(fileToUnzip, liveFolder)
        
        print("---END OF TASK---")

    def HasProgramUpdateBeenCopiedToServer(self, task):
        program = task.Program
        version = task.Version
        server = task.Server
        #copied zips are stored like this: CopiedZips[program][server] = zip_dst_fpath
        if not program in self.CopiedZips or not version in self.CopiedZips[program] or not server in self.CopiedZips[program][version]:
            return False
        else:
            return True
        #other option: iterate all tasks for task.HasZipBeenCopiedToServer flag

    def UnzipOnServer(self, zipfile, unpackdir):
        server = self.GetServerFromPath(zipfile)
        unzipperObj = Unzipper()
        unzipperObj.UnzipOnServer(server, zipfile, unpackdir)

    def CopyZipToServer(self, task):
        copysrc = task.ZipFileCopySrcPath
        copydst = task.ZipFileCopyDstPath
        program = task.Program
        version = task.Version
        server = task.Server
        
        success = False
        
        #copy zip to server
        copysuccess = self.CopyWithXcopy(copysrc, copydst)

        if copysuccess:
            success = True

            #store the zip location
            if not program in self.CopiedZips:
                self.CopiedZips[program] = {}
            if not version in self.CopiedZips[program]:
                self.CopiedZips[program][version] = {}
            self.CopiedZips[program][version][server] = zip_dst_fpath
                
        return success

    def CopyWithXcopy(self, zip_src_fpath, zip_dst_fpath):
    
        print('Copying ZIP to update folder...')
        
        #ensure zip_dest_fpath exists
        os.makedirs(os.path.dirname(zip_dst_fpath), exist_ok=True)
        
        #keep track of success
        success = False
            
        try:
            #copy with xcopy
            print('xcopy src:', zip_src_fpath)
            print('xcopy dst:', zip_dst_fpath)
            print('filesize:', os.path.getsize(zip_src_fpath) )
            subprocess.call('xcopy.exe "%s" "%s*" /q /j' % (zip_src_fpath, zip_dst_fpath))
            success = True
        except Exception as e:
            print('ERROR ----- Exception while copying ZIP to update folder. Be sure to check that your VPN is working correctly. Exception message: ' + str(e))
        
        if success:
            print('...complete. ')
        
        return success

    def IsMakingZipFileNecessary(self, task):
        #only necessary if there is not already a zipfile in lookup for this program and version
        version = task.Version
        program = task.Program
        if not version in self.CreatedZipFilesByVersionProgram or not program in self.CreatedZipFilesByVersionProgram[version]:
            return True
        else:
            return False

    def CreateZipFiles(self):
        #make a lookup for created zipfiles so we can access them later
        self.CreatedZipFilesByVersionProgram = {} #will this remain necessary?
        for task in self.Tasks:
            if self.IsMakingZipFileNecessary(task):
                binarysource = task.BinSourcePath
                #get files to zip
                filesToZip = FilterDir(task)
                #create zip
                zipFile = self.CreateZipFile(task, filesToZip)
                #add to lookup
                if not version in self.CreatedZipFilesByVersionProgram:
                    self.CreatedZipFilesByVersionProgram[version] = {}  
                    self.CreatedZipFilesByVersionProgram[version][program] = zipFile
                #store reference to zipfile location
                task.ZipFileCopySrcPath = zipFile.filename
            else:
                #store reference to zipfile location
                task.ZipFileCopySrcPath = self.CreatedZipFilesByVersionProgram[version][program]
                    
            
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
    
    def GetTime(self):
        date = datetime.today().strftime('%Y%m%d')
        time = datetime.today().strftime('%H%M')
        result = date+"_"+time
        print(result)
        return result
        
    