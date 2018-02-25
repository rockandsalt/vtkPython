# -*- coding: utf-8 -*-

import configparser
import copy

FillEnum = ['black', 'checker_board']
Default_Slice_Setting = {'fill': FillEnum[0], 'layer_thickness': 0.1}
Default_Printer_Setting = {'printbedsize': [10,10]}
Default_Versa3d_Setting = {'unit':'mm'}

class config():
    
    def __init__(self, FilePath):
        
        self._FilePath = FilePath

        self.SlicingSettings = {}
        self.Versa3dSettings ={}
        self.PrinterSettings = {}

        self._configFile = None
        self._configParse = None
        try:
            self.readConfigFile()
        except IOError:
            self.createConfigFile()
            
    def createConfigFile(self):
        #create config        
        self.setDefaultValue()
        self.saveConfig()
        
    def setDefaultValue(self):
        self.SlicingSettings = copy.deepcopy(Default_Slice_Setting)
        self.Versa3dSettings = copy.deepcopy(Default_Versa3d_Setting)
        self.PrinterSettings = copy.deepcopy(Default_Printer_Setting)
    
    def readConfigFile(self):
        self._configFile = open(self._FilePath, 'r')
        self._configParse = configparser.ConfigParser()
        
        self._configParse.read_file(self._configFile)

        for section in self._configParse.sections():
            for key in self._configParse[section]:
                configdic = getattr(self, section)
                configdic[key] = self._configParse[section][key]

        self._configFile.close() 
    
    def getValue(self,configKey):
        
        if(configKey in self.Versa3dSettings.keys()):
            return self.Versa3dSettings[configKey]
        elif(configKey in self.PrinterSettings.keys()):
            return self.PrinterSettings[configKey]
        elif(configKey in self.SlicingSettings.keys()):
            return self.SlicingSettings[configKey]
        else:
            return ''

    def setValue(self, configKey,value):
        if(configKey in self.Versa3dSettings.keys()):
            self.Versa3dSettings[configKey] = value
            return self.Versa3dSettings[configKey] 
        elif(configKey in self.PrinterSettings.keys()):
            self.PrinterSettings[configKey] = value
            return self.PrinterSettings[configKey]
        elif(configKey in self.SlicingSettings.keys()):
            self.SlicingSettings[configKey] = value
            return self.SlicingSettings[configKey]
        else:
            return ''
    
    def saveConfig(self):
        self._configParse = configparser.ConfigParser()

        self._configParse['Versa3dSettings'] = self.Versa3dSettings      
        self._configParse['SlicingSettings'] = self.SlicingSettings
        self._configParse['PrinterSettings'] = self.PrinterSettings
        
        with open(self._FilePath, 'w') as self._configFile:
            self._configParse.write(self._configFile)
        
        self._configFile.close()
    

    

    