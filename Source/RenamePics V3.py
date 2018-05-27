## Rename pics based on Itinerary file and sequntial order at each location.
##
##
# 1. In itinerary two successive lines have to have different names
# 2. The second column has the start DateTime of that location
# 3. First row is the default
###

import os
import exifread
import csv
import pickle


## Get the Image time "Exif" time
class ImageFileData(object):

    def __init__(self, filename):

        self.OriginalName = filename

        try:

            f = open(filename, 'rb')

            # for Exif tags description see:
            #   https: // sno.phy.queensu.ca / ~phil / exiftool / TagNames / EXIF.html
            #   https://pypi.python.org/pypi/ExifRead
            #
            tags = exifread.process_file(f)


            try:
                self.DateTime = tags.__getitem__('EXIF DateTimeOriginal')
            except:
                try:
                    self.DateTime = tags.__getitem__('EXIF DateTimeDigitized')
                    writeLog ("Use Digitized DateTime" + repr(filename))
                except:
                    self.DateTime = tags.__getitem__("Image DateTime")
                    writeLog("Use Image DateTime " + repr(filename))


            self.Date = self.DateTime.printable[0:4] + '-' + self.DateTime.printable[5:7] + '-' + self.DateTime.printable[8:10]

            if (tags.__getitem__('Image Make').printable == "HUAWEI"):
                try:
                    GPSTime = tags.__getitem__("GPS GPSTimeStamp").values
                    TimeStr = '{0:02d}:'.format(int(str(GPSTime[0]))) + '{0:02d}:'.format(int(str(GPSTime[1]))) + '{0:02d}'.format(int(str(GPSTime[2])))
                    self.DateTime.values = unicode(self.DateTime.values[:11] + TimeStr)
                    self.DateTime.printable = str(self.DateTime.values)
                except:
                    writeLog("HUAWEI but No GPS " + repr(filename))

#           GPS_Lat = tags.__getitem__('GPSLatitude')
#           GPS_Long = tags.__getitem__('GPSLongitutde')
            self.Location = ""
            self.NewName = ""

            self.Ignore = False

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            writeLog(message + " " + repr(filename))
            self.Ignore = True

        return(None)

    def __repr__(self):
        return '{}: {}   {}\n'.format(self.DateTime.values, self.OriginalName, self.NewName)

    def giveNames(self):

        return()


def getKeyImage(ImageFileData):
        return ImageFileData.DateTime.values


def getKeyItinerary(item):
    return item[0]

def writeLog(*args):
    logFile.write(*args)
    logFile.write('\n')
    print "\n",args
    return





# get folder name

MyDebug = False
UsePreviousFileList = False

# os.chdir(os.path.join(os.environ['USERPROFILE'], "Google Drive\\My Pictures"))
os.chdir("D:\\users\Menashe\G Drive\\My Pictures")

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
    ItineraryFile = "itinerary.csv"

itinerary = []

GetString = raw_input("Actually Rename? [CR for YES] ")
if len(GetString) == 0:
    DoRename = True
else:
    DoRename = False
    GetString = raw_input("Use Previous File List? [CR for NO]")
    if len(GetString) <> 0:
        UsePreviousFileList = True


with open(ItineraryFile, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        itinerary.append(row)

logFile = open(ItineraryFile[:-4] + '.log', 'w') # Log file


itinerary.sort(key=getKeyItinerary)
DefaultTime = itinerary[0][0]
DefaultLocation = itinerary[0][1]

if not(UsePreviousFileList):
    ListOfFiles = []

    for j in range(0, len(filenames)):

        if (filenames[j][-4:].upper() == '.JPG'):

            print "\r{0:02d}%".format(j*100/len(filenames)),

            tempData = ImageFileData(filenames[j])
            if not tempData.Ignore :
                ListOfFiles.append(ImageFileData(filenames[j]))


    # sort the list of files
    ListOfFiles.sort(key=getKeyImage)
    with open('listOfFile.pkl', 'wb') as fpkl:
        pickle.dump(ListOfFiles,fpkl)
        fpkl.close()

else:
    with open('listOfFile.pkl', 'rb') as fpkl:
        ListOfFiles = pickle.load(fpkl)
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
        print 'j = ', j


    for i in range(Last_i, len(itinerary)-1):


        if MyDebug:
            print '    i = ', i

        if (ListOfFiles[j].DateTime.printable < itinerary[i][0]):
            ListOfFiles[j].NewName = ListOfFiles[j].Date + ' ' + '{0:04d}'.format(IdinDay) + ' ' + Location + '.jpg'
            IdinDay = IdinDay + 1
            State = 0
            j = j + 1
            break
        elif (ListOfFiles[j].DateTime.printable < itinerary[i+1][0]):
            if (State == 0):
                State = 1
                Last_i = i
                Location = itinerary[i][1]
            ListOfFiles[j].NewName = ListOfFiles[j].Date + ' ' + '{0:04d}'.format(IdinDay) + ' ' + Location + '.jpg'
            IdinDay = IdinDay + 1
            j = j + 1
            break
        elif (ListOfFiles[j].DateTime.printable >= itinerary[len(itinerary)-1][0]):
            Last_i = len(itinerary)-1
            Location = itinerary[len(itinerary)-1][1]
            ListOfFiles[j].NewName = ListOfFiles[j].Date + ' ' + '{0:04d}'.format(IdinDay) + ' ' + Location + '.jpg'
            j = j + 1
            IdinDay = IdinDay + 1
            break
        else:
            State = 0

    if MyDebug:
        print ListOfFiles[j-1].NewName






print "\n*** Start Renaming files ***"

for j in range(0, len(ListOfFiles)):
    try:
        if DoRename:
            os.rename(ListOfFiles[j].OriginalName, ListOfFiles[j].NewName)
        logFile.write(repr(ListOfFiles[j]))
        print "\r{0:02d}%".format(j * 100 / len(filenames)),
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = "Failed to rename " + template.format(type(ex).__name__, ex.args)
        writeLog(message + " " + repr(ListOfFiles[j]))

f.close()
