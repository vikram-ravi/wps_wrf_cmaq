# -*- coding: utf-8 -*-
"""
Created on Sun Feb 04 18:50:23 2018

Author: Vikram Ravi
Description: Used in Writing a WPS or WRF namelist file
             Formats as a string based on input - whether list, ints, str, floats etc
             The idea for this class came from here: https://pyformat.info/
"""

###################################################
# Module to write in a format that depends on the 
# type: 
###################################################   

class TypeBasedFormat:
    def __init__(self, parameter):
        self.nmlParam = parameter
        
    # the to_str lambda function below converts to a string with quotation marks
    
    def __format__(self, wpsnamelist):
        to_str = lambda x: ("'"+x+"'" if isinstance(x, str) else x)    
        if isinstance(self.nmlParam, str):
            return to_str(self.nmlParam)
        elif isinstance(self.nmlParam, list) and isinstance(self.nmlParam[0], str):
            returnValue = ','.join(map(to_str,self.nmlParam))
            return returnValue
        elif isinstance(self.nmlParam, list):
            returnValue = ','.join(map(str, self.nmlParam))
            return returnValue
        else:
            return str(self.nmlParam)

######################
#unit test below
######################            
if __name__ == '__main__':
    print 'a={}'.format(TypeBasedFormat(['abracadabra', 'abbadi']), 'wpsnamelist')
    print 'a={}'.format(TypeBasedFormat([36,12,4,1.33]), 'wpsnamelist')
    print 'a={}'.format(TypeBasedFormat(['alphanumerics']), 'wpsnamelist')
    print 'a={}'.format(TypeBasedFormat(1), 'wpsnamelist')
    
