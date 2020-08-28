import logging, sys, re


import azure.functions as func


def main(myblob: func.InputStream):


    #Read the blob file from the blob storage
    lines = myblob.readlines()

    #Close off the file
    #transFile.close()

    #Tags for opening and closing name in transcipt
    charOpenName = '<v '
    charCloseName = '>'

    #Create List of speakers
    speakerList = {}

    #What were the total words spoken
    totalWordsSpoken = 0


    #Count 1 Dynamic count on not knowing who is in the call
    #As we count each line check on the speaker to see who it is, and count the number of words spoken
    for textLine in lines:

        #Lets make sure we decode the line from binary to text
        newTxtLine = textLine.decode('utf-8')

        #Check to see if its a spoken line
        if newTxtLine[:len(charOpenName)] == charOpenName:
            #We need to find the occurrence of the first closing tag
            closePos = newTxtLine.find(charCloseName)
            #If this is a spoken line, lets look for the persons name
            speakerName = newTxtLine[len(charOpenName):closePos]
            
            if speakerName not in speakerList:
                #Insert the new speaker and increment the line count by 1
                speakerList[speakerName] = len(re.findall(r'\w+', newTxtLine[closePos:len(newTxtLine)-4]))
            else:
                #if the speaker already exists we need to find the speaker and increment their line count
                speakerList[speakerName] += len(re.findall(r'\w+', newTxtLine[closePos:len(newTxtLine)-4]))

            totalWordsSpoken += len(re.findall(r'\w+', newTxtLine[closePos:len(newTxtLine)-4]))

    #TODO: Can we try and do something here that connects to the length of time people spoke. We would need to take line 1 for time taken, and then line 2 to determine who spoke.



    #Code to sort output
    sortedSpeakers = sorted(speakerList.items(), key=lambda x: x[1], reverse=True)

    print('Of the', totalWordsSpoken, 'words spoken.')

    #Output the speaker list
    for x in sortedSpeakers:
        
        print(str(x[0]), 'spoke', '{:.1%}'.format(x[1]/totalWordsSpoken), 'of the time.')    
    