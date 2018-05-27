import sys, os
from win32com.shell import shell, shellcon



def GetFolderAndPIDLForPath(filename):
    desktop = shell.SHGetDesktopFolder()
    info = desktop.ParseDisplayName(0, None, os.path.abspath(filename))
    cchEaten, pidl, attr = info
    # We must walk the ID list, looking for one child at a time.
    folder = desktop
    while len(pidl) > 1:
        this = pidl.pop(0)
        folder = folder.BindToObject([this], None, shell.IID_IShellFolder)
    # We are left with the pidl for the specific item.  Leave it as
    # a list, so it remains a valid PIDL.
    return folder, pidl


os.chdir("D:\\users\\menashe\\mG Drive\\My Pictures")

foldername = raw_input("Enter folder name: ")
if len(foldername) == 0:
    foldername = "data"

try:
    filenames = next(os.walk(foldername))[2]
except:
    print("No folder")
    exit(1)

os.chdir(foldername)

ItineraryFile = raw_input("Enter initerary file name (Date, Location): ")
if len(ItineraryFile) == 0:
    ItineraryFile = "IMAG2790.jpg"
folder, pidl = GetFolderAndPIDLForPath(ItineraryFile)
print folder, pidl



