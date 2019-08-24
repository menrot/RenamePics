# RenamePics

Rename pic file names to reflect date and location

## Usage notes

The python script receives the following arguments:

Working folder  (Mandatory), and the following:

 ``-h, --help        show this help message and exit`
  `-i INPUTFOLDER    Relative to root input folder name`
  `-o OUTPUTFOLDER   Relative to root output folder name`
  `-I ITINERARYFILE  Itinirary file name in root folder`
  `-P                Use Previous list, saves processing`
  `-R                When set- actually rename the files``

A batch file supports the daily naming of pictures by camera. eg:

\root

​	\root\2019-08-04

​	\root\2019-08-05

At DOS prompt type:  _1_RenamePics_DO.bat 04



## Resulting file name

The results look like

​	2019-0804 0007 Location_Name

Order is according to the time taken

# Logic

