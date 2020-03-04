import cv2
import numpy as np
import copy
import sys
import pygame
from pygame import midi
from time import sleep

sys.path.insert(0, 'Drive_API')

import drive_api_write_file

########################### FUNCTION ###########################

def arrangeNotation( start, end ):
    notationList = list()
    collect = line[start:end].split(", ")
    print('collect : ', collect)
    index = 0
    for number in collect:
        # print('index : ', index)
        if collect.index(number)%4 == 0:
            notationList.append([])
            # print(number[1:])
            notationList[index].append(int(number[1:]))
        elif collect.index(number)%4 == 3:
            # print(number[:-1])
            notationList[index].append(int(number[:-1]))
            index += 1
        else:
            # print(number)
            notationList[index].append(int(number))
    # print('notationList : ', notationList)
    return notationList

######################### Read and arrange Dict #########################

# f = open('music_notation_location_test.txt', 'r')
f = open('00002.txt', 'r')


checkFirst = True
detectedDict = dict()

for line in f:
    
    if checkFirst:
        #   get rid of \n
        imagePath = str(line[:-1])
        print(imagePath)
        checkFirst = False

    else:
        start = line.find('treble') + 10
        end = line.find('bass') - 4
        # print('line[start:end] : ', line[start:end])
        if line[start:end]:
            notationList = arrangeNotation( start, end )
            detectedDict['treble'] = notationList

        start = line.find('bass') + 8
        end = line.find('blacknote') - 4
        # print('line[start:end] : ', line[start:end])
        if line[start:end]:
            notationList = arrangeNotation( start, end )
            detectedDict['bass'] = notationList

        start = line.find('blacknote') + 13
        end = line.find('whitenote') - 4
        # print('line[start:end] : ', line[start:end])
        if line[start:end]:
            notationList = arrangeNotation( start, end )
            detectedDict['blacknote'] = notationList

        start = line.find('whitenote') + 13
        end = line.find('wholenote') - 4
        # print('line[start:end] : ', line[start:end])
        if line[start:end]:
            notationList = arrangeNotation( start, end )
            detectedDict['whitenote'] = notationList
        
        start = line.find('wholenote') + 13
        end = len(line)-3
        # print('line[start:end] : ', line[start:end])
        if line[start:end]:
            notationList = arrangeNotation( start, end )
            detectedDict['wholenote'] = notationList

print('detectedDict : ', detectedDict)

########################## Read Image ##########################

#   read dataset image
img = cv2.imread(imagePath)

########################## Dummy dataset ########################

#   format of detectedDict
#   detectedDict[className].append( [x1, y1, x2, y2] )

#   00007.png
# trebleXCoor = [[169, 244], [54, 131]]
# trebleYCoor = [[220, 462], [530, 770]]
# detectedDict = {
#                 'treble': [[173, 232, 255, 445], [54, 542, 137, 763]], 
#                 'bass': [], 
#                 'blacknote': [[1399, 310, 1456, 349], [837, 394, 887, 432], [776, 393, 826, 432], [1318, 740, 1370, 775], [1323, 325, 1371, 363], [611, 411, 661, 448], [1145, 724, 1196, 760], [495, 426, 543, 466], [1156, 360, 1202, 396], [663, 410, 714, 448], [433, 426, 482, 466], [1241, 342, 1284, 377], [719, 411, 770, 448], [900, 376, 949, 414], [728, 690, 778, 729], [558, 412, 607, 449], [952, 375, 1005, 415], [384, 654, 434, 695], [559, 676, 605, 709], [219, 639, 267, 677], [976, 709, 1022, 744], [1005, 375, 1059, 415], [1059, 376, 1110, 415]], 
#                 'whitenote': [], 
#                 'wholenote': []
#                 }

#   00089.png
#   TODO : if treble not in front position we can filter it out by filter x value that more than... out
#   NOTE : this list already filter worng value out

# trebleXCoor = [[167, 206], [167, 206], [167, 205], [274, 313]]
# trebleYCoor = [[1627, 1733], [878, 981], [1255, 1357], [509, 616]]

#   00016.png
# trebleXCoor = [[158, 199], [158, 200], [159, 199], [159, 200], [158, 200], [159, 199], [238, 280]]
# trebleYCoor = [[1447, 1545], [765, 868], [935, 1035], [1794, 1895], [1281, 1382], [1965, 2063], [364, 462]]

#   00057.png
# trebleXCoor = [[131, 168], [131, 168], [130, 167], [131, 166]]
# trebleYCoor = [[635, 740], [1069, 1179], [1946, 2055], [1508, 1616]]

#   00058.png
# trebleXCoor = [[155, 187], [153, 186], [154, 187], [154, 187], [153, 186], [153, 187], [153, 186]]
# trebleYCoor = [[1309, 1379], [441, 515], [886, 958], [1516, 1586], [1735, 1806], [677, 750], [1097, 1169]]

#   mary-had-a-little-lamb.png
# trebleXCoor = [[274, 313], [172, 211], [172, 209], [173, 208]]
# trebleYCoor = [[480, 581], [1649, 1752], [1257, 1361], [866, 972]]

#   score1.png
# trebleXCoor = [[121, 189], [117, 189], [123, 190], [112, 179], [128, 194], [121, 188], [117, 180], [123, 189], [120, 187], [123, 185], [125, 189], [121, 184]]
# trebleYCoor = [[463, 644], [193, 368], [1003, 1180], [3017, 3186], [746, 922], [2239, 2419], [2757, 2923], [1488, 1665], [2000, 2172], [1254, 1418], [1755, 1927], [2542, 2714]]

####################################################################

trebleXCoor = list()
trebleYCoor = list()
bassXCoor = list()
bassYCoor = list()
noteXCoor = list()
noteYCoor = list()

for key in list( detectedDict.keys() ):
    for coor in detectedDict[key]:
        if key == 'treble':
            #   treble x coordinate
            trebleXCoor.append( [coor[0], coor[2]] )
            #   treble y coordinate
            trebleYCoor.append( [coor[1], coor[3]] )
        elif key == 'bass':
            bassXCoor.append( [coor[0], coor[2]] )
            bassYCoor.append( [coor[1], coor[3]] )
        else:
            noteXCoor.append( [coor[0], coor[2]] )
            noteYCoor.append( [coor[1], coor[3]] )

###################### Scaling image when use resize ###################
#   close this if not use scaling

imageScaling = 2

imageHeight = img.shape[0]
imageWidth = img.shape[1]

img = cv2.resize(img, ( int(imageWidth/2), int(imageHeight/2)) )

for x in [trebleXCoor, bassXCoor, noteXCoor]:
    #   change value in trebleXCoor
    for xTuple in x:
        xTuple[0] = int( xTuple[0]/imageScaling )
        xTuple[1] = int( xTuple[1]/imageScaling )

for y in [trebleYCoor, bassYCoor, noteYCoor]:
    #   change value in trebleYCoor
    for yTuple in y:
        yTuple[0] = int( yTuple[0]/imageScaling )
        yTuple[1] = int( yTuple[1]/imageScaling )

########################################################################

#   pick only 3 pixel from front of the G-clef, this will make line detection method more accuracy
widthGap = 20    #   if we close scaling image, sometimes it can't detect to line (change to 5 pixel)

allLineList = list()

assert len(trebleXCoor) == len(trebleYCoor), 'this 2 must be equal!'

#   choose line in sheet music that we want to detect line
for chooseBar in range( len(trebleXCoor) ):

    #   cut staff line that we want to use line detection
    crop = img[ trebleYCoor[chooseBar][0]:trebleYCoor[chooseBar][1] ]
    #   pick 5 pixel from G-clef
    lineImage = img[ trebleYCoor[chooseBar][0]:trebleYCoor[chooseBar][1], trebleXCoor[chooseBar][0]-widthGap:trebleXCoor[chooseBar][0]]
    # cv2.imshow('lineImage', lineImage)
    # cv2.waitKey(0)

    imageHeight = lineImage.shape[0]
    imageWidth = lineImage.shape[1]

    #   resize lineImage, so HoughLinesP can work with the larger image
    #   (HoughLinesP cannot work with 3 image pixel)
    lineImage = cv2.resize(lineImage, ( 150, imageHeight ) )
    # cv2.imshow('lineImage', lineImage)
    # cv2.waitKey(0)

    #   convert image to grayscale
    gray = cv2.cvtColor(lineImage, cv2.COLOR_BGR2GRAY)

    #   detect edges in image
    edges = cv2.Canny(gray, 100, 120, apertureSize=3)
    # cv2.imshow('edges', edges)

    #   detect line in image
    lines = cv2.HoughLinesP( edges, 1, np.pi/180, 100, minLineLength = 10, maxLineGap = 100 )

    horizontalLineList = list()
    horizontalLineDict = dict()
    print('lines : ', lines)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        horizontalLineList.append(y2)
        #   define y2 as a key
        horizontalLineDict[str(y2)] = ( x1, y1, x2, y2 )

    #   arrage number in horizontalLineList from least to most
    horizontalLineList.sort()
    print('horizontalLineList : {}' .format(horizontalLineList))

    #   list that will contain only  staff line (already filter from horizontalLineList)
    arrLineList = list()
    #   this flag will tell that next number will be skip and will not keep in to arrLineList
    isSameLine = False

    #   calculate approximate width gap between staff line
    gapBetweenLine = ( horizontalLineList[-1] - horizontalLineList[0] )/5

    #   arrange number in horizontalLineList and keep in to arrLineList
    for index in range( len( horizontalLineList ) ):

        #   if flag is true, skip and not keep this number in to arrLineList 
        if isSameLine == True:
            #   change flag to the normal state
            isSameLine = False
            continue

        #   when len( horizontalLineList ) is odd number, index+1 will out of range
        #   so we have to use try, except
        try:
            #   if value in next index - value in this index are less than gap between line,
            #   next number will not keep in to arrLineList
            if horizontalLineList[index+1] - horizontalLineList[index] < gapBetweenLine:
                #   change flag
                isSameLine = True

            #   append value in this index in to list
            arrLineList.append( horizontalLineList[index] )

        #   when len( horizontalLineList ) is odd, program will run in this exception
        except:
            #   append value in this index in to list
            arrLineList.append( horizontalLineList[index] )
            break

    print('arrLineList : {}' .format(arrLineList))

    #   if more than 5 staff line was detected, raise error 
    assert len(arrLineList) == 5, 'staff line are more or less than 5!'

    #   create new list in allLineList, this will divide staff line
    #   small list will collect only 5 line
    allLineList.append( [] )

    #   only choose line in arrLineList
    for y in arrLineList:
        x1, y1, x2, y2 = horizontalLineDict[str(y)]
        #   append all line in to allLineList (this line already add position of original sheet music)
        allLineList[-1].append(trebleYCoor[chooseBar][0] + y1)
        cv2.line( crop, (0, y1), (crop.shape[1], y2), (0, 255, 0), 1 )

    # cv2.imshow('image', crop)
    # cv2.waitKey(0)

    for line in allLineList[chooseBar]:
        cv2.line( img, (0, line), (img.shape[1], line), (0, 255, 0), 1 )

print('allLineList : {}' .format(allLineList))

# cv2.imshow('image', img)
# cv2.waitKey(0)

################################ Arrange Note #############################

noteX = list()
noteY = list()
noteArr = list()
medianLineList = list()

for index in range(len(noteYCoor)):
    #   find center of note
    if noteYCoor[index][1] < trebleYCoor[0][0] :
        continue
    noteY.append( int((noteYCoor[index][1] - noteYCoor[index][0])/2 + noteYCoor[index][0]) )
    noteX.append( int((noteXCoor[index][1] - noteXCoor[index][0])/2 + noteXCoor[index][0]) )

assert len(noteX) == len(noteY), 'this 2 must be equal!'

print('noteX : ', noteX)
print('noteY : ', noteY)

allBar = len(trebleXCoor)

#   allBar must equal to amount of list that append in noteArr
for bar in range( allBar ):
    noteXsort = list()
    noteYsort = list()

    #   find medain line between bar(staff line)
    if bar < allBar - 1:
        medianLine = int( (trebleYCoor[bar+1][0] - trebleYCoor[bar][1])/2 ) + trebleYCoor[bar][1]
    #   if this is last bar, medianLine = y coor of last treble
    else:
        medianLine = trebleYCoor[-1][-1]

    #   index of noteX and noteY are relate to each other
    for index in range( len(noteY) ):
        if noteY[index] < medianLine:
            noteYsort.append( noteY[index] )
            noteXsort.append( noteX[index] )

    tmpx = copy.deepcopy( noteXsort )
    tmpy = copy.deepcopy( noteYsort )
    noteYsort = list()
    #   sort x pixel from first -> last
    noteXsort.sort()

    for number in noteXsort:
        noteYsort.append( tmpy[ tmpx.index(number) ] )

    print('noteXsort : ', noteXsort)
    print('noteYsort : ', noteYsort)

    noteArr.append( [noteXsort, noteYsort] )

    for pixel in noteXsort:
        noteX.remove( pixel )
    for pixel in noteYsort:
        noteY.remove( pixel )

print('noteArr : ', noteArr)

############################# Note detection #############################

#   allLineList : [[137, 154, 171, 190, 205], [293, 310, 327, 346, 361]]

#   find top and bottom line, find average space between line and add to create new line
for bar in range( allBar ):
    avgSpace = 0
    for index in range(4):
        avgSpace += allLineList[bar][index+1] - allLineList[bar][index]
    avgSpace = int( avgSpace/4 )
    #   add top line
    allLineList[bar].insert(0, allLineList[bar][0] - avgSpace)
    #   add buttom line
    allLineList[bar].append( allLineList[bar][-1] + avgSpace )

    for line in allLineList[bar]:
        cv2.line( img, (0, line), (img.shape[1], line), (0, 255, 0), 1 )

print('allLineList : {}' .format(allLineList))

checkingLineList = list()

for bar in range( allBar ):
    checkingLineList.append( [] )
    for index in range( len(allLineList[bar]) ):
        checkingLineList[bar].append( allLineList[bar][index] )
        if index < len(allLineList[bar]) - 1:
            checkingLineList[bar].append( int( (allLineList[bar][index+1] - allLineList[bar][index])/2 ) + allLineList[bar][index] )

print('checkingLineList : ', checkingLineList)

############################ Make Decision ############################

detectedNote = list()
dataNote = list()

for bar in range( allBar ):
    checkSpace = int( ( allLineList[bar][1] - allLineList[bar][0] )/4 )
    detectedNote.append( [] )
    for note in noteArr[bar][1]:
        if note <= checkingLineList[bar][0] - checkSpace:
            detectedNote[bar].append('B5')
            dataNote.append(83)
        elif note >= checkingLineList[bar][0] - checkSpace and note <= checkingLineList[bar][0] + checkSpace:
            detectedNote[bar].append('A5')
            dataNote.append(81)
        elif note >= checkingLineList[bar][1] - checkSpace and note <= checkingLineList[bar][1] + checkSpace:
            detectedNote[bar].append('G5')
            dataNote.append(79)
        elif note >= checkingLineList[bar][2] - checkSpace and note <= checkingLineList[bar][2] + checkSpace:
            detectedNote[bar].append('F5')
            dataNote.append(77)
        elif note >= checkingLineList[bar][3] - checkSpace and note <= checkingLineList[bar][3] + checkSpace:
            detectedNote[bar].append('E5')
            dataNote.append(76)
        elif note >= checkingLineList[bar][4] - checkSpace and note <= checkingLineList[bar][4] + checkSpace:
            detectedNote[bar].append('D5')
            dataNote.append(74)
        elif note >= checkingLineList[bar][5] - checkSpace and note <= checkingLineList[bar][5] + checkSpace:
            detectedNote[bar].append('C5')
            dataNote.append(72)
        elif note >= checkingLineList[bar][6] - checkSpace and note <= checkingLineList[bar][6] + checkSpace:
            detectedNote[bar].append('B4')
            dataNote.append(71)
        elif note >= checkingLineList[bar][7] - checkSpace and note <= checkingLineList[bar][7] + checkSpace:
            detectedNote[bar].append('A4')
            dataNote.append(69)
        elif note >= checkingLineList[bar][8] - checkSpace and note <= checkingLineList[bar][8] + checkSpace:
            detectedNote[bar].append('G4')
            dataNote.append(67)
        elif note >= checkingLineList[bar][9] - checkSpace and note <= checkingLineList[bar][9] + checkSpace:
            detectedNote[bar].append('F4')
            dataNote.append(65)
        elif note >= checkingLineList[bar][10] - checkSpace and note <= checkingLineList[bar][10] + checkSpace:
            detectedNote[bar].append('E4')
            dataNote.append(64)
        elif note >= checkingLineList[bar][11] - checkSpace and note <= checkingLineList[bar][11] + checkSpace:
            detectedNote[bar].append('D4')
            dataNote.append(62)
        elif note >= checkingLineList[bar][12] - checkSpace and note <= checkingLineList[bar][12] + checkSpace:
            detectedNote[bar].append('C4')
            dataNote.append(60)
        elif note >= checkingLineList[bar][12] + checkSpace:
            detectedNote[bar].append('B3')
            dataNote.append(59)

print('detectedNote : ', detectedNote)
print('dataNote : ', dataNote)

# dataNote = [72, 74, 76, 69, 69, 67, 69, 69, 67, 69, 72, 71, 71, 72, 74, 67, 67, 64, 67, 67, 64, 67, 69, 69, 71, 72, 74, 76, 76, 74, 76, 76, 74, 76, 84, 83, 79, 76, 74, 72, 71, 72, 74, 76, 76, 76, 74, 76, 76, 74, 76, 77, 77, 76, 74, 74, 74, 72, 74, 74, 72, 79, 81, 79, 76, 76, 74, 74, 72, 74, 76, 72, 74, 76, 69, 74, 76, 67, 69, 72, 74, 76, 79, 76, 74]

# cv2.imshow('image', img)
# cv2.waitKey(0)

################################ Midi Keyboard ################################

noteToDataDict = {'F3' : 53, 'G3' : 55, 'A3' : 57, 'B3' : 59, 'C4' : 60, 'D4' : 62, 'E4' : 64,
                    'F4' : 65, 'G4' : 67, 'A4' : 69, 'B4' : 71, 'C5' : 72, 'D5' : 74, 'E5' : 76,
                    'F5' : 77, 'G5' : 79, 'A5' : 81, 'B5' : 83, 'C6' : 84
                }

dataToNoteDict = {'53' : 'F3', '55' : 'G3', '57' : 'A3', '59' : 'B3', '60' : 'C4', '62' : 'D4', '64' : 'E4',
                    '65' : 'F4', '67' : 'G4', '69' : 'A4', '71' : 'B4', '72' : 'C5', '74' : 'D5', '76' : 'E5',
                    '77' : 'F5', '79' : 'G5', '81' : 'A5', '83' : 'B5', '84' : 'C6'
                }

noteToPosition = {'F3' : 180, 'G3' : 223, 'A3' : 265, 'B3' : 309, 'C4' : 353, 'D4' : 396, 'E4' : 439,
                    'F4' : 482, 'G4' : 526, 'A4' : 569, 'B4' : 612, 'C5' : 656, 'D5' : 699, 'E5' : 742,
                    'F5' : 785, 'G5' : 828, 'A5' : 871, 'B5' : 914, 'C6' : 957
                }

pygame.init()
pygame.midi.init()
screen = pygame.display.set_mode((1005, 410))

pygame.display.set_caption('GUI Keyboard')
image = pygame.image.load(r'D:\Jester_Blog\Sheet music reader project\GUI Keyboard resize.jpg')

for n in range(pygame.midi.get_count()):
    print(n, pygame.midi.get_device_info(n))

#   input -> midi keyboard
my_input = pygame.midi.Input(1)
#   output -> laptop keyboard
midiout = pygame.midi.Output(0)
midiout.set_instrument(0)

print('START...')

move = 0

font = pygame.font.Font('freesansbold.ttf', 40) 


run = True
#Main loop
while(run):

    screen.blit(image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('END...')
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and move != 0:
            print('restart')
            move = 0

    if move == 0:
        text = font.render( dataToNoteDict[str(dataNote[move])], True, (0, 0, 0)) 
        screen.blit( text, (485, 50) )
        pygame.draw.circle(screen, (255, 0, 0), ( noteToPosition[ dataToNoteDict[str(dataNote[move])] ], 370 ), 15, 0)
        pygame.display.update()

    #   this must not in for event loop!!!
    if my_input.poll():
        #   read data from input device
        readData = my_input.read(1)[0]
        data = readData[0]
        #   data[0] : 128, 144 -> up key and down key
        #   data[1] : note number
        #   data[2] : velocity
        # print (data)
        # print (number_to_note(data[1]), data[2])
        # print('data[1] : ', data[1])
        if data[0] == 144:
            midiout.note_on(data[1], data[2])
        if data[0] == 128:
            midiout.note_off(data[1], 0)

        if move == len(dataNote):
            text = font.render( 'End Song!! Press R to restart', True, (0, 0, 0)) 
            screen.blit( text, (250, 50) )
            pygame.display.update()
            continue
            
        text = font.render( dataToNoteDict[str(dataNote[move])], True, (0, 0, 0)) 
        screen.blit( text, (485, 50) )
        pygame.draw.circle(screen, (255, 0, 0), ( noteToPosition[ dataToNoteDict[str(dataNote[move])] ], 370 ), 15, 0)
        pygame.display.update()


        if data[1] == dataNote[move] and data[0] == 144:
            move += 1

