#!/usr/bin/python
"""
Author - Vikram ravi
Description - job to submit qsub jobs, overcomes PBS -o and -e options errors when passing command line arguments    USAGE - python submit_qsub_wps.py year month day inithour endhour
        no preeciding zeros for any arguments: instead of MONTH = 08, use 8
"""
# import necessary modules
import os
import sys
from datetime import datetime, timedelta
from collections import OrderedDict
from wpsWRFNamelist import WPSNameList
from wpsWRFJobs import WPSJob

###########################################
# read the argumenys
if (len(sys.argv) == 6):
   iYear   = int(sys.argv[1])  #2017
   iMonth  = int(sys.argv[2])  #5
   iDay    = int(sys.argv[3])  #5
   iHour   = int(sys.argv[4])  #0
   fHours  = int(sys.argv[5])  #18
else:
   print ('error in arguments of %s\n'%(sys.argv[0]))
   print ('number of arguments passed = %s'%(len(sys.argv)))
   print ('correct use is....')
   print ('python submit_qsub_wps.py year month day inithour fcsthours')

############################################
# USER INPUTS
############################################

# whether to run GEOGRID, UNGRIB and METGRID
runGeogrid = True
runUngrib  = True
runMetgrid = True

# set following as per job requirements
walltime   = '01:00:00'
nodesProcs = [1,1]
memoryInGB = '5gb'

# data or executable locations
HRRRxDir  = '/data/lar/users/vikram.ravi/HRRR/hrrr_from_ESRL/wrfnat_for_september2017_simulations/'
HRRRxDir  = '/data/lar/users/vikram.ravi/HRRR/hrrr_from_ESRL/wrfnat/'
outputDir = '/data/lar/users/vikram.ravi/HRRR/WRF_RUNS/'
wpsDir    = '/home/vikram.ravi/models/WRF3.9.1.1/WPS/' 

# define the static components of WPS namelist
# hour specific namelist will be changed below 
# while submitting jobs for each hour
nameList = OrderedDict( [ 
                # shared options
                ('core'              , 'ARW'             ),
                ('maxDomains'        , 2                 ),
                ('startDate'         , [2011, 2012, 2013]),
                ('endDate'           , [2011, 2012, 2013]),
                ('intervalSeconds'   , 21000             ),
                ('ioFormGeogrid'     , 2                 ),
                ('geogridOutPath'    , 'workDir'         ),
                ('debugLevel'        , 2                 ),
                
                # geogrid options
                ('parentID'          , [1,2,3]           ),
                ('parentGridRatio'   , [1,2,3]           ),
                ('iParentStart'      , [1,31, 22]        ),
                ('jParentStart'      , [1,31, 22]        ),
                ('extentWestEast'    , [285, 200, 100]  ),
                ('extentSouthNorth'  , [158, 200, 100]  ),
                ('geogDataResolution', ['modis_lakes+30s', 'default', 'default']),
                ('cellSizeX'         , [4000, 12, 4]     ),
                ('cellSizeY'         , [4000, 12, 4]     ),
                ('mapProjection'     , 'lambert'         ),
                ('referenceLatitude' , 45.35041          ),
                ('referenceLongitude', -118.9322         ),
                ('trueLatitude1'     , 30.0              ),
                ('trueLatitude2'     , 60.0              ),
                ('standardLongitude' , -121.0            ),
                ('geogDataPath'      , 'workDir'         ),
                ('geogTablePath'     , 'workDir'         ),

                # ungrib options
                ('ungribFormat'      , 'WPS'             ),
                ('ungribPrefix'      , 'HRRR2WRF'        ),

                # metgrid options                
                ('gribFileName'      , 'HRRR2WRF'        ),
                ('ioFormMetgrid'     , 2                 ),
                ('metgridOutPath'    , 'workDir'         ),
                ('metgridTablePath'  , 'workDir'         ) ] )

###########################################
# END OF USER INPUTS
##########################################
iDateTime = datetime(iYear, iMonth, iDay, iHour)

for fHour in range(fHours):

    #define and create working dir
    #workDir = outputDir + '/{IY}{IM}{ID}/{IH}/wps_{FH}/'.format(IY=iYear, IM=iMonth, ID=iDay, IH=iHour, FH=fHour)
    workDir = outputDir + '/{:04}{:02}{:02}/{:02}/wps_{:02}/'.format(iYear, iMonth, iDay, iHour, fHour)
    if not os.path.exists(workDir):
        os.system( 'mkdir -p {}'.format(workDir) )

   # modify namelist
    sDate = iDateTime + timedelta(hours = fHour)
    eDate = iDateTime + timedelta(hours = fHour+1)
    dateTimeTag = sDate.strftime('%y%j%H00') + sDate.strftime('%H00') # 1730401000000.airpact
    nameList[ 'startDate' ]      = '{:04}-{:02}-{:02}_{:02}:00:00'.format(sDate.year, sDate.month, sDate.day, sDate.hour)
    nameList[ 'endDate'   ]      = '{:04}-{:02}-{:02}_{:02}:00:00'.format(eDate.year, eDate.month, eDate.day, eDate.hour)
    nameList['geogridOutPath']   = workDir
    nameList['geogTablePath']    = workDir
    nameList['metgridOutPath']   = workDir
    nameList['metgridTablePath'] = workDir

    # create the namelist file in workDir
    nml_fHour = WPSNameList(nameListParameters=nameList, WPS_run_dir=workDir)
    nml_fHour.writeWPSNameList()

    # create and instance of the WPS job
    job_fHour = WPSJob( geogrid = runGeogrid, 
                        ungrib  = runUngrib, 
                        metgrid = runMetgrid,
                        wpsDir  = wpsDir, 
                        workDir = workDir )

    #get the qsub script
    qsubScript = job_fHour.writeQsubScript( dateTimeTag = dateTimeTag,
                                            walltime    = walltime, 
                                            nodesProcs  = nodesProcs, 
                                            memory      = memoryInGB, 
                                            HRRRxDir    = HRRRxDir )
    # submit the job
    os.system('chmod 700 {}'.format(qsubScript))
    jobCommand = 'qsub -V {}'.format(qsubScript)
    #os.system(jobCommand)
