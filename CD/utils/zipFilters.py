from utils.paths import Programs
import os
        
def FilterDir(task):
    print('Collecting files to zip for {} {}...'.format(task.Program, task.Version))
    program = task.Program
    result = []
    if program == Programs.Client:
        result = FilterDirForClientSoftware(task.BinSourcePath)
    elif program == Programs.WebService:
        result = FilterDirForWebService(task.BinSourcePath)
    print('...done.')
    return result
   
def FilterDirForWebService(sourcepath):
    """
    Take everything except web.config
    """
    result = []
    dir_list = os.listdir(sourcepath)
    for item in dir_list:
        abspath = os.path.join(sourcepath, item)
        #files
        if os.path.isfile(abspath):
            #anything but webconfig
            if os.path.basename(item).lower() == "web.config":
                continue
            #also skip other zips
            elif os.path.basename(item).lower().endswith("zip"):
                continue
            else:
                result.append(abspath)
        #folders
        elif os.path.isdir(abspath):
            result.append(abspath)
            #get everything inside the folder
            result.extend(GetAllFolderContent(abspath))
    return result

def FilterDirForClientSoftware(sourcepath):
    """
    Pass the following items:
    -folders: DLL, Documents, EmbeddedResources
    -filetypes .exe, .dat, .dll, .lib, .pak, .pdb
    -file: version.txt
    """
    result = []
    filetypes = [".exe", ".dat",  ".dll", ".lib", ".pdb"]
    folders = ["dll", "documents", "embeddedresources"]
    dir_list = os.listdir(sourcepath)
    for item in dir_list:
        abspath = os.path.join(sourcepath, item)
        #files
        if os.path.isfile(abspath):
            if os.path.basename(abspath).lower() == "version.txt":
                result.append(abspath)
            else:
                filename, file_extension = os.path.splitext(abspath)
                if file_extension.lower() in filetypes:
                    result.append(abspath)
        #folders
        elif os.path.isdir(abspath):
            if os.path.basename(abspath).lower() in folders:
                result.append(abspath)
                #get everything inside the folder
                result.extend(GetAllFolderContent(abspath))
    return result

def GetAllFolderContent(rootdir):
    result = []
    for root, folders, files in os.walk(rootdir):
        for item in folders:
            abspath = os.path.join(root, item)
            result.append(abspath)
        for item in files:
            abspath = os.path.join(root, item)
            result.append(abspath)
    return result
    
