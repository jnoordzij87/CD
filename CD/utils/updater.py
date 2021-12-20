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
from utils.zipBuilder import *

class Updater:

    def Update(self, tasks):
        
        self.StartTime = self.GetTime()
        self.Tasks = tasks
        
        #stop if no working vpn connection
        if not self.TestVPN():
            return
        
        #create ZIP files 
        zipBuilderObj = ZipBuilder(tasks)
        zipBuilderObj.CreateZipFiles()
        
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

        print('Starting distribution for', task.Program, task.Environment)

        #get updatefolderpath and zipfilepath from timestamp
        task.UpdateFolderPath = task.GetUpdateFolderPath(timeSuffix)
        task.ZipFileCopyDstPath = os.path.join(updateFolder, os.path.basename(task.ZipFileCopySrcPath))

        #copy zip to server, but only once per program/version/server
        #i.e. if 2 envs on 1 server need the same binaries, copy zip once and use for both envs
        copiedBefore, fileToUnzip = self.HasProgramBeenCopiedToServer(task)
        doUnzip = False
        if copiedBefore:
            #copying not needed, proceed to unzip file
            doUnzip = True
        else:
            #do copy
            copySuccess = self.CopyZipToServer(task)
            #proceed with unzip if copy successful
            doUnzip = copySuccess
            
        #unzip on server
        if doUnzip:
            unzipperObj = Unzipper()
            unzipperObj.UnzipOnServer(task)

            #TODO NEXT:
            #unzip into live folder
            #print('Proceeding to unzip in update folder: ', environment, program)
            #self.Unpack(fileToUnzip, liveFolder)
        
        print("---END OF TASK---")

    def HasProgramBeenCopiedToServer(self, thistask):
        for task in self.Tasks:
            sameProgram = task.Program == thistask.Program
            sameVersion = task.Version == thistask.Verion
            sameServer = task.Server == thistask.Server
            if task.HasZipBeenCopiedToServer and sameProgram and sameVersion and sameServer:
                #found match
                return true, task.ZipFileCopyDstPath
        #if we are here, no match
        return false, None

    def CopyZipToServer(self, task):
        copysrc = task.ZipFileCopySrcPath
        copydst = task.ZipFileCopyDstPath
        
        #ensure copydst exists
        os.makedirs(os.path.dirname(copydst), exist_ok=True)

        print('Copying ZIP to update folder...')
        print('xcopy src:', copysrc)
        print('xcopy dst:', copydst)
        print('filesize:', os.path.getsize(copysrc))

        success = False
        try:
            subprocess.call('xcopy.exe "%s" "%s*" /q /j' % (copysrc, copydst))
            #success
            success = True
            task.HasZipBeenCopiedToServer = True
        except Exception as e:
            print('ERROR ----- Exception while copying ZIP to update folder. Be sure to check that your VPN is working correctly. Exception message: ' + str(e))
        if success:
            print('...complete. ')

        return success

    def GetTime(self):
        date = datetime.today().strftime('%Y%m%d')
        time = datetime.today().strftime('%H%M')
        result = date+"_"+time
        print(result)
        return result
        
    