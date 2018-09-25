import urllib.request
import os
import os.path
import csv

# Global varibles
new_fn = 'new_data.csv'
old_fn = 'archive.csv'
delta_fn = 'delta.csv'

def getConfData():
    sc = 'ACTF1117'
    exid = '1815636'
    em = 'michelle@waysidepublishing.com'
    
    url = 'http://www.xpressleadpro.com/Leads/Leads_Download_All.php?SC=%s&EXID=%s&EM=%s' % (sc, exid, em)
    with urllib.request.urlopen(url) as response, open(new_fn, 'wb') as out_file:
        data = response.read()
        out_file.write(data)
        return out_file   

def getJustNewDataFrom():
    # If "archive.csv" doesn't exist, that means this is the first set of data ever downloaded
    if os.path.isfile(old_fn) is not True: 
        return new_fn

    else:
        with open(delta_fn, 'a') as delta_file, open(old_fn, 'r') as old_file, open(new_fn, 'r') as new_file:
            old_file_data = csv.DictReader(old_file)
            new_file_data = csv.DictReader(new_file)

            headers = new_file_data.fieldnames

            writer = csv.DictWriter(delta_file, fieldnames=headers)
            writer.writeheader()

            for line in new_file_data:
                if line not in old_file_data:
                    writer.writerow(line)

        return delta_fn

    # if oldData!=freshData[:len(oldData)]:
    #     raise Exception('Data strings have different history.')
    # newData = freshData[len(oldData):]

# def getOldData(ofn):
#     if os.path.isfile(ofn) is not True:
#         return False
#     archiveFile = open(ofn, 'r')
#     oldData = archiveFile.read()
#     archiveFile.close()
#     return oldData

def pushDataTo(fn, url):
    with open(fn, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

        for row in reader:
            for header in headers:
                print(row[header])

def cleanup():
    if(os.path.isfile(old_fn)):
        os.remove(old_fn)

    if(os.path.isfile(delta_fn)):
        os.remove(delta_fn)

    os.rename(new_fn, old_fn)

def main():

    # Getting fresh data
    new_data = getConfData()
    
    # Parsing through new data to check for duplicates bewteen "new_data.csv" and "archive.csv" if "archive.csv" exists
    parsed_data_fn = getJustNewDataFrom()
    
    # Push data to the LS and Pardot
    pushDataTo(parsed_data_fn, '')

    # Deleting "archive.csv" and "delta.csv" if necessary, renames "new_data.csv" to "archive.csv"
    cleanup()   

if __name__ == '__main__':
    main()