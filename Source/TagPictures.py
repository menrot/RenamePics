import os
import exifread
from menrotPackage import GetFileProperties

def PrintTags(filename):
    # Open image file for reading (binary mode)
    f = open(filename, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)
    print "File ", filename
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print "Key: %s, value %s" % (tag, tags[tag])
    return()


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
os.chdir("data")

for j in range(0, len(filenames)):

    if (filenames[j][-4:].upper() == '.JPG'):
        # print "\r{0:02d}%".format(j * 100 / len(filenames)),
        # PrintTags(filenames[j])
        x = os.stat(filenames[j])
        propgenerator = GetFileProperties.property_sets(filenames[j])
        for name, properties in propgenerator:
            print name
            for k, v in properties.items():
                print "  ", k, "=>", v

    break



