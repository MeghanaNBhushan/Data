#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Global Parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#JIRA REST Api URL: to get Issue data
$issueRESTUrl = "https://rb-tracker.bosch.com/tracker08/rest/api/2/issue/"

#JIRA REST Api URL: Get JQL query results
$searchRESTUrl = "https://rb-tracker.bosch.com/tracker08/rest/api/2/search"

#JIRA REST Api URL: Get project info
$projectRESTUrl = "https://rb-tracker.bosch.com/tracker08/rest/api/2/project/"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Function to get a Time stamp for logging
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function Get-TimeStamp{
	write-output (Get-Date -format "[dd.MM.yyyy HH:mm:ss]")
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Function to get List of JIRA issues based on JQL query
#
#Param: jqlString: JIRA JQL Query string
#Param: fields: Define which fields of an issue are extracted from JIRA. This reduces download size from jira
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function Get-JiraRESTJQLSearch {
	Param(
	[Parameter(Mandatory=$True)]
    [String]
    $jqlString,
	
	[Parameter(Mandatory=$False)]
    [String]
    $fields = "key,status,labels,fixVersions,customfield_26620"
	)
		
	$searchBody = @{
		startIndex=0
		maxResults = 2000
		jql=$jqlString
		fields=  $fields
	}
	
	try
    {
        $searchResult = Invoke-RestMethod -Method get -uri $searchRESTUrl -body $searchBody -UseDefaultCredentials   
        write-debug ("$(Get-TimeStamp) JIRA REST API search JQL executed")
		write-output $searchResult 	    
    }
	catch
    {
		$ErrorMessage = $_.Exception.Message
    	Write-debug "$(Get-TimeStamp) Error: Invoke-RestMethod Search Error: $ErrorMessage"
    }  
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Function to get List of attached links to a specific JIRA issue
#
#Param: JIRA JQL Query string
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function Get-JiraRESTRemoteLinks {
	Param(
	[Parameter(Mandatory=$True)]
    [String]
    $IssueID
	)
	
	try
	{
		$issueRESTUrlForID= $issueRESTUrl + $IssueID+ "/remotelink"  
		$listOfLinks = Invoke-RestMethod -Method get -uri $issueRESTUrlForID -UseDefaultCredentials
		write-output $listOfLinks 
	}
	catch
		{
		$ErrorMessage = $_.Exception.Message
		Write-debug "$(Get-TimeStamp) Error: Invoke-RestMethod Search Error: $ErrorMessage"
	}  
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get List of JIRA Fix versions. Just a test. not really required. Can be handled by JQL query
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
function Get-JiraRESTVersions {
	[CmdletBinding()]
    Param(
    [Parameter(Mandatory=$True)]
    [String]
    $SearchString,

    [Parameter(Mandatory=$True)]
    [string]
    $projectIDorKey
    )

	$searchBody = @{
		startAt=0
		maxResults = 2000
		orderedby = "name"
	}
		
	$ListOfVersions = @()
	try
	{
		$URLcurrent = $projectRESTUrl + $projectIDorKey+ "/version"  
		$versionList = Invoke-RestMethod -Method get -uri $URLcurrent -body $searchBody -UseDefaultCredentials
		
		foreach($version in $versionList.values)
		{	
			if ($version.name -like '*'+$SearchString+'*' )
			{
				$ListOfVersions += $version.name
			}
		}
		
		write-output $ListOfVersions
	}
	catch
		{
		$ErrorMessage = $_.Exception.Message
		Write-debug "$(Get-TimeStamp) Error: Invoke-RestMethod Search Error: $ErrorMessage"
		return
	}  
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Make functions available to other modules
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Export-ModuleMember -Function "Get-JiraRESTJQLSearch"
Export-ModuleMember -Function "Get-JiraRESTRemoteLinks"
Export-ModuleMember -Function "Get-JiraRESTVersions"
