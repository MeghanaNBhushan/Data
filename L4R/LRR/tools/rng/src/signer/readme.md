# WorkOn REST API  <!-- omit in toc -->

WorkOn provides a REST API to create a draft workon and to get the status.

**WorkOn User Manual**

https://inside-docupedia.bosch.com/confluence/display/workonend/WorkON+User+Manual

**REST API Description**

https://inside-docupedia.bosch.com/confluence/display/workonend/WorkON+User+Manual

**Short Summary of Usage of workon.py**

The REST API expects an json file as input which contains all relevant data. This file 
need to be adapated by the project:

- User information
- Approver List
- ...

Examples of the json file can be found in /rn_TestProject/workon_cfg.json

**Undocumented REST JSON Infos**

Base on the following attribute a multiple approver list is defined. 
rbga.field.approvalstep: [One Step Approval|Two Step Approval|Three Step Approval]

Example:

```
"rbga.field.approvalstep": "Two Step Approval",
```

Approver 1 List config
```
"rbga.field.workflowType": "Parallel",
"rbga.field.parallelWorkflowSel": "All the Approvers has to approve",
"rbga.field.approver1": {
    "approvers": [
    {
        "addAfterEnabled": true,
        "deleteFlag": "Yes",
        "description": "PO SW Integration",
        "fixed": false,
        "removable": true,
        "userid": "zna8fe",
        "ccList": ""
    }
    ],
    "checkDuplicate": "false",
    "maxApprover": "20",
    "type": "1"
},
```

Approver 2 List config

```
"rbga.field.wf2": "Serial",
"rbga.field.parallelWorkflowSel2": "All the Approvers has to approve",
"rbga.field.approver2": {
    "approvers": [
    {
        "addAfterEnabled": true,
        "deleteFlag": "Yes",
        "description": "PM",
        "fixed": false,
        "removable": true,
        "userid": "cit2abt",
        "ccList": ""
    },
    {
        "addAfterEnabled": true,
        "deleteFlag": "Yes",
        "description": "Head of Athena Sensors",
        "fixed": false,
        "removable": true,
        "userid": "scx2bue",
        "ccList": ""
    }
    ],
    "checkDuplicate": "false",
    "maxApprover": "20",
    "type": "1"
}
```

For Three Step Approvl simple duplicate approver two list and change 2 to 3.

**REST API Parameters**

In order to communicate with the work on server the following infos are required:

- WorkOn Endpoint
- Key ID
- REST Service names

The workon endpoint and key are confidental and **must not** be shared.

The configuration ist done view workon_rest_cfg.json

```
{
    "rest_status": {
        "url": "ENDPOINT/status",
        "key_id": "GET THIS KEY ON DEMAND"
    },
    "rest_draft": {
        "url": "ENDPOINT/createdraftrequest/draft",
        "key_id": "GET THIS KEY ON DEMAND"
    },
    "rest_draftcreate": {
        "url": "ENDPOINT(createdraftrequest/create",
        "key_id": "GET THIS KEY ON DEMAND"
    }
}
```

**Testing**

It is posssible to test the API on Q-Server

The endpoint to the q-server can be obtained from jochen.held@de.bosch.com or directly at the workon on responsiblers Manjunath Rajamanickam (SX/BSW2)

The Q-server Website can be found here

https://inside-docupedia.bosch.com/confluence/display/workonend/03+-+How+to+test+new+developments+in+Q-Portal





