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
#  @brief         : demangle GHS symbols
#=============================================================================

import threading
import subprocess
import ctypes
import re

class GHSDemangleError(Exception):
    def __init__(self,message):
       self.message = message
    def __str__(self):
        return self.message



def staticConstructorDecoder(name):
    dmName = name
    prefix = ''
    stimatch = re.search('^__sti___(\d+)_(.*)',name)
    if stimatch:
        size = int(stimatch.group(1))
        uname = stimatch.group(2)
        file = uname[0:size]
        filematch = re.match('^(.*)_([^_]+)$',file)
        if filematch:
            file = filematch.group(1)+ '.' + filematch.group(2)
        uid = uname[size+1:]
        dmName = '_'.join(['__static_constructor',uid,'file('+file+')'])
    return dmName,''
    
def ghsThunkDecoder(name):
    dmName = name
    gtmatch = re.search('^__ghs_thunk__0x([0-9a-f]+)__(.*)',name)
    if gtmatch:
        uid = gtmatch.group(1)
        func = gtmatch.group(2)
        prefix = '_'.join(['__ghs_thunk',uid,'vfunc',''])
    return prefix,func
    
def stringIdentity(name):
    return name,''

def getNamespaceHandleTemplates(name,p_excludeSpecialSymbols=False):
    specialSymbol = False
    namespace = ''
    vtablematch = re.match('^virtual_function_table_for_(.*)$',name)
    if vtablematch:
        namespace = vtablematch.group(1)
        specialSymbol = True
    else:
        gthunkmatch = re.match('^__ghs_thunk_[0-9a-f]+_vfunc_(.*)$',name)
        if gthunkmatch:
            name = gthunkmatch.group(1)
            specialSymbol = True
    if not ( bool(namespace) or ( p_excludeSpecialSymbols and specialSymbol )):
        operatorMatch = re.search('operator ',name)
        pos = -1
        cc = 0
        abc = 0
        for i in range(0,len(name)):
            c = name[i]
            if c == ':' and abc == 0:
                cc += 1
                if cc == 2:
                    pos = i - 1
                    cc = 0
            elif c in ['<','(']:
                abc += 1
                #cc = 0
            elif c in ['>',')']:
                abc -= 1
        if pos > 0 :
            if abc == 0:
                namespace = name[0:pos]
            elif operatorMatch:
                if name[0] in ['*','&']:
                    namespace = name[1:pos]
                else: 
                    namespace = name[0:pos]
            else:
                pass
                #print('HOLLA {0} .. {1}'.format(abc,name))
    return namespace
            
    
    
    

class CDllDemangler(object):
    __symsStartingWithDemangler = {
            '__ghs_thunk__':ghsThunkDecoder,
            '__sti___':staticConstructorDecoder
        }
    __nameSpaceIgnoreStartingWith = [
        '__ghs_thunk_',
        '__static_constructor_'
    ]
    def __init__(self,dll):
        self.__dll = dll
    def __str__(self):
        return 'CDllDemangler({0})'.format(self.__dll)
        
    def init(self):
        self.__demangleDll = ctypes.cdll.LoadLibrary(self.__dll)
        self.__decodeFunc = self.__demangleDll.demangle_ghs_name
        self.__decodeFunc.restype = ctypes.c_char_p
        self.__lastResort = CFallBackDemangler()
    def finit(self):
        pass

    def decodeName(self,name):
        tobemandled = name
        decodedName = name
        dmprefix = ''
        callDllDemangler = True
        for prefix in CDllDemangler.__symsStartingWithDemangler:
            if name.startswith(prefix):
                dmprefix,tobemandled = CDllDemangler.__symsStartingWithDemangler[prefix](name)
                break
        if bool(tobemandled):
            ctype_name = ctypes.c_char_p(bytes(tobemandled,'utf-8'))
            ctype_demangledTemp = self.__decodeFunc(ctype_name)
            if bool(ctype_demangledTemp):
                demangledTemp = ctype_demangledTemp.decode("utf-8")
                decodedName = ''.join([dmprefix,demangledTemp])
            else:
                decodedName = name
        elif bool(dmprefix):
            decodedName = dmprefix
        if name != decodedName:
            #print('{0} .... \nDECODED\t{1}'.format(name,decodedName))
            pass
        return decodedName

    def getNamespace(self,name,p_fallBack=False,p_decodeFirst=False):
        namespace = ''
        if p_fallBack:
            namespace = self.__lastResort.getNamespace(name)
        else:
            dmName = name
            if p_decodeFirst:
                dmName = self.decodeName(name,p_local)
            if not p_decodeFirst or name != dmName:
                for prefix in CDllDemangler.__nameSpaceIgnoreStartingWith:
                    if dmName.startswith(prefix):
                        break
                else:
                    #namespace = '::'.join(dmName.split('::')[0:-1])
                    namespace = getNamespaceHandleTemplates(name)
                    #print('{0} .... \nNAMESPACE\t{1}'.format(name,namespace))
        return namespace

            
class CFallBackDemangler(object):
    def __init__(self):
        pass
    def __str__(self):
        return 'CFallBackDemangler'

    def init(self):
        pass
    def finit(self):
        pass

    def decodeName(self,name):
        return name
# copied from vw calcres implementation

    def getNamespace(self,sname,p_decodeFirst=False):
        # find first occurence of "Q\d_\d"
        m_q = re.search("(Q\d)_\d",sname)
        if not m_q: return '' # no C++ symbol
        pos = sname.find(m_q.group(1)) + 1
        name_number = int(sname[pos])
        pos += 2
        # delete unused prefix
        search_string = sname[pos:]
        namespace = ""
        for i in range(name_number):
            # extract number and amount of digits
            m_count = re.match("(\d+)", search_string)
            if not m_count: 
                print("Warning: Could not extract namespace of following symbol:", sname)
                return ''
            length = int(m_count.group(1))
            temp_length = length
            digits_count = 0
            while temp_length > 0:
                temp_length = int(temp_length / 10)
                digits_count += 1
            # extract namespace part with length of previos number
            # stop if name includes "__tm__" (internal instantiations)
            name = search_string[digits_count:digits_count+length]
            search_string = search_string[digits_count + length:]
            tm_pos = name.find("__tm__")
            if tm_pos != -1: name = name[:tm_pos]
            if "_INTERNAL_" in name: continue
            elif namespace == "": namespace = name
            else: namespace += "::"+name
            if tm_pos != -1: break
        #print('{0} -- {1} \n\t {2}\n\n'.format('get_namespace', sname, namespace))
        return namespace





class Csync:
    def __init__(self):
        self.valid = False
        self.is_done = False
        self.name = ''
    def set(self,name):
        #print('Csync.set({0})'.format(name))
        self.name = name
        self.valid = True
    def p_valid(self):
        return self.valid
    def getName(self):
        return self.name
    def clear(self):
        self.valid = False
    def done(self):
        self.is_done = True
    def p_done(self):
        return self.is_done
     


class myThread (threading.Thread):
    def __init__(self, threadID, name,readfp,syncO):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.readfp = readfp
        self.nl = None
        self.done = False
        self.sync = syncO

    def run(self):
        self.readName()
        self.done = True

    def getDMName(self):
        result = None
        if self.nameValid:
            self.nameValid = False
            result = self.name
        return result

    def readName(self):
        started = False
        while True:
            dmn = self.readfp.readline()
            if dmn.startswith('$$$START$$$'):
                started = True
            elif dmn.startswith('$$$END$$$'):
                started = False
            elif dmn.startswith('$$$DONE$$$'):
                self.sync.done()
                break
            elif started:
                self.sync.set(dmn)
                started = False

class CDecodeDemangler(object):
    __symsStartingWithDemangler = {
            '__ghs_thunk__':ghsThunkDecoder,
            '__sti___':staticConstructorDecoder
        }
    __nameSpaceIgnoreStartingWith = [
        '__ghs_thunk_',
        '__static_constructor_'
    ]

    def __init__(self,decode_cmd):
        #decode_cmd.extend(['>', 'sepppppel.txt'])
        self.__decode = decode_cmd
        self.__subProcess = None
        self.__decodeStdin = None
        self.__decodeStdout = None
        self.__decodeStderr = None
        self.__mSubprocess = None
        self.__readingThread = None
    
    def __str__(self):
        return 'CDecodeDemangler({0})'.format(self.__decode[0])
        
    def init(self):
        self.__mSubprocess = subprocess
        proc = None
        try:
            print('Try to create decode process object ... {0}'.format(str(self.__decode)))
            self.__subProcess 
            proc = subprocess.Popen(
                    self.__decode,
                    shell=True,
                    universal_newlines=True,
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    bufsize=1,
                    close_fds=True,
                    text=True,
                )
        except ValueError:
            raise GHSDemangleError('failed to run demangler {0}\n\t{1}'.format(' '.join(self.__decode),str(ValueError)))
        self.__subProcess = proc
        self.__decodeStdin = self.__subProcess.stdin
        self.__decodeStdout = self.__subProcess.stdout
        self.__sync = Csync()
        self.__readingThread = myThread(1, 'ReaderLe',self.__decodeStdout,self.__sync)
        print('Start Reader Thread ...')
        self.__readingThread.start()
        print('[DONE] Start Reader Thread ...')

    def getDName(self):
        result = None
        if self.__sync.p_valid():
            result = self.__sync.getName()
            self.__sync.clear()
        return result

    def finit(self):
        self.__decodeStdin.write('$$$DONE$$$\n')
        while not self.__sync.p_done():
            self.__decodeStdin.write('$$$SOMETHING$$$\n')
        try:
            #print('try to terminate ... {0}'.format(str(self.__subProcess)))
            outs, errs = self.__subProcess.communicate(input=('\x1a' + '\n'),timeout=15) # .encode()
        except subprocess.TimeoutExpired:
            print('failed to terminate process ....')
            self.__subProcess.kill()
            outs, errs = self.__subProcess.communicate()
        self.__subProcess = None
        self.__decodeStdin = None
        self.__decodeStdout = None

    def decodeName(self,name):
        tobemandled = name
        decodedName = name
        dmprefix = ''
        for prefix in CDecodeDemangler.__symsStartingWithDemangler:
            if name.startswith(prefix):
                dmprefix,tobemandled = CDecodeDemangler.__symsStartingWithDemangler[prefix](name)
                break
        if bool(tobemandled):
            demangledTemp = self.demangleName(tobemandled)
            if bool(demangledTemp):
                decodedName = ''.join([dmprefix,demangledTemp])
            else:
                decodedName = name
        elif bool(dmprefix):
            decodedName = dmprefix
        if name != decodedName:
            #print('{0} .... \nDECODED\t{1}'.format(name,decodedName))
            pass
        return decodedName

    def demangleName(self,name):
        ubName = (name + '\n')
        self.__decodeStdin.write('$$$START$$$\n')
        self.__decodeStdin.write(ubName)
        self.__decodeStdin.write('$$$END$$$\n')
        self.__decodeStdin.flush()
        dnm = dm.getDName()
        while dnm is None:
            self.__decodeStdin.write('$$$SOMETHING$$$\n')
            dnm = dm.getDName()
        return dnm

    def getNamespace(self,name,p_decodeFirst=False):
        namespace = ''
        dmName = name
        if p_decodeFirst:
            dmName = self.decodeName(name,p_local)
        if not p_decodeFirst or name != dmName:
            for prefix in CDecodeDemangler.__nameSpaceIgnoreStartingWith:
                if dmName.startswith(prefix):
                    break
            else:
                #namespace = '::'.join(dmName.split('::')[0:-1])
                namespace = getNamespaceHandleTemplates(name)
                #print('{0} .... \nNAMESPACE\t{1}'.format(name,namespace))
        return namespace

    def sendToBuffer(self):
        self.__decodeStdin.write('$$$SOMETHING$$$\n')



if __name__ == "__main__":
    dm = CDecodeDemangler(['c:/TCC/Tools/greenhills_ifx/comp_201815_4fp_WIN64/decode.exe'])
    dm.init()
    symbols = [
            '__CPR1363____vtbl__170Q2_24daddy_qualification_test138UCCheckDataPortConnection__tm__104_Q2_J14J72TSCOM__tm__59_Q2_J14J27PROXY_LATEST_CIRC_BUFF_LOCK__Q2_J14J1147TEST_IMPL_UCCheckDataPortConnectioncheckReceiverAll_SenderConnection__tm__1069_Q2_J14JJ107JQ2_3vfc955TTypeList__tm__937_Q2_J14J72TSCOM__tm__59_Q2_J14J27PROXY_LAST_3_CIRC_BUFF_LOCKQ2_3vfc823TTypeList__tm__805_Q2_J14J71TSCOM__tm__58_Q2_J14J26PROXY_NEW_3_CIRC_BUFF_LOCKQ2_3vfc692TTypeList__tm__674_Q2_J14J72TSCOM__tm__59_Q2_J14J27PROXY_ALLNEW_CIRC_BUFF_LOCKQ2_3vfc560TTypeList__tm__542_Q2_J14J75TSCOM__tm__62_Q2_J14J30NONE_PROXY_PARAM_TRIPLE_BUFFERQ2_3vfc425TTypeList__tm__407_Q2_J14J76TSCOM__tm__63_Q2_J14J31NONE_PROXY_NEWEST_TRIPLE_BUFFERQ2_3vfc289TTypeList__tm__271_Q2_J14J76TSCOM__tm__63_Q2_J14J31NONE_PROXY_LATEST_TRIPLE_BUFFERQ2_3vfc153TTypeList__tm__135_Q2_J14J77TSCOM__tm__64_Q2_J14J32NONE_PROXY_ALLNEW_CIRC_BUFF_LOCKQ2_3vfc17CTypeListNullType',
            '__cl__184__Ul1_FUcT1__L1__sortBehindByScore__Q4_3Per3Rrs115RrsClusterManager__tm__90_Q3_3Per3Rrs76RrsConfig__tm__59_Q3_3Per3Rrs21RrsCluster__tm__4_fUsXCUsL_3_256XCUsL_3_288Uc12SortedAccessFv_UiCFUcT1',
            '__cl__56__Ul2_Fv__L2__execVelocityVxv__5Mon_xFRQ2_5Mon_x7CMonItfCFv',
            'is_monitoring_triggered_FAULT_CONSISTENCY_ACC_EXTENSION__L0__monitor__Q2_6vw_ssw11CFodManagerFv',
            '__sti___18_rbSysEvMRA5_DT_cpp_59c81aa9',
            '__ghs_thunk__0xfffffffffffffffc__run__Q3_2Vw3Mon97TMonStrategyCoded__tm__72_Q4_2Vw3Fct10Monitoring47MonFaultEspStoppingDistanceControlNotAppliedCtrFv_v',
        ]
    #symbols = []
    n = 2
    for name in symbols:
        demangledName = dm.decodeName(name)
        namespace = dm.getNamespace(demangledName,False)
        print('Name: {0}\n\tDECODES --- {1}\tNAMESPACE --- {2}'.format(name,demangledName,namespace))
    dm.finit()
    #dm.finit()


