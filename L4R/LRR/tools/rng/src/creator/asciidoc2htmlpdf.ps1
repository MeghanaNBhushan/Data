#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Parameters passed from command line call 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Param(
	[Parameter(Mandatory = $False)]
	[System.String]
	$inputfile = "$PSScriptRoot/test/system-release-notes.adoc",
	
	[Parameter(Mandatory = $False)]
	[System.String]
	$output_dir = "$PSScriptRoot/test/gen",
	
	[Parameter(Mandatory = $False)]
	[String]
	$CfgFilePath = "$PSScriptRoot/test/asciidocvariants.json",
	
	[Parameter(Mandatory = $False)]
	[String]
	$ReleaseVersion = "Test_Release_Name",

	[Parameter(Mandatory = $False)]
	[System.String]
	$LogFilePath = "$PSScriptRoot/test/log/",

	[Parameter(Mandatory = $False)]
	[System.String]
	$DebugMode = "DebugOff"
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Import (Include) powershell module
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Import-Module -Name $PSScriptRoot\PSModules\utilFct.psm1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Global Settings
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Enable Debug output in console
if ($DebugMode -eq "DebugOn") {
	$DebugPreference = "Continue"
}

#ascidoctor-pdf command line parameters
$atr_pdf_fonts_dir = "pdf-fontsdir=" + $PSScriptRoot + "/styles/;GEM_FONTS_DIR"
$atr_pdf_style = "pdf-style=" + $PSScriptRoot + "/styles/custom-pdf-theme.yml"
$atr_revnumber = "revnumber=$ReleaseVersion"
$atr_variants = @(
	'DEFAULT1'
	'DEFAULT2'
	'DEFAULT3'
	'DEFAULT4'
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Execution Starts here
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Read Config File Data
$ConfigFileData = Get-CfgFileData $CfgFilePath

# #Create log files path
$logfile = ($LogFilePath + 'asciidoc2htmlpdf.log')
#Create log file and folder if file does not exist
New-Item -Path $logfile -ItemType File -Force

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run asciidoctor to generate pdf and html output
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

foreach ($cfg in $ConfigFileData.asciidocvariants) {
	#Variant Name 
	$variantname = $ReleaseVersion + "_" + $cfg.VariantShort
	
	# Start the processing and create the folder
	Write-Log -level INFO -logfile $logfile -Message "Generation of $variantname started"
	write-debug $variantname
	
	Write-host "$(Get-TimeStamp) $variantname folder created"
	$destination_dir = $output_dir + "\" + $variantname
	New-Item -ItemType directory -Force -Path $destination_dir

	#Update variant selctors from config file
	if ($cfg.VariantSelectors.count -le $atr_variants.count) {
		$i = 0;
		foreach ($varselector in $cfg.VariantSelectors) {
			$atr_variants[$i] = $varselector
			$i++				
		}
	}
	else {
		$msg = "Number of Variants in json config file greater then number of agruments considered in asciidoctor-pdf call. Adapt number of agruments in code"
		Write-Log -level ERROR -logfile $logfile -Message $msg
		write-host $msg
	}
	
	#Run PDF Generation
	$out_file = $variantname + ".pdf"
	# Run asciidoctor-pdf Generation Executable
	& 'asciidoctor-pdf' $inputfile -D $destination_dir -o $out_file -a $atr_pdf_fonts_dir -a $atr_pdf_style -a $atr_revnumber -a $atr_variants[0] -a $atr_variants[1] -a $atr_variants[2] -a $atr_variants[3] 

	Write-Log -level INFO -logfile $logfile -Message "Generation of $out_file finished"
	write-host "$(Get-TimeStamp) $out_file created"   

	#Run HTML Generation
	#Copy the resource folder 
	$inputfilePath = Split-Path $inputfile
	$resourcesPath = $inputfilePath + "\" + "resources"
	$resourcesDestPath = $destination_dir + "\resources"
	Copy-Item $resourcesPath -Destination $resourcesDestPath -Recurse -Force
	
	#Run asciidoctor html generation
	$out_file = $variantname + ".html"
	& 'asciidoctor' $inputfile -D $destination_dir -o $out_file -a $atr_variants[0] -a $atr_variants[1] -a $atr_variants[2] -a $atr_variants[3] 

	Write-Log -level INFO -logfile $logfile -Message "Generation of $out_file finished"
	write-host "$(Get-TimeStamp) $out_file created"   
}






