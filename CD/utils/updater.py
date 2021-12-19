from datetime import datetime
import os
from utils.paths import *
from zipfile import ZipFile
import zipfile
import glob
from shutil import *
import subprocess
from subprocess import *
import utils.unzipper
from utils.zipFilters import *
import utils.zipBuilder

class Updater:

    def __init__(self):
        self.CopiedZips = {}
        pass
    
    def Update(self, tasks, sources):
        """
        Prepares and executes copy.
        Tasks = a list of strings like ["1.1", "1.2", .. ]
        Sources = a dict containing sourcedirectories indexed by program
        """
  
        #Sources example
        #sources[Programs.Client] = C:\VS\AzureRepos\RESuite\bin\Debug
        #sources[Programs.Webservice] = \\pc-12\temp\publish
        
        self.StartTime = self.GetTime()
        self.Tasks = tasks
        self.Sources = sources
        
        #stop if no working vpn connection
        if not self.TestVPN():
            return
        
        #create ZIP files 
        self.CreateZipFiles()
        
        #execute tasks 
        for taskId in tasks:
           task = self.ParseAndExecuteTask(taskId)

        print('All tasks completed.')
    
    def TestVPN(self):
        print('Testing VPN...')
        if not os.path.exists(r"\\demo-ts-2\DEMO\Demonstratie"):
            print('...VPN not working, aborted!')
            return False
        else:
            print('...working.')
            return True

    def ParseAndExecuteTask(self, taskId):
    
        if not self.IsValidTask(taskId):
            return
        
        #get program id & environment Id from taskId
        programId, envId = taskId.split(".")
        
        #get program and environment from enum by id
        program = Programs(int(programId))
        environment = Environments(int(envId))
        
        #get versionkey by environment
        version = self.GetVersionKeyByEnvironment(environment)
        
        print('Starting distribution for', program, environment)

        #get path of update folder
        updateFolder = self.GetUpdateFolder(program, environment) # need real enum here, not string, fix mess later
        timeSuffix = self.StartTime
        updateFolder = os.path.join(updateFolder, timeSuffix) # need real enum here, not string, fix mess later
                
        #get path of live folder 
        liveFolder = self.GetLiveFolder(program, environment)
        
        #get zip source and dest paths
        zip_src_fpath = self.ZipfileLookup[str(version)][str(program)].filename
        zip_dst_fpath = os.path.join(updateFolder, os.path.basename(zip_src_fpath))

        #copy zip to server, only once
        server = self.GetServerFromPath(zip_dst_fpath)
        hasProgramUpdateBeenCopiedToServer = self.HasProgramUpdateBeenCopiedToServer(program, version, server)
        copySuccess = False
        doUnzip = False
        if hasProgramUpdateBeenCopiedToServer:
            #copying not needed, proceed to unzip file
            doUnzip = True
        else:
            #copy
            copySuccess = self.CopyZipToServer(program, version, server, zip_src_fpath, zip_dst_fpath)
            doUnzip = copySuccess
            
        #unzip on server
        if doUnzip:
            #get the file to unzip
            fileToUnzip = self.CopiedZips[program][server]
            
            #unzip into update folder
            print('Proceeding to unzip in update folder: ', environment, program)
            self.UnzipOnServer(fileToUnzip, updateFolder)
            
            #unzip into live folder
            #print('Proceeding to unzip in update folder: ', environment, program)
            #self.Unpack(fileToUnzip, liveFolder)
        
        print("---END OF TASK---")

    def GetVersionKeyByEnvironment(self, environment):
        # the idea is to return prerelease version string for any prerelease environment
        # otherwise return release
        if "PreRelease" in str(environment):
            return str(Versions.PreRelease)
        else:
            return str(Versions.Release)

    def HasProgramUpdateBeenCopiedToServer(self, program, version, server):
        #copied zips are stored like this: CopiedZips[program][server] = zip_dst_fpath
        if not program in self.CopiedZips or not version in self.CopiedZips[program] or not server in self.CopiedZips[program][version]:
            return False
        else:
            return True

    def UnzipOnServer(self, zipfile, unpackdir):
        server = self.GetServerFromPath(zipfile)
        unzipper = Unzipper.Unzipper()
        unzipper.UnzipOnServer(server, zipfile, unpackdir)

    def CopyZipToServer(self, program, version, server, zip_src_fpath, zip_dst_fpath):
        success = False
        
        #copy zip to server
        copysuccess = self.Copy(zip_src_fpath, zip_dst_fpath)

        if copysuccess:
            success = True

            #store the zip location
            if not program in self.CopiedZips:
                self.CopiedZips[program] = {}
            if not version in self.CopiedZips[program]:
                self.CopiedZips[program][version] = {}
            self.CopiedZips[program][version][server] = zip_dst_fpath
                
        return success

    def Copy(self, zip_src_fpath, zip_dst_fpath):
    
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

    def GetLiveFolder(self, program, environment):
        if program == Programs.Client:
            return ClientSoftwareLiveFolderPaths[environment]
        elif program == Programs.WebService:
            return WebServiceLiveFolderPaths[environment]
        #todo : add RE_Suite service etc

    def GetUpdateFolder(self, program, environment):
        if program == Programs.Client:
            return ClientSoftwareUpdateFolderPaths[environment]
        elif program == Programs.WebService:
            return WebServiceUpdateFolderPaths[environment]
        #todo : add RE_Suite service etc

    def CreateZipFiles(self):
        #make a lookup for created zipfiles so we can access them later
        self.ZipfileLookup = {}
        for version, dict in self.Sources.items():
            for program, sourcepath in dict.items():
                #continue only if valid sourcepath
                if sourcepath:
                    #get files to zip
                    filesToZip = FilterDir(sourcepath, program, version)
                    #create zip
                    zipFile = self.CreateZipFile(sourcepath, filesToZip, program, version)
                    #add to lookup
                    self.AddZipfileToLookup(zipFile, version, program)
                    

    def AddZipfileToLookup(self, zipFile, version, program):
        #ensure lookup keys exist
        if not version in self.ZipfileLookup:
            self.ZipfileLookup[version] = {}  
        self.ZipfileLookup[version][program] = zipFile
            
    def CreateZipFile(self, sourcepath, filesToZip, program, version):
        print("Building ZIP for {} {} ...".format(program, version))
        zipfilepath = os.path.join(sourcepath, (self.StartTime + ".zip"))
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
        
    def IsValidTask(self, taskId):
        #tasks should be in form of 1.1 / 1.2 / etc
        return ("." in taskId)
        
    def GetServerFromPath(self, path):
        for server in Servers:
            if server.value in path:
                return server.value