import os

class Unzipper:

    def UnzipOnServer(self, task):

        unzipSrc = task.ZipFileCopyDstPath
        unzipDst = task.UpdateFolderPath
        server = task.Server.value

        print('Proceeding to unzip in update folder: ', task.Program, task.Environment)
        print('Sending unzip command to server...')
        print('Src: ', unzipSrc)
        print('Dst: ', unzipDst)

        #get path to unzip.bat
        batpath = r"c:\users\josn\desktop\cd\unzip.bat"
        
        #call unzip bat, which does powershell unzip on server
        cmd = r"%s %s %s %s" % (batpath, unzipSrc, unzipDst, server)
        os.system(cmd)
        
        print('...unzip complete.')
        
