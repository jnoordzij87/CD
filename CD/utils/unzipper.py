import os

class Unzipper:

    def UnzipOnServer(self, server, srczip, dstdir):
        
        print('Sending unzip command to server...')

        print('Src: ', srczip)
        print('Dst: ', dstdir)
        print('Server: ', server)

        #get path to unzip.bat
        batpath = r"c:\users\josn\desktop\cd\unzip.bat"
        
        #call unzip bat, which does powershell unzip on server
        cmd = r"%s %s %s %s" % (batpath, srczip, dstdir, server)
        os.system(cmd)
        
        print('...unzip complete.')
        

##TEST VALUES
#batpath = r"c:\users\josn\desktop\cd\tests\unzip.bat"
#src = r"c:\temp\test.zip"
#dst = r"c:\temp\jnotest"
#server = "\\" + "demo-ts-2"
#cmd = r"%s %s %s" % (batpath, src, dst)
#import os
#os.system(cmd)
#
##TEST VALUES WITH DYNAMIC SERVER
#batpath = r"c:\users\josn\desktop\cd\unzip.bat"
#src = r"c:\temp\test.zip"
#dst = r"c:\temp\jnotest"
#server = "demo-ts-2"
#cmd = r"%s %s %s %s" % (batpath, src, dst, server)
#import os
#os.system(cmd)
