from utils.paths import *
import os

class TaskData:

    def __init__(self, taskId):

        #things to track
        self.Program = None
        self.Environment = None
        self.Version = None
        self.Server = None
        self.BinSourcePath = None
        self.UpdateFolderPath = None
        self.LiveFolderPath = None
        self.ZipFileCopySrcPath = None
        self.ZipFileCopyDstPath = None
        self.HasCreatedZip = False
        self.HasZipBeenCopiedToServer = False

        #first initialisation
        programId, envId, versionId = taskId.split(".")
        self.Program = Programs(int(programId))
        self.Environment = Environments(int(envId))
        self.Version = Versions(int(versionId))
        self.LiveFolderPath = self.GetLiveFolderPath()
        self.Server = self.GetServer()

    def GetLiveFolderPath(self):
        if self.Program == Programs.Client:
            return ClientSoftwareLiveFolderPaths[self.Environment]
        elif self.Program == Programs.WebService:
            return WebServiceLiveFolderPaths[self.Environment]
        #todo : add RE_Suite service etc

    def GetUpdateFolderPath(self, timestamp):
        if self.Program == Programs.Client:
            updatefolderbase = ClientSoftwareUpdateFolderPaths[self.Environment]
        elif self.Program == Programs.WebService:
            updatefolderbase = WebServiceUpdateFolderPaths[self.Environment]
        #todo : add RE_Suite service etc
        return os.path.join(updatefolderbase, timestamp)

    def GetServer(self):
        for server in Servers:
            #this is probably not entirely safe
            if server.value in self.LiveFolderPath: 
                return server

    def GetVersion(self):
        # this is incorrect because for ayn client we could want to release prerelease or release
        if "PreRelease" in str(self.Environment):
            return Versions.PreRelease
        else:
            return Versions.Release

    def SetBinSourcePath(self, value):
        self.BinSourcePath = value

