import os, inspect
import sys
import platform


def sysInclude():



    try:
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        scriptFile = inspect.getfile(inspect.currentframe())
        fileName = os.path.basename(scriptFile)
        cipFilename = os.path.splitext(fileName.strip())[0] + '.cip'
        normal_parent = os.path.dirname(current_dir)
        dataDir = os.path.dirname(normal_parent)
        cctDir = os.path.dirname(dataDir)
        configDir = os.path.dirname(cctDir)
        cipDir = os.path.join(configDir, "cip")
        cipFilepath = os.path.join(cipDir, cipFilename)
        cipFile = open(cipFilepath, 'w')

        compiler_path = os.getenv('GHS_IFX_HOME')
        if None == compiler_path:
           raise FileNotFoundError('Environment variable GHS_IFX_HOME is not set')

        compiler_include_path = [
            os.path.join(compiler_path, "include", "tri"),
			os.path.join(compiler_path, "ansi")
        ]
        stub_include_path = [
        ]
        force_include_header = [
        ]

        for dirName in stub_include_path:
            cipFile.write('-i "' + dirName + '"\n')
            cipFile.write('-q "' + dirName + '"\n')
        for fn in force_include_header:
            cipFile.write('-fi "' + fn + '"\n')
        for dirName in compiler_include_path:
            cipFile.write('-i "' + dirName + '"\n')
            cipFile.write('-q "' + dirName + '"\n')
        
        cipFile.close()
    except IOError: pass 

if __name__=="__main__":
    if sys.platform == 'win32' :
        sysInclude()

