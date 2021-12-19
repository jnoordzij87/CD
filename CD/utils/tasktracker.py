class TaskTracker:

    def __init__(self):
        #things to track
        self.Program = None
        self.Version = None
        self.Environment = None
        self.Server = None
        self.BinSourcePath = None
        self.ZipFileCopySrcPath = None
        self.ZipFileCopyDstPath = None
        self.UpdateFolderPath = None
        self.LiveFolderPath = None
        self.HasZipBeenCopiedToServer = None