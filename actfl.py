import urllib2
import os.path


def getConfData():
    response = urllib2.urlopen('http://www.xpressleadpro.com/Leads/Leads_Download_All.php?SC=ACTF1117&EXID=1815636&EM=michelle@waysidepublishing.com')
    return response.read()

def getJustNewDataFrom(freshData):
    oldData = getOldData()
    if oldData == False: #no previous data
        return freshData
    if oldData!=freshData[:len(oldData)]:
        raise Exception("Data strings have different history.")
    newData = freshData[len(oldData):]
    return newData

def getOldData():
    if os.path.isfile("archive.csv") is not True:
        return False
    archiveFile = open("archive.csv","r")
    oldData = archiveFile.read()
    archiveFile.close()
    return oldData

def archiveNewData(dataToArchive):
    archiveFile = open("archive.csv", "w+")
    archiveFile.write(dataToArchive)
    archiveFile.close()

def pushDataTo(newData,url):
    print newData
    pass

def main():
    print "Starting"
    freshData = getConfData()
    print "Got fresh data"
    newData = getJustNewDataFrom(freshData)
    print "Isolated new data"
    archiveNewData(freshData)
    print "Saved to archive"
    pushDataTo(newData,'')

main()