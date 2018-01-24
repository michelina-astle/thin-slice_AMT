from __future__ import print_function
import httplib2
import os
import sys
sys.path.insert(1, '/Library/Python/2.7/site-packages')
import random
import pprint
import csv
import re
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, 'PycharmProjects/AMT/input')  ## Change this to be wherever your drive-python-quickstart.json file is.
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
      #  print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    urlList = []
    refList = []
    trainingList = []

    results = service.files().list(
        ## Change the pageSize to be however many results you want it to return.
        ## If you're using the output file "MTurkCSVFile" as input for batches of 10 slices, make sure pageSize is divisible by 10.
        ## Change the hexadecimal string in q (query) to be the id of the folder you want it to extract files from (from the ID of the folder's URL: "....drive.google.com/drive/.../folders/"1wwDPvyIRDXWin1KSmWQD5AhUC7f8__MT")
        pageSize=800, q="'1wwDPvyIRDXWin1KSmWQD5AhUC7f8__MT' in parents", fields="nextPageToken, files(id, name)").execute()



        ### This is the 6 (for RAPT) training vidoes, so change pageSize if you have more or less than 6
        ### Change the hexadecmial string in q to be the folder ID for the folder they're in: (from the last part of the url... "https://drive.google.com/drive/u/0/folders/12hs0gnj1V3rNNZR8ynYmxebeWOacoIAa")
    trainingResults = service.files().list(
        pageSize=6, q="'12hs0gnj1V3rNNZR8ynYmxebeWOacoIAa' in parents", fields="nextPageToken, files(id, name)").execute()


    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')

        for item in items:
            item['src'] = "https://drive.google.com/file/d/{0}/preview".format(item["id"])
            src = item['src']
            title = item['name']
            print(title)

            # add to list
            urlList.append((title,src))
            refList.append((title, src))

    training = trainingResults.get('files', [])
    if not training:
        print('No files found.')
    else:
        print('Files:')

        for item in training:
            item['src'] = "https://drive.google.com/file/d/{0}/preview".format(item["id"])
            src = item['src']
            title = item['name']

            # add to list
            trainingList.append((title,src))
         #   refList.append((title, src))



    try:
        assert(len(urlList) == len(refList))
        assert(len(trainingList) == 5)
    except:
        print("Hmm something went wrong. Check the input")

    random.shuffle(urlList) # randomize list

    title = 'src'
    titles = [title + str(num) for num in range(1, 16)]
 #   print(urlList)



    # write to file - data for MTurk
    with open("MTurkCSVFile_WoZ_test1.csv", "wb") as csvFile:   ## Change batch# for every batch
        csvwriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(titles)
        num = 1
        round = 1
        srcs = []
        extra = []

        remainder = len(urlList) % 10    ## Finds the number of slices that won't fit into a complete batch of 10 slices
        divis = len(urlList) - remainder ## Finds the number of slices divisible by 10, for the complete "batches" of 10 slices
        #print(len(trainingList))
        trainingList = sorted(trainingList)
        for i in range(len(trainingList)):
            print(trainingList[i])
            srcs.append(trainingList[i][1])
        for title,src in urlList:
               # print(src[0])
            srcs.append(src)

            if round <= divis:
                if num == 10: ## Start over for each batch

                    csvwriter.writerow(srcs)  ## Add each src to the row
                    srcs = []
                    for i in range(len(trainingList)):
                        srcs.append(trainingList[i][1])
                    num = 0
                num += 1
            else:
                extra.append((title,src))  ## Add the remaining slices to an incomplete list, to be kept in the Google Drive folder for the next submission.
            round += 1
    csvFile.close()




    # write reference file to match MTurk data to video num later
    csvFile = open("VideoNameRef_WoZ_test1.csv", "w") ### Change "batch#" for each batch
    csvFile.write('Participant#' + 'Slice#' + ',' + 'title' + ',' + 'src' + "," + "UsageType")
    csvFile.write('\n')
    for title,src in refList:
        if any(src in s for s in extra):
            #print("HERE")
            usageType = "M"
        else:
            usageType = "U"
        for i in range(len(title)):
            if title[i] == "P":  ## Find the participant ID (e.g. "P1_Slice_16.csv")
                participantID = title[i+1:]
                participantID = participantID.split("_", 1)[0]
                print(participantID)

                if title[i+3] == "S":
                    slice = title[i+9:]
                else:
                    slice = title[i+10:]
                sep = '.'
                slice = slice.split(sep, 1)[0]
        csvFile.write(participantID + ',' + slice + ',' + title + ',' + src + "," + usageType)
        csvFile.write('\n')



    for title,src in trainingList:
        usageType = "T"
        for i in range(len(title)):
            if title[i] == "P":
                participantID = title[i+1:]
                participantID = participantID.split("_", 1)[0]
                print(participantID)

                if title[i+3] == "S":
                    slice = title[i+9:]
                else:
                    slice = title[i+10:]
                sep = '.'
                slice = slice.split(sep, 1)[0]
        csvFile.write(participantID + ',' + slice + ',' + title + ',' + src + "," + usageType)
        csvFile.write('\n')




    csvFile.close()



if __name__ == '__main__':
    main()