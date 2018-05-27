## https://mail.python.org/pipermail/python-list/2009-June/539760.html

import os, sys
from win32com.shell import shell, shellcon
import pythoncom
from win32com import storagecon

filepath = sys.argv[1]
pidl, flags = shell.SHILCreateFromPath (os.path.abspath (filepath), 0)
property_set_storage = shell.SHGetDesktopFolder().BindToStorage (
    pidl, None, pythoncom.IID_IPropertySetStorage
)
summary_info = property_set_storage.Open (
    pythoncom.FMTID_SummaryInformation,
    storagecon.STGM_READWRITE | storagecon.STGM_SHARE_EXCLUSIVE
)
summary_info.WriteMultiple ([storagecon.PIDSI_TITLE], ["BLAHBLAH2"])

