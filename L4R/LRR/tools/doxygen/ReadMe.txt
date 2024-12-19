-------------------------- README for documentaton generator with Doxygen (Prototype)------------------------------------

1. 	Ensure the following software are already installed: 	
	- 	Doxygen 1.8.12, check the path C:/TOOLS/doxygen/1.8.12	( Doxygen 1.8.12 can be installed in ismClientCenter)
	- 	Perl.

2. 	To use the doxygen for your component, the file DoxyfileVar has to be configurated as the following:

	- 	PROJECT_NAME : your component name.
	- 	INPUT : enter your source code files (.c, .h) or the directory with relativ path. e.g.: ../../../../if_fw/core/memstack.
	-	OUTPUT_DIRECTORY : enter the relativ path of your output directory for generated latex and html files. e.g.: ../../../../if_fw/core/memstack/doc/doxygen_output.

3.	Run the perl scipt AutoGenDoxyDoc.pl to generate documents for your component. 

4.	The documents are generated into html files (because of compatibility the latex file generation is deactivated as default), the file /html/index.html is the main document in html format. 

------------------------ Viewing of doxygen document ---------------------------------------------------------------------

    Steps to import and view qch file are below:
    1. Goto C:/TCC/Tools/qt directory ( <TCCdirectory>/Tools/qt/<version number>/bin ) and open assistant.exe.
    2. Goto Edit option in the menu bar and select Preferences.
    3. In Preferences window goto Documentation tab and click on Add button to add the generated qch file.

