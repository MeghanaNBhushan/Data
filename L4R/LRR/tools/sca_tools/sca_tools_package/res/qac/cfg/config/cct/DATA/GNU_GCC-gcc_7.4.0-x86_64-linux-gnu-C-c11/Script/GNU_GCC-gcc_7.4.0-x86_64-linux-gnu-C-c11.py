from __future__ import print_function

import os
import sys

# add include paths for CCT stub directories
def stub():
  try:
    # template settings to make this script generic
    compilerHierarchy = "GNU"
    sourceLanguage = "C"

    includeOption = "-si" if sourceLanguage == "C++" else "-i"
    scriptFile = (sys.executable if getattr(sys, 'frozen', False) else
      os.path.realpath(__file__)
    )
    currentDir = os.path.dirname(scriptFile)
    fileName = os.path.basename(scriptFile)
    cipFilename = os.path.splitext(fileName)[0].strip()
    parentDir = os.path.dirname(currentDir)
    configDir = os.path.dirname(os.path.dirname(os.path.dirname(parentDir)))
    stubDir = os.path.join(parentDir, "Stub")
    cipFile = open(os.path.join(configDir, "cip", cipFilename + ".cip"), 'w')

    # stub directory
    print("-q", "\"" + stubDir + "\"", file=cipFile)
    for d, ds, fs in os.walk(stubDir):
      if d.endswith("prlforceinclude"):
        for fn in fs:
          print("-fi", "\"" + os.path.join(d, fn) + "\"", file=cipFile)
      else:
        doInclude = True
        if compilerHierarchy == "GNU":
          sepCount = d[len(stubDir):].count(os.sep)
          doInclude = (
            (sepCount == 1 and len(fs) != 0) or (sepCount > 1 and len(ds) != 0)
          )
        if doInclude:
          print(includeOption, "\"" + d + "\"", file=cipFile)
    # add paths from syshdr.lst
    print("* system include paths", file=cipFile)
    templatePath = os.path.join(stubDir, "syshdr.lst")
    dirFile = open(templatePath, "r")
    root = ""
    expectRoot = False
    for sysPath in dirFile:
      sysPath = sysPath.strip()
      if expectRoot:
        expectRoot = False
        root = sysPath
      elif sysPath == ":ROOT:":
        expectRoot = True
      else:
        path = "\"" + os.path.join(root, sysPath) + "\""
        print(includeOption, path, file=cipFile)
        print("-q", path, file=cipFile)
    dirFile.close()
    cipFile.close()
  except IOError:
    pass

if __name__=="__main__":
  stub()

