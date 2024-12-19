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
    return dmName,'',''
    
def ghsThunkDecoder(name):
    prefix = name
    func = ''
    gtmatch = re.search('^__ghs_thunk__0x([0-9a-f]+)__(.*)',name)
    if gtmatch:
        uid = gtmatch.group(1)
        func = gtmatch.group(2)
        prefix = '_'.join(['__ghs_thunk',uid,'vfunc',''])
    return prefix,func,''

def unnamedStaticDecoder(name):
    prefix = ''
    suffix = ''
    unsmatch = re.search('^____UNNAMED_(\d+)_static_in_(.*)',name)
    if unsmatch:
        count = unsmatch.group(1)
        name = unsmatch.group(2)
        suffix =  ' UNNAMED_static_{0}'.format(count)
    return prefix,name,suffix

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
            
    
    
    

class CDllDemangler:
    __symsStartingWithDemangler = {
            '__ghs_thunk__':ghsThunkDecoder,
            '__sti___':staticConstructorDecoder,
            '____UNNAMED_':unnamedStaticDecoder
        }
    __nameSpaceIgnoreStartingWith = [
        '__ghs_thunk_',
        '__static_constructor_'
    ]
    def __init__(self,dll):
        self.__dll = dll

    def init(self):
        self.__demangleDll = ctypes.cdll.LoadLibrary(self.__dll)
        self.__decodeFunc = self.__demangleDll.demangle_ghs_name
        self.__decodeFunc.restype = ctypes.c_char_p
        self.__lastResort = CFallBackDemangler()

    def decodeName(self,name):
        tobemandled = name
        decodedName = name
        dmprefix = ''
        dmsuffix = ''
        demangledTemp = ''
        callDllDemangler = True
        for prefix in CDllDemangler.__symsStartingWithDemangler:
            if name.startswith(prefix):
                dmprefix,tobemandled,dmsuffix = CDllDemangler.__symsStartingWithDemangler[prefix](name)
                break
        if bool(tobemandled):
            ctype_name = ctypes.c_char_p(bytes(tobemandled,'utf-8'))
            ctype_demangledTemp = self.__decodeFunc(ctype_name)
            if bool(ctype_demangledTemp):
                demangledTemp = ctype_demangledTemp.decode("utf-8")
                decodedName = ''.join([dmprefix,demangledTemp,dmsuffix])
            else:
                decodedName = name
        elif bool(dmprefix):
            decodedName = dmprefix
        if name != decodedName:
            # print('{0} .... \nDECODED\t{1}'.format(name,decodedName))
            # print('OOOOO: {0} \nTTTTT: {1}\nDDDDD:{2}\n'.format(name,demangledTemp,decodedName))
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

            
class CFallBackDemangler:
    def __init__(self):
        pass

    def init(self):
        pass

    def decodeName(self,name):
        return name
# copied from vw calcres implementation

    def getNamespace(self,sname,p_decodeFirst=False):
        # find first occurence of "Q\d_\d"
        m_q = re.search("(Q\d)_\d",sname)
        if not m_q: return None # no C++ symbol
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
                return None
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
