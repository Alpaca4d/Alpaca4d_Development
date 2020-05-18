﻿import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper
#import System as sy #DV
import sys

'''
ghFilePath = ghenv.LocalScope.ghdoc.Path
ghFileName = ghenv.LocalScope.ghdoc.Name
folderNameLength = len(ghFilePath)-len(ghFileName)-2 #have to remove '.gh'
ghFolderPath = ghFilePath[0:folderNameLength]

outputPath = ghFolderPath + 'assembleData'
wrapperFile = ghFolderPath + 'assembleData\\openSeesModel.txt'

userObjectFolder = Grasshopper.Folders.DefaultUserObjectFolder
fileName = userObjectFolder + 'Alpaca'
'''
fileName = r'C:\GitHub\Alpaca4d\PythonScript\function'
sys.path.append(fileName)
# importante mettere import 'import Rhino.Geometry as rg' prima di importatre DomeFunc
import DomeFunc as dg 

#---------------------------------------------------------------------------------------#

diplacementWrapper = openSeesOutputWrapper[0]
reactionOut = openSeesOutputWrapper[1]
#print( len( reactionOut ) )

pointWrapper = []

for index,item in enumerate(diplacementWrapper):
    pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )

## Dict. for point ##
pointWrapperDict = dict( pointWrapper )

## per scalare le reazioni #
rowReaction = [row[1] for row in reactionOut ]
valorReaction = []
for valor in rowReaction:
    rx = mt.fabs( valor[0] )
    ry = mt.fabs( valor[1] )
    rz = mt.fabs( valor[2] )
    mx = mt.fabs( valor[0] )
    my = mt.fabs( valor[1] )
    mz = mt.fabs( valor[2] )
    valorReaction.append( [ rx, ry, rz, mx, my, mz ] )

rx = max([row[0] for row in valorReaction ])
ry = max([row[1] for row in valorReaction ])
rz = max([row[2] for row in valorReaction ])
mx = max([row[3] for row in valorReaction ])
my = max([row[4] for row in valorReaction ])
mz = max([row[5] for row in valorReaction ])
# -------------------------------------------------------#

ReactionForce = []
ReactionMoment = []
viewElement = []
tagPoints = []
for value in reactionOut:
    pointIndex = value[0]
    tagPoints.append( pointIndex )
    point = pointWrapperDict.get( pointIndex , "never")
    Rx = rg.Vector3d( value[1][0], 0, 0 )
    Ry = rg.Vector3d( 0,value[1][1], 0 )
    Rz = rg.Vector3d( 0,0, value[1][2] )
    Mx = rg.Vector3d( value[1][3], 0, 0 )
    My = rg.Vector3d( 0, value[1][4], 0 )
    Mz = rg.Vector3d( 0,0, value[1][5] )
    Rxyz = Rx + Ry + Rz
    Mxyz = Mx + My + Mz
    viewElement.append( [ point, Rx/rx, Ry/ry, Rz/rz, Mx/mx, My/my, Mz/mz ] )
    ReactionForce.append( Rxyz )
    ReactionMoment.append( Mxyz )

point = [row[0] for row in viewElement ]
Rx = [row[1] for row in viewElement ]
Ry = [row[2] for row in viewElement ]
Rz = [row[3] for row in viewElement ]
Mx = [row[4] for row in viewElement ]
My = [row[5] for row in viewElement ]
Mz = [row[6] for row in viewElement ]

if reactionForcesView == True:
    view = th.list_to_tree( [ point, Rx, Ry, Rz ]  )

if reactionMomentsView == True:
    view = th.list_to_tree( [ point, Mx, My, Mz ]  )