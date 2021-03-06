## Rename pictures based on Itinerary file and sequential order at each location.
##
##
# 1. In itinerary two successive lines have to have different names
# 2. The second column has the start DateTime of that location
# 3. First row is the default
###

import os
import sys
import exifread
import csv
import pickle
import argparse
import re
from datetime import datetime


class DateTime(object):

    def __init__(self, value):
        self.values = value
        self.printable = str(value)
        return


## Get the Image time "Exif" time
class ImageFileData(object):

    def __init__(self, path, filename):

        self.OriginalName = filename

        try:
            fullPath = path + '\\' + filename
            f = open(fullPath, 'rb')

            # for Exif tags description see:
            #   https: // sno.phy.queensu.ca / ~phil / exiftool / TagNames / EXIF.html
            #   https://pypi.python.org/pypi/ExifRead
            #

            self.DateTime = DateTime(u'1900:01:01 01:01:01')
            tags = exifread.process_file(f)
            DateFlag = False

            try:
                self.DateTime = tags.__getitem__('EXIF DateTimeOriginal')
            except:
                try:
                    self.DateTime = tags.__getitem__('EXIF DateTimeDigitized')
                    writeLog("Use Digitized DateTime" + repr(filename))
                except:
                    try:
                        self.DateTime = tags.__getitem__("Image DateTime")
                        writeLog("Use Image DateTime " + repr(filename))
                    except:
                        # writeLog("No DateTime property " + repr(filename))
                        regex_YYYYMMDD = u'([0-9]{4})(((0[13578]|(10|12))(0[1-9]|[1-2][0-9]|3[0-1]))|(02(0[1-9]|[1-2][0-9]))|((0[469]|11)(0[1-9]|[1-2][0-9]|30)))'
                        m = re.search(regex_YYYYMMDD, filename)
                        if not (m is None):
                            s = m.start()
                            self.DateTime.values = u'%s:%s:%s 12:00:00' % (
                            filename[s:s + 4], filename[s + 4:s + 6], filename[s + 6:s + 8])
                            self.DateTime.printable = str(self.DateTime.values)
                        else:
                            try:
                                fileTime = min(os.path.getctime(fullPath), os.path.getmtime(
                                    fullPath))  # the earliest from creation and modification
                                self.DateTime.values = datetime.fromtimestamp(fileTime).strftime("%Y:%m:%d %I:%M:%S")
                                self.DateTime.printable = str(self.DateTime.values)
                            except:
                                raise ValueError('No EXIF and no match for date in file name')

            self.Date = self.DateTime.printable[0:4] + '-' + self.DateTime.printable[
                                                             5:7] + '-' + self.DateTime.printable[8:10]

            try:
                if (tags.__getitem__('Image Make').printable == "HUAWEI"):
                    try:
                        GPSTime = tags.__getitem__("GPS GPSTimeStamp").values
                        TimeStr = '{0:02d}:'.format(int(str(GPSTime[0]))) + '{0:02d}:'.format(
                            int(str(GPSTime[1]))) + '{0:02d}'.format(int(str(GPSTime[2])))
                        if (TimeStr[0:5] != self.DateTime.printable[11:16]):  # compare HH:MM
                            writeLog("HUAWEI modified by GPS time " + repr(
                                filename) + '  GPS:' + TimeStr + '  Time:' + self.DateTime.printable[11:19])
                            self.DateTime.values = unicode(self.DateTime.values[:11] + TimeStr)
                            self.DateTime.printable = str(self.DateTime.values)
                    except:
                        pass

            #           GPS_Lat = tags.__getitem__('GPSLatitude')
            #           GPS_Long = tags.__getitem__('GPSLongitutde')
            except Exception as ex:
                pass  # no EXIF

            self.Location = ""
            self.NewName = ""

            self.Ignore = False

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            writeLog(message + " " + repr(filename))
            self.Ignore = True

        return (None)

    def __repr__(self):
        return '{}: {}   {}\n'.format(self.DateTime.values, self.OriginalName, self.NewName)

    def giveNames(self):

        return ()


def getKeyImage(ImageFileData):
    return ImageFileData.DateTime.values


def getKeyItinerary(item):
    return item[0]


def writeLog(*args):
    logFile.write(*args)
    logFile.write('\n')
    print("\n", args)
    return


MyDebug = False

### Usage RenamePics.py RootFolder -i RelativeInputFolder -o RelativeOutputFolder -I itineraryFile  -P  -R
parser = argparse.ArgumentParser(description='Rename Pics in INPUT based on ITINERARY and move files to OUTPUT')
parser.add_argument('RootFolder', metavar='RootFolder', type=str,
                    help='the folder in which the whole processing is done')
parser.add_argument('-i', dest='InputFolder', action='store',
                    help='Relative to root input folder name')
parser.add_argument('-o', dest='OutputFolder', action='store',
                    help='Relative to root output folder name')
parser.add_argument('-I', dest='ItineraryFile', action='store',
                    help='Itinirary file name in root folder')
parser.add_argument('-P', dest='UsePreviousFileList', action='store_true',
                    help='Use Previous list, saves processing')
parser.add_argument('-R', dest='DoRename', action='store_true',  # By default - Dont rename
                    help='When set- actually rename the files')

print(__name__)
if __name__ == '__main__':

    print('RenamePics Release 3.0')  # update release number

    MyArgs = vars(parser.parse_args())

    # create variables
    locals().update(MyArgs)

    workingDir = os.path.abspath(RootFolder)
    if InputFolder is None:
        InputFolder = 'inputPics'  # Default value
    PicInputFolder = os.path.abspath(workingDir + '\\' + InputFolder)

    if OutputFolder is None:
        OutputFolder = 'ProcessedPics'  # default value
    PicOutputFolder = os.path.abspath(workingDir + '\\' + OutputFolder)

    if ItineraryFile is None:
        ItineraryFile = 'itinerary.csv'

    origDir = os.getcwd()
    os.chdir(workingDir)

    try:
        filenames = next(os.walk(PicInputFolder))[2]
    except:
        print("No Input folder")
        exit(1)
    if len(filenames) == 0:
        print("No files in input folder")
        exit(1)

    itinerary = []

    try:
        with open(ItineraryFile, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                itinerary.append(row)

    except Exception as ex:
        print('Itinerary file exception', ex)
        exit(1)

    logFile = open(ItineraryFile[:-4] + '_log_' + datetime.now().strftime("%Y%m%d_%I%M%S") + '.log', 'w')  # Log file

    itinerary.sort(key=getKeyItinerary)
    DefaultTime = itinerary[0][0]
    DefaultLocation = itinerary[0][1]

    try:
        fpkl = open('listOfFile.pkl', 'rb')
    except:
        UsePreviousFileList = False

    if UsePreviousFileList:
        with open('listOfFile.pkl', 'rb') as fpkl:
            ListOfFiles = pickle.load(fpkl)
            fpkl.close()
    else:
        ListOfFiles = []

        for j in range(0, len(filenames)):
            if (filenames[j][-4:].upper() == '.JPG') or (filenames[j][-5:].upper() == '.JPEG'):
                print('\r{0:02f}%'.format(j * 100 / len(filenames)), )  # print progress
                tempData = ImageFileData(PicInputFolder, filenames[j])
                if not tempData.Ignore:
                    ListOfFiles.append(tempData)

        # sort the list of files
        ListOfFiles.sort(key=getKeyImage)
        with open('listOfFile.pkl', 'wb') as fpkl:
            pickle.dump(ListOfFiles, fpkl)
            fpkl.close()

    j = 0
    State = 0
    Last_i = 0
    Location = DefaultLocation
    LastDate = "1900:01:01"

    while (j < len(ListOfFiles)):

        if (ListOfFiles[j].DateTime.printable[:10] > LastDate):
            IdinDay = 1
            LastDate = ListOfFiles[j].DateTime.printable[:10]

        if MyDebug:
            print('j = ', j)

        for i in range(Last_i, len(itinerary) - 1):

            if MyDebug:
                print('    i = ', i)

            if (ListOfFiles[j].DateTime.printable < itinerary[i][0]):
                ListOfFiles[j].NewName = ListOfFiles[j].Date + ' ' + '{0:04d}'.format(IdinDay) + ' ' + Location + '.jpg'
                IdinDay = IdinDay + 1
                State = 0
                j = j + 1
                break
            elif (ListOfFiles[j].DateTime.printable < itinerary[i + 1][0]):
                if (State == 0):
                    State = 1
                    Last_i = i
                    Location = itinerary[i][1]
                ListOfFiles[j].NewName = ListOfFiles[j].Date + ' ' + '{0:04d}'.format(IdinDay) + ' ' + Location + '.jpg'
                IdinDay = IdinDay + 1
                j = j + 1
                break
            elif (ListOfFiles[j].DateTime.printable >= itinerary[len(itinerary) - 1][0]):
                # Last_i = len(itinerary)-1
                Location = itinerary[len(itinerary) - 1][1]
                ListOfFiles[j].NewName = ListOfFiles[j].Date + ' ' + '{0:04d}'.format(IdinDay) + ' ' + Location + '.jpg'
                j = j + 1
                IdinDay = IdinDay + 1
                break
            else:
                State = 0

        if MyDebug:
            print(ListOfFiles[j - 1].NewName)

    print(DoRename, "\n*** Start Renaming files ***, %s")

    for j in range(0, len(ListOfFiles)):
        try:
            if DoRename:
                os.rename(PicInputFolder + '\\' + ListOfFiles[j].OriginalName,
                          PicOutputFolder + '\\' + ListOfFiles[j].NewName)
            logFile.write(repr(ListOfFiles[j]))
            print("\r{0:02f}%".format(j * 100 / len(filenames)), )  # print progress
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = "Failed to rename " + template.format(type(ex).__name__, ex.args)
            writeLog(message + " " + repr(ListOfFiles[j]))

    f.close()
