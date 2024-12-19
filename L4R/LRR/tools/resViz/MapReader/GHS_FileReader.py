#=============================================================================
#  C O P Y R I G H T
#-----------------------------------------------------------------------------
#  @copyright (c) 2019 - 2020 by Robert Bosch GmbH. All rights reserved.
#
#  The reproduction, distribution and utilization of this file as
#  well as the communication of its contents to others without express
#  authorization is prohibited. Offenders will be held liable for the
#  payment of damages. All rights reserved in the event of the grant
#  of a patent, utility model or design.
#=============================================================================
#  P R O J E C T   I N F O R M A T I O N
#-----------------------------------------------------------------------------
#  Projectname            : resViz (Mapfile based memory resource analysis)
#=============================================================================
#  F I L E   I N F O R M A T I O N
#-----------------------------------------------------------------------------
#  @brief : Read GHS Map file and detect internal structure to facilitate parsing
#  @state : waiting for cleanup 
#=============================================================================


class FileReaderError(Exception):
    def __init__(self,message):
       self.message = message
    def __str__(self):
        return self.message


class FileReader:
    def __init__(self,filename):
        self.__filename = filename
        self.__p_opened = False
        self.__fileHandle = None
        self.__lineno = -1
        self.__p_insection = False
        self.__eof = False

    def currentLineNumber(self):
        return self.__lineno
        
    def getFilename(self):
        return self.__filename

    def __open(self):
        if self.__eof:
            raise FileReaderError('open at eof - file {0}'.format(self.__filename))
        if self.__p_opened:
            raise FileReaderError('already opened - file {0}'.format(self.__filename))
        self.__lineno = 0
        self.__p_opened = True
        self.__fileHandle = open(self.__filename,'r')
    def p_insection(self):
        return self.__p_insection
    def p_eof(self):
         return self.__eof
       
    def __close(self):
        if self.__p_opened:
            self.__fileHandle.close()
            self.__lineno = -1
            self.__p_opened = False
            self.__fileHandle = None
    def nextLine(self):
        if not self.__p_opened:
            self.__open()
        line = self.__fileHandle.readline()
        if bool(line):
            self.__lineno += 1
            if self.__p_insection:
                if line.startswith('\x0c'):
                    self.__p_insection = False
                    line = ''
                else:
                    line = line.rstrip()
                    if line == '':
                        return self.nextLine()
            else:
                line = line.rstrip()
                if line.startswith('Load Map '):
                    self.__p_insection = True
                return self.nextLine()
        else:
            self.__close()
            self.__eof = True
            line = ''
        return line
