# -*- coding: utf-8 -*-
"""
Created on Sat Feb 03 00:12:26 2018

Author: Vikram Ravi
Description: Writes a WPS namelist file
Updates:     VR: As of now, only writes for 3 maximum domains
             VR: Updated to write for as many domains as possble, 
                 but that is based on the input nameListParameters
             
"""
from collections import OrderedDict
from namelistFormatter import TypeBasedFormat

###################################################
# Module to write WPS namelist
###################################################   
class WPSNameList:
    
    def __init__(self, nameListParameters, WPS_run_dir):
        self.WPSNameList = nameListParameters
        self.WPS_run_dir = WPS_run_dir
    
    def writeWPSNameList(self):
        nameListFile = open("{}/{}".format(self.WPS_run_dir,'namelist.wps'), 'w')
    
        wpsParamsDict = {'shared':
                                 {'core'             :'wrf_core                     = ', 
                                 'maxDomains'        :'max_dom                      = ', 
                                 'startDate'         :'start_date                   = ', 
                                 'endDate'           :'end_date                     = ',
                                 'intervalSeconds'   :'interval_seconds             = ',
                                 'ioFormGeogrid'     :'io_form_geogrid              = ', 
                                 'geogridOutPath'    :'opt_output_from_geogrid_path = ', 
                                 'debugLevel'        :'debug_level                  = '},
                         'geogrid':{
                                 'parentID'          :'parent_id            = ', 
                                 'parentGridRatio'   :'parent_grid_ratio    = ', 
                                 'iParentStart'      :'i_parent_start       = ', 
                                 'jParentStart'      :'j_parent_start       = ', 
                                 'extentWestEast'    :'e_we                 = ', 
                                 'extentSouthNorth'  :'e_sn                 = ', 
                                 'geogDataResolution':'geog_data_res        = ',
                                 'cellSizeX'         :'dx                   = ', 
                                 'cellSizeY'         :'dy                   = ', 
                                 'mapProjection'     :'map_proj             = ', 
                                 'referenceLatitude' :'ref_lat              = ',
                                 'referenceLongitude':'ref_lon              = ', 
                                 'trueLatitude1'     :'true_lat1            = ', 
                                 'trueLatitude2'     :'true_lat2            = ', 
                                 'standardLongitude' :'stand_lon            = ', 
                                 'geogDataPath'      :'geog_data_path       = ', 
                                 'geogTablePath'     :'opt_geogrid_tbl_path = '},
                         'ungrib':{
                                 'ungribFormat'      :'out_format       = ', 
                                 'ungribPrefix'      :'prefix           = '},
                         'metgrid':{
                                 'gribFileName'      :'fg_name                       = ',
                                 'ioFormMetgrid'     :'io_form_metgrid               = ',
                                 'metgridOutPath'    :'opt_output_from_metgrid_path  = ', 
                                 'metgridTablePath'  :'opt_metgrid_tbl_path          = '}}
#        wpsParamsDict = OrderedDict(paramDict)
        
        sharedList  = ["&share"]
        geogridList = ["&geogrid"]
        ungribList  = ["&ungrib"]
        metgridList = ["&metgrid"]
        
        # shared part of the namelist
#        for nmlParam in nameListParameters.keys():
        for nmlParam in self.WPSNameList.keys():
            if nmlParam in wpsParamsDict['shared'].keys():
                sharedParameter = wpsParamsDict['shared'][nmlParam] + \
                                  '{}'.format(TypeBasedFormat(self.WPSNameList[nmlParam]), 'wpsnamelist')
                sharedList.append(sharedParameter)
                
            elif nmlParam in wpsParamsDict['geogrid'].keys():
                geogridParameter = wpsParamsDict['geogrid'][nmlParam] + \
                                   '{}'.format(TypeBasedFormat(self.WPSNameList[nmlParam]), 'wpsnamelist')
                geogridList.append(geogridParameter)

            elif nmlParam in wpsParamsDict['ungrib'].keys():
                ungribParameter = wpsParamsDict['ungrib'][nmlParam] + \
                                  '{}'.format(TypeBasedFormat(self.WPSNameList[nmlParam]), 'wpsnamelist')
                ungribList.append(ungribParameter)

            elif nmlParam in wpsParamsDict['metgrid'].keys():
                metgridParameter = wpsParamsDict['metgrid'][nmlParam] + \
                                   '{}'.format(TypeBasedFormat(self.WPSNameList[nmlParam]), 'wpsnamelist')
                metgridList.append(metgridParameter)

        # append the fortran namelist section end and newline char
        for appendItem in ["/", "\n"]:
            sharedList.append(appendItem)
            geogridList.append(appendItem)
            ungribList.append(appendItem)
            metgridList.append(appendItem)

        # create a single string for each part of the namelist
        sharedPart  = "\n".join(sharedList)    
        geogridPart = "\n".join(geogridList)    
        ungribPart  = "\n".join(ungribList)
        metgridPart = "\n".join(metgridList)
        
        # write to the namelist file
        nameListFile.writelines(sharedPart)
        nameListFile.writelines(geogridPart)
        nameListFile.writelines(ungribPart)
        nameListFile.writelines(metgridPart)
        nameListFile.close()

###########################
# unit test below
###########################
if __name__ == "__main__":
    
    nameListDir = r"C:\Users\vik\Desktop"
    nameList = OrderedDict([('core' , 'ARW'),
                ('maxDomains', 2),
                ('startDate', [2011, 2012, 2013]),
                ('endDate', [2011, 2012, 2013]),
                ('intervalSeconds', 21000),
                ('ioFormGeogrid',2),
                ('geogridOutPath',"C:\\Users\\vik\\Desktop"),
                ('debugLevel',2),
                
                ('parentID',[1,2,3]),
                ('parentGridRatio',[1,2,3]),
                ('iParentStart',[1,31, 22]),
                ('jParentStart',[1,31, 22]),
                ('extentWestEast',[1000, 200, 100]),
                ('extentSouthNorth',[1000, 200, 100]),
                ('geogDataResolution',['modis_lakes+30s', 'default', 'default']),
                ('cellSizeX',[36, 12, 4]),
                ('cellSizeY',[36, 12, 4]),
                ('mapProjection','lambert'),
                ('referenceLatitude',45.35041),
                ('referenceLongitude',-118.9322),
                ('trueLatitude1',30.0),
                ('trueLatitude2',60.0),
                ('standardLongitude',-121.0),
                ('geogDataPath',"C:\\Users\\vik\\Desktop"),
                ('geogTablePath',"C:\\Users\\vik\\Desktop"),
                
                ('ungribFormat','WPS'),
                ('ungribPrefix','HRRR2WRF'),
                
                ('gribFileName','HRRR2WRF'),
                ('ioFormMetgrid',2),
                ('metgridOutPath',"C:\\Users\\vik\\Desktop"),
                ('metgridTablePath', "C:\\Users\\vik\\Desktop")])
                
    WPSNameList(nameList, nameListDir).writeWPSNameList()
