import os
import xml.etree.ElementTree as ET

# Prepare the Batch Script with the Select Queries
def prepareBatchScript(selectQueries, dsn, scalabilityTesterPath, outputDir):
    SCALABILITY_TESTER_PATH = scalabilityTesterPath
    TestNo = 0
    TEST_TIME_IN_SECONDS = 3400
    DSN = dsn
    OUTPUT_DIRECTORY = outputDir
    THREAD_COUNT = 30

    script = "@echo off\n"
    script += "cls\n\n"

    script += "Set TestNo=" + str(TestNo) + "\n"
    script += "Set TEST_TIME_IN_SECONDS=" + str(TEST_TIME_IN_SECONDS) + "\n"
    script += "Set SCALABILITY_TESTER_PATH=" + SCALABILITY_TESTER_PATH + "\n"
    script += "Set DSN=\"" + DSN + "\"\n"
    script += "Set OUTPUT_DIRECTORY=" + OUTPUT_DIRECTORY + "\n"
    script += "Set THREAD_COUNT=" + str(THREAD_COUNT) + "\n\n"

    script += ":start\n"
    script += "Set OUTPUT_FILE=\"%OUTPUT_DIRECTORY%" + "%TestNo%\n"

    for query in selectQueries:
        script += "if %TestNo% == " + str(TestNo)
        script += " %SCALABILITY_TESTER_PATH% -t %THREAD_COUNT%" + " -dc %DSN% -q \"" + query + "\""
        script += " -tt %TEST_TIME_IN_SECONDS%" + " -o %OUTPUT_FILE%\n"
        TestNo += 1

    script += "if %TestNo% == " + str(TestNo) + " goto end\n\n"

    script += "Set /A TestNo+=1\n"
    script += "goto start\n\n"

    script += ":end\n"
    script += "echo \"Done.\"\n"
    script += "pause\n"

    return script

# Accessing files part using os lib ##################################################################################################

'''
    Replace the following part of the directory path with package location in the VM that you are going to use.
    C:\\Users\\rkundeti\\Documents\\QuickBooks\\SFMC-1011-package\\new_pack_CL_1\\SFMarketingCloud_w2012r2_vs2013_64\\

'''
packageLocation = "C:\\Users\\rkundeti\\Documents\\QuickBooks\\SFMC-1011-package\\new_pack_CL_1\\SFMarketingCloud_w2012r2_vs2013_64\\"
testSets_Dir = packageLocation + "Touchstone\\specific\\TestDefinitions\\SQL\\TestSets"

SQL_TestSets = []    # The Test Sets such as AND_OR, JOIN, LIKE, PASSDOWN, SELECT_TOP, GROUP_BY, ORDER_BY

for filename in os.listdir(testSets_Dir):
    f = os.path.join(testSets_Dir, filename)
    if os.path.isfile(f):
        SQL_TestSets.append(str(f))


# XML parsing part using xml's etree lib ############################################################################################

selectQueries = []     # should contain 20 select queries for Scalability Test.

# Replace all the testSetFilePaths with the xml parsed roots which is in this case a <TestSet>
for fileIndex, testSetFilePath in enumerate(SQL_TestSets):
    parsedTestSetFile = ET.parse(testSetFilePath)
    testSet = parsedTestSetFile.getroot()
    SQL_TestSets[fileIndex] = testSet

# Pick the 20 queries required for the Scalibility Test.
no_of_queries = 0
while no_of_queries < 20:
    querynumber = 1
    for testSet in SQL_TestSets:
        if no_of_queries >= 20: break
        query = testSet[querynumber - 1].find('SQL').text
        if 'select' in query.lower():
            selectQueries.append(query)
            no_of_queries += 1
    if no_of_queries >= 20: break
    querynumber += 1

# for query in selectQueries:
#     print(query)


# Prepare the Batch Script for Starting the Scalibilty Test.

SCALABILITY_TESTER_PATH = "C:\\Users\\rkundeti\\Desktop\\ScalabilityTester.exe"
DSN = "dsn=Microsoft SFMC"
OUTPUT_DIRECTORY = "C:\\Users\\rkundeti\\Desktop\\"

script = prepareBatchScript(selectQueries, DSN, SCALABILITY_TESTER_PATH, OUTPUT_DIRECTORY)

exampleBatFile = open(r'.\\ExampleBatchFileForST.bat', 'w+')
exampleBatFile.write(script)
exampleBatFile.close()
