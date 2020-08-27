import sys

#Lets get the file first
#Add another comment

transFile = open(sys.argv[1], mode='r', encoding='utf-8-sig')
#Read the lines in to a list
lines = transFile.readlines()

#Close off the file
transFile.close()

#Tags for opening and closing name in transcipt
charOpenName = '<v '
charCloseName = '>'

#Create List of speakers
speakerList = {}

#Count 2 Dynamic count on not knowing who is in the call
#As we count each line check on the speaker to see who it is
for textLine in lines:
    #Check to see if its a spoken line
    if textLine[:len(charOpenName)] == charOpenName:
        #We need to find the occurrence of the first closing tag
        closePos = textLine.find(charCloseName)
        #If this is a spoken line, lets look for the persons name
        speakerName = textLine[len(charOpenName):closePos]
        
        if speakerName not in speakerList:
            #Insert the new speaker and increment the line count by 1
            speakerList[speakerName] = 1
        else:
            #if the speaker already exists we need to find the speaker and increment their line count
            speakerList[speakerName] += 1

#TODO: Can we try and do something here that connects to the length of time people spoke.
#TODO: We would need to take line 1 for time taken, and then line 2 to determine who spoke.

#Code to sort output
sortedSpeakers = sorted(speakerList.items(), key=lambda x: x[1], reverse=True)

#Output the speaker list
for x in sortedSpeakers:
    print(x[0], 'spoke', x[1], 'times.')

