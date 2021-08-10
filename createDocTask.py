from jira import JIRA
import sys

# Project Id for Documentation
documentationId = '10807'

# Dictionary of Issue Type Key:Value pairs
# where, Key is Name of the Issue
#        Value is ID of the Issue
issueTypes = {
    'OEM Release': '10401',
    'Retail Release': '10402',
    'Gateway Adapter Release': '10601'
}


# Login Class for logging into the User Account/Profile
class Login:
    def __init__(self, userName, password, server='https://jira.magnitude.com'):
        self.userName = userName
        self.password = password
        self.server = server
    '''
    @return: Makes a connection and returns that connection to the User Profile
    '''
    def connect(self):
        jiraServer = {'server': self.server, 'verify': False}
        return JIRA(options=jiraServer, basic_auth=(self.userName, self.password))

# DocTask Class for creating a Doc Task/Issue
class DocTask:
    def __init__(self, projectId, summary, issueType, releaseDate, userProfile):
        self.projectId = projectId
        self.summary = summary
        self.issueType = issueType
        self.releaseDate = releaseDate
        self.userProfile = userProfile
        self.taskInfo = TaskInfo(self.projectId, self.summary, self.issueType, self.releaseDate)
    '''
    @return: Creates and returns the OEM Doc Task
    '''
    def createDocTask_OEM(self, releaseLabel, perforcePath, customerVersionNumber): 
        docTaskDetails = self.taskInfo.getDetails_OEM(releaseLabel, perforcePath, customerVersionNumber)
        return self.userProfile.create_issue(fields=docTaskDetails)
    '''
    @return: Creates and returns the Retail Doc Task
    '''
    def createDocTask_Retail(self, releaseLabel, perforcePath):
        docTaskDetails = self.taskInfo.getDetails_Retail(releaseLabel, perforcePath)
        return self.userProfile.create_issue(fields=docTaskDetails)
    '''
    @return: Creates and returns the Gateway Adapter Doc Task
    '''
    def createDocTask_GatewayAdapter(self, releaseLabel, perforcePath, standAloneVersionNumber):
        docTaskDetails = self.taskInfo.getDetails_GatewayAdapter(releaseLabel, perforcePath, standAloneVersionNumber)
        return self.userProfile.create_issue(fields=docTaskDetails)

# TaskInfo Class for getting the details of the required fields of the Doc Task
class TaskInfo:
    def __init__(self, projectId, summary, issueType, releaseDate):
        self.projectId = projectId
        self.summary = summary
        self.issueType = issueType
        self.releaseDate = releaseDate
    '''
    @return: Returns the Details of the OEM Doc Task
    '''   
    def getDetails_OEM(self, releaseLabel, perforcePath, customerVersionNumber):
        return {
            'project': {'id': self.projectId},
            'summary': self.summary,
            'issuetype': {'id': self.issueType},
            'customfield_13942': self.releaseDate,
            'customfield_13941': releaseLabel,
            'customfield_13944': perforcePath,
            'customfield_13943': customerVersionNumber
        }
    '''
    @return: Returns the Details of the Retail Doc Task
    '''
    def getDetails_Retail(self, releaseLabel, perforcePath):
        return {
            'project': {'id': self.projectId},
            'summary': self.summary,
            'issuetype': {'id': self.issueType},
            'customfield_13942': self.releaseDate,
            'customfield_13941': releaseLabel,
            'customfield_13944': perforcePath
        }
    '''
    @return: Returns the Details of the Gateway Adapter Doc Task
    '''
    def getDetails_GatewayAdapter(self, releaseLabel, perforcePath, standAloneVersionNumber):
        return {
            'project': {'id': self.projectId},
            'summary': self.summary,
            'issuetype': {'id': self.issueType},
            'customfield_13942': self.releaseDate,
            'customfield_13941': releaseLabel,
            'customfield_13944': perforcePath,
            'customfield_15002': standAloneVersionNumber
        }


# Login to the account with username and password
userName = sys.argv[1]
password = sys.argv[2]

login = Login(userName, password)
profile = login.connect()

issueType = sys.argv[3]
issueType = issueType.strip()

if issueType == 'OEM Release' or issueType == 'OEM':
    summary = sys.argv[4]
    releaseDate = sys.argv[5] # need the date value to be entered in YYYY-MM-DD format.
    releaseLabel = sys.argv[6]
    perforcePath = sys.argv[7]
    customerVersionNumber = sys.argv[8]

    docTask = DocTask(documentationId, summary, issueTypes['OEM Release'], releaseDate, profile)
    newDocIssue = docTask.createDocTask_OEM(releaseLabel, perforcePath, customerVersionNumber)

    print(newDocIssue)

if issueType == 'Retail Release' or issueType == 'Retail':
    summary = sys.argv[4]
    releaseDate = sys.argv[5] # need the date value to be entered in YYYY-MM-DD format.
    releaseLabel = sys.argv[6]
    perforcePath = sys.argv[7]

    docTask = DocTask(documentationId, summary, issueTypes['Retail Release'], releaseDate, profile)
    newDocIssue = docTask.createDocTask_Retail(releaseLabel, perforcePath)

    print(newDocIssue)

if issueType == 'Gateway Adapter Release' or issueType == 'Gateway Adapter':
    summary = sys.argv[4]
    releaseDate = sys.argv[5] # need the date value to be entered in YYYY-MM-DD format.
    releaseLabel = sys.argv[6]
    perforcePath = sys.argv[7]
    standAloneVersionNumber = sys.argv[8]
    # wireframesURL = sys.argv[9]

    docTask = DocTask(documentationId, summary, issueTypes['Gateway Adapter Release'], releaseDate, profile)
    newDocIssue = docTask.createDocTask_GatewayAdapter(releaseLabel, perforcePath, standAloneVersionNumber)
    
    print(newDocIssue)
