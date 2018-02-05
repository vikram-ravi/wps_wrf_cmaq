# -*- coding: utf-8 -*-
"""
Created on Sun Feb 04 19:05:30 2018

Author: Vikram Ravi
Description: Two classes WPSJob and WRFJob that create two qsub job scripts

"""

class WPSJob:
    
    def __init__(self, wpsDir, workDir, geogrid=True, ungrib=True, metgrid=True):
        self.runGeogrid = geogrid
        self.runUngrib  = ungrib
        self.runMetgrid = metgrid
        self.wpsDir  = wpsDir
        self.workDir = workDir
    
    def writeQsubScript(self, dateTimeTag = None, walltime='01:00:00', nodesProcs=[1,1], memory='300gb', HRRRxDir=None):
        # scriptname 
        qsubScriptName = '{workDir}/{scriptName}'.format(workDir=self.workDir, scriptName='qsub_WPS.csh')
        qsubScript = open(qsubScriptName, 'w')

        # qsub file header        
        logFileName = 'WPS_GEOGRID-{}_UNGRIB-{}_METGRID-{}_{}.log'.format( self.runGeogrid, 
                                                                           self.runUngrib, 
                                                                           self.runMetgrid,
                                                                           dateTimeTag )
        qsubHeader = ['#!/bin/csh -f',
                      '#PBS -N WPS-{}'.format(dateTimeTag),
                      '#PBS -q lar',
                      '#PBS -l walltime={}'.format(walltime),
                      '#PBS -l nodes={}:ppn={},mem={}'.format(nodesProcs[0], nodesProcs[1], memory),
                      '#PBS -j oe',
                      '#PBS -o {workDir}/{log}'.format(workDir=self.workDir, log=logFileName),
                      '#PBS -m abe',
                      '#PBS -M vikram.ravi@wsu.edu',
                      '########## END OF PBS OPTIONS ##########\n']
                      
        qsubScript.writelines("\n".join(qsubHeader))
        qsubScript.writelines("\n\n")      
        
        qsubScript.writelines('setenv PBS_O_WORKDIR {}\n'.format(self.workDir))
        qsubScript.writelines('cd  $PBS_O_WORKDIR\n')
        qsubScript.writelines('set run_status = 0 \n')
        qsubScript.writelines("#####################################\n\n\n")

        # if running GEOGRID, write relevant comands to the qsub                 
        if self.runGeogrid:
            #create soft link to the directory where geogrid is run
            geogridList = []
            geogridList.append('if $run_status == 0 then')
            geogridList.append('  echo *****************')
            geogridList.append('  echo RUNNING GEOGRID')
            geogridList.append('  echo *****************')
            geogridList.append('  #Linking to the GEOGRID.TBL')
            geogridList.append('  echo `ln -sf {wpsDir}/geogrid/GEOGRID.TBL {workDir}`'.format(wpsDir=self.wpsDir, \
                                                                                         workDir=self.workDir))
            geogridList.append('  echo `ln -sf {wpsDir}/geogrid/geogrid.exe {workDir}`'.format(wpsDir=self.wpsDir, \
                                                                                         workDir=self.workDir))
            mpiCommand = '  time /opt/openmpi-pgi/1.6/bin//mpirun {workDir}/geogrid.exe'.format(workDir=self.workDir)
            geogridList.append(mpiCommand)
            geogridList.append('  set run_status = $?')
            geogridList.append('endif')
            qsubScript.writelines("\n".join(geogridList))
            qsubScript.writelines("\n\n")
            qsubScript.writelines("#####################################\n")
            
        # if running UNGRIB, write relevant comands to the qsub                     
        if self.runUngrib:
            ungribList = []
            VtableLocation = '{wpsDir}/ungrib/Variable_Tables/Vtable.raphrrr.airpactfire'.format(wpsDir=self.wpsDir)
            gribFileName = '{hrrrxDir}/{dateTimeTag}.airpact'.format(hrrrxDir=HRRRxDir, dateTimeTag=dateTimeTag)

            ungribList.append('if $run_status == 0 then')
            #link to the Vtable
            ungribList.append('  echo `ln -sf  {VtableLocation} {workDir}/Vtable`'.format(VtableLocation=VtableLocation, \
                                                                                          workDir=self.workDir))
            # since we will run one ungrib at a time, just create a link as GRIB.AAA                                                                                                           
            ungribList.append('  echo `ln -sf {gribFileName} {workDir}/GRIBFILE.AAA`'.format(gribFileName=gribFileName, \
                                                                                             workDir=self.workDir))
    
            # create softlink to workdirectory and run ungrib
            ungribList.append('  echo ln -sf {wpsDir}/ungrib.exe {workDir}/'.format(wpsDir=self.wpsDir, 
                                                                                    workDir = self.workDir))
            ungribList.append('  echo *************************************************')
            ungribList.append('  echo RUNNING UNGRIB ON {dateTimeTag}'.format(dateTimeTag=dateTimeTag))
            ungribList.append('  echo *************************************************')
            ungribList.append('  time {workDir}/ungrib.exe'.format(workDir=self.workDir))
            ungribList.append('  set run_status = $?')
            ungribList.append('endif')
            
            qsubScript.writelines("\n".join(ungribList))
            qsubScript.writelines("\n\n")
            qsubScript.writelines("#####################################\n")
            
        if self.runMetgrid:
            metgridList = []
            metgridTable = '{wpsDir}/metgrid/METGRID.TBL.ARW.rap'.format(wpsDir=self.wpsDir)

            metgridList.append('if $run_status == 0 then')
            metgridList.append("  #link files an run program")
            metgridList.append('  echo Linking to METGRID.TBL')
            metgridList.append('  echo `ln -sf {metgridTable} {workDir}/METGRID.TBL`'.format(metgridTable=metgridTable, \
                                                                                             workDir=self.workDir))
            metgridList.append('  echo `ln -sf {wpsDir}/metgrid.exe {workDir}/ `'.format(wpsDir=self.wpsDir, 
                                                                                         workDir = self.workDir))
            metgridList.append('  echo *************************************************')
            metgridList.append('  echo RUNNING METGRID ON {dateTimeTag}'.format(dateTimeTag=dateTimeTag))
            metgridList.append('  echo *************************************************')
            metgridList.append('  time {workDir}/metgrid.exe'.format(workDir=self.workDir))
            metgridList.append('  set run_status = $?')
            metgridList.append('endif')
            
            qsubScript.writelines("\n".join(metgridList))
            qsubScript.writelines("\n\n") 
            qsubScript.writelines('exit $run_status \n')
            qsubScript.writelines("#####################################\n")
            
        qsubScript.close()
        
        return qsubScriptName
        
if __name__ == "__main__":
    
        job = WPSJob(geogrid=True, ungrib=True, metgrid=True,
                     wpsDir=r'C:/Users/vik/Desktop', 
                     workDir=r'C:/Users/vik/Desktop')
        job.writeQsubScript()
