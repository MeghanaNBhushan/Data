'''
Created on 19.10.2021

@author: BAD2LR
'''

from timeit import default_timer as timer
from datetime import timedelta

class CExecutionTime():
    def __init__(self):
        self.startTimer = 0
        self.endTimer = 0
    
    def startMeasurement(self):
        self.startTimer = timer()
        
    def stopMeasurement(self):
        self.endTimer = timer()
        
    def getElapsedTime(self):
        return timedelta(seconds = (self.endTimer - self.startTimer))
    
    def measureFunctionTime(self, function):
        self.startMeasurement()
        
        # execute the provided function and return its result
        result = function()
        
        self.stopMeasurement()
        
        return self.getElapsedTime(), result
        