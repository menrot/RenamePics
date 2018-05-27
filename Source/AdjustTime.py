# Change Exif DateTime to be local to location based on date travelled
# July - Iceland
# Auguist - Europe
# The original time are in Israel

import os
import piexif
from PIL import Image


MyDebug = False

# get folder name
# os.chdir(os.path.join(os.environ['USERPROFILE'], "Google Drive\\My Pictures"))
os.chdir("D:\\users\\menashe\\G Drive\\My Pictures")

foldername = raw_input("Enter folder name: ")
if len(foldername) == 0:
    foldername = "data"

try:
    filenames = next(os.walk(foldername))[2]
except:
    print("No folder")
    exit(1)

os.chdir(foldername)

print "*** Start Modifying ***"

for j in range(0, len(filenames)):

    # Display progrees
    print "\r{0:02d}%".format(j * 100 / len(filenames)),

    if (filenames[j][-4:].upper() == '.JPG'):
        img = Image.open(filenames[j])
        exif_dict = piexif.load(img.info['exif'])

        # OffsetDateTimeOriginal
        tempStr = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]

        # Calculate offset
        #   in July -> 3 hours (Iceland)
        #   in Aug -> 2 hours (Europe)
        if int(tempStr[5:7]) == 7:
            offset = 3
        elif int(tempStr[5:7]) == 8:
            offset = 1
        else:
            offset = 0
            print "** No Offset ", filenames[j], tempStr

        #use format to keep it 2 digits
        if int(tempStr[11:13]) >= offset:
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = \
                tempStr[:11] + '{0:02d}'.format(int(tempStr[11:13]) - offset) + tempStr[13:]
        else:
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = \
                tempStr[:8] + '{0:02d}'.format(int(tempStr[8:10])-1)+ " " + '{0:02d}'.format(int(tempStr[11:13]) - offset + 24) + tempStr[13:]

        # OffsetDateTimeDigitized
        tempStr = exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized]

        # Calculate offset
        #   in July -> 3 hours (Iceland)
        #   in Aug -> 2 hours (Europe)
        if int(tempStr[5:7]) == 7:
            offset = 3
        elif int(tempStr[5:7]) == 8:
            offset = 1
        else:
            offset = 0
            print "** No Offset ", filenames[j], tempStr

        if int(tempStr[11:13]) >= offset:
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = tempStr[:11] + '{0:02d}'.format(int(tempStr[11:13]) - offset) + tempStr[13:]
        else:
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = tempStr[:8] + '{0:02d}'.format(int(tempStr[8:10])-1)+ " " + '{0:02d}'.format(int(tempStr[11:13]) - offset + 24) + tempStr[13:]



        #Store the updated time
        exif_bytes = piexif.dump(exif_dict)
        img.save('_%s' % filenames[j][:-4] + ".JPG", "jpeg", exif=exif_bytes)
