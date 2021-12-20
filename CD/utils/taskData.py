from utils.paths import *

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
        self.HasZipBeenCopiedToServer = None

        #first initialisation
        programId, envId = taskId.split(".")
        self.Program = Programs(int(programId))
        self.Environment = Environments(int(envId))
        self.Version = self.GetVersion()
        self.Server = self.GetServer()
        self.LiveFolderPath = self.GetLiveFolderPath()

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
            if server.value in self.LiveFolderPath: #this is probably not entirely safe
                return server

    def GetVersion(self):
        if "PreRelease" in str(self.Environment):
            return Versions.PreRelease
        else:
            return Versions.Release

    def SetBinSourcePath(self, value):
        self.BinSourcePath = value

