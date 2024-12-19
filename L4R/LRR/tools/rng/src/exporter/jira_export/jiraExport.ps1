#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Parameters passed from command line call 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Param(
	[Parameter(Mandatory = $True)]
	[String]
	$CfgFilePath,
	
	[Parameter(Mandatory = $True)]
	[System.String]
	$JQLFixVersion = "EMPTY",
	
	[Parameter(Mandatory = $False)]
	[System.String]
	$OutputPath = "$PSScriptRoot/output/",

	[Parameter(Mandatory = $False)]
	[System.String]
	$DebugMode = "DebugOff"
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Import (Include) powershell module
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Import-Module -Name $PSScriptRoot\PSModules\utilFct.psm1
Import-Module -Name $PSScriptRoot\PSModules\jiraRESTapi.psm1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Global Settings
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Enable Debug output in console
if ($DebugMode -eq "DebugOn") {
	$DebugPreference = "Continue"
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Function to create a new object consisting of JIRA base fields + DOORS Links from /remotelink query
#
#Param: JIRA JQL Query result
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function New-JiraIssueObjectList {
	Param(
		[Parameter(Mandatory = $True)]
		$jiraIssueExport
	)

	$issueObjectList = @()
    
	foreach ($issue in $jiraIssueExport.issues) {
		#FixVersions is an array of all assigned fix versions. Go through the list and only extract the ones with LRR_LGU in name"
		$FixVersionsList = @()
		foreach ($FixVersion in $issue.fields.fixVersions) {
			if ($FixVersion.name -match 'LRR_LGU') {
				$FixVersionsList += $FixVersion.name #Add to array
			}
		}
		
		#If multiple releases are assigned store this info in log file
		if ($FixVersionsList.Count -gt 1) {
			$IssueID = $issue.key
			Write-Log -level WARN -logfile $logfile -Message "IssueID $IssueID : Multiple FixVersions assigned to ticket"
		}
		
		
		$AffectedVersionsList = @()
		foreach ($AffectedVersion in $issue.fields.versions) {
			$AffectedVersionsList += $AffectedVersion.name #Add to array
		}

		
		#Scope is an array. Contains "Customer Relevant", Variant e.g. LRR, SRR
		$ListOfScope = @()
		foreach ($Scope in $issue.fields.customfield_26120) {
			$ListOfScope += $Scope.value #Add to array
		}
					
		#Create Object with all required data	
		$issueObject = [PSCustomObject]@{
			IssueID            = $issue.key
			IssueURL           = "https://rb-tracker.bosch.com/tracker08/browse/" + $issue.key
			IssueStatus        = $issue.fields.status.name 
			FixVersion         = $FixVersionsList
			AffectedVersions   = $AffectedVersionsList
			Scope              = $ListOfScope
			Team               = $issue.fields.customfield_26620
			Summary            = $issue.fields.summary
			StakeholderSummary = $issue.fields.customfield_29720 
			Severity           = $issue.fields.customfield_26728.value
			SafetyRelevance    = $issue.fields.customfield_31220.value 
		}
		#Add all item to an overall list
		
		$issueObjectList += $issueObject
	}    
    
	write-debug ("$(Get-TimeStamp) Issue Object created")
	write-output $issueObjectList
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Execution Starts here
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Read Config File Data
$ConfigFileData = Get-CfgFileData $CfgFilePath

#Create log files path
$logfile = ($OutputPath + "/" + 'jira_export.log')
#Create log file and folder if file does not exist
New-Item -Path $logfile -ItemType File -Force

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Read and Process JIRA Data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

foreach ($cfg in $ConfigFileData.JiraJQLcfg) {
	
	$OutputFileName = $cfg.outputFile
	Write-Log -level INFO -logfile $logfile -Message "Generation of $OutputFileName started"
	write-debug $OutputFileName
	Write-host "$(Get-TimeStamp) Config File $OutputFileName read succesfully"

	#JQL Filter expression to get list of jira issues
	$jqlJiraFilter = $cfg.jqlJiraFilter

	#Replace place holder in JQL string
	$jqlJiraFilter = $jqlJiraFilter.Replace("#FIXVERSION#", $JQLFixVersion)
	write-debug $jqlJiraFilter

	# Get JIRA data, call REST api getting only specific fields to reduce data amount transferred from JIRA server
	$jqlSearchResult = Get-JiraRESTJQLSearch -jqlString $jqlJiraFilter -fields "key,status,labels,fixVersions,versions,summary,customfield_26120,customfield_26620,customfield_29720,customfield_26728,customfield_31220"

	$issueObjectList = New-JiraIssueObjectList $jqlSearchResult
	$outputfile = ($OutputPath + "/" + $OutputFileName)

	# NEXT LINE WILL BE POSSIBLE WITH POWERSHELL > V7.0
	# [-AsArray] Outputs the object in array brackets, even if the input is a single object.
	#$issueObjectList | ConvertTo-Json -AsArray -depth 100 | Out-File $outputfile -Encoding utf8
	# Workaround in Powershell V5.1
	# use @() to convert object into an array of objects. 
	$output = ConvertTo-Json @($issueObjectList) -depth 100 
	
	# Create the folder in case it does not exist
	New-Item -Path $outputfile -ItemType File -Force
	$output | Out-File $outputfile -Encoding utf8

	Write-Log -level INFO -logfile $logfile -Message "Generation of $OutputFileName finished"
	write-host "$(Get-TimeStamp) JSON File $outputfile created"   
}