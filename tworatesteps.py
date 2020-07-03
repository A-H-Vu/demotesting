#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2020.1.3),
    on July 03, 2020, at 10:24
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard



# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2020.1.3'
expName = 'tworatesteps'  # from the Builder filename that created this script
expInfo = {'participant': 'test', 'taskVer': '1'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\Clifton\\Documents\\psych-proj\\forks\\demo2020-fork\\tworatesteps.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[2560, 1440], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "setup"
setupClock = core.Clock()
setupText = visual.TextStim(win=win, name='setupText',
    text='Use Mouse. Space continue',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
setupResp = keyboard.Keyboard()
# Do error checking for correct values of taskVer
try:
    taskVer = int(expInfo['taskVer']) # Check to see if this is safe
except ValueError:
    taskVer = 0

# variable to keep track of the trial number
trialNum = 0

# Variables to keep track of the order, rotation and target choices
orderChoice = taskVer % 6
rotationChoice = np.floor( taskVer / 12 ) % 2
targetChoice = np.floor( taskVer / 6) % 2

# Order 
order = [0,1,2] # Default choice
if (orderChoice == 0):
    order = [0,1,2]
elif (orderChoice == 1):
    order = [0,1,3]
elif (orderChoice == 2):
    order = [0,2,1]
elif (orderChoice == 3):
    order = [0,2,3]
elif (orderChoice == 4):
    order = [0,3,1]
elif (orderChoice == 5):
    order = [0,3,2]

# Rotation of the mouse angle
rotation = [1,-1] # Default choice
if (rotationChoice == 0):
    rotation = [1,-1]
elif (rotationChoice == 1):
    rotation = [-1,1]

# Choose set of angles for Main and Inverted task, respectively
targetAngles = [[40,50,130,140],[40,50],[130,140]] # Default choice
if (targetChoice == 0):
    targetAngles = [[40,50,130,140],[40,50],[130,140]]
elif (targetChoice == 1):
    targetAngles = [[40,50,130,140],[130,140],[40,50]]

ang = None
rtd = None

#Set up rotations and main tasks
# NOTE: JS isn't automatically converted with global keyword
def setAbruptMainTask():
    print('Abrupt Main Task')
    global ang
    global rtd
    ang = rotation[0] * 30
    rtd = ang*(pi/180)

def setRampedMainTask():
    print('Ramped Main Task')
    global ang
    global rtd
    if (trialsLoop.thisN <= 47):
        ang = rotation[0] * (trialsLoop.thisN+1)*0.625
    else:
        ang = rotation[0] * 30
    rtd = ang*(pi/180)

def setStepMainTask():
    print('Step Main Task')
    global ang
    global rtd
    if (trialsLoop.thisN <= 23):
        ang = rotation[0] * 7.5
    elif (trialsLoop.thisN > 23 and trialsLoop.thisN <= 47):
        ang = rotation[0] * 15
    elif (trialsLoop.thisN > 47 and trialsLoop.thisN <= 71):
        ang = rotation[0] * 22.5
    else:
        ang = rotation[0] * 30
    rtd = ang*(pi/180)

#Set up inverses
# Might be possible combine these with the Main task functions
def setAbruptInverseTask():
    print('Abrupt Inverse Task')
    global ang
    global rtd
    ang = rotation[1] * 30
    rtd = ang*(pi/180)

def setRampedInverseTask():
    print('Ramped Inverse Task')
    global ang
    global rtd
    if (trialsLoop.thisN <= 47):
        ang = rotation[1] * (trialsLoop.thisN+1)*0.625
    else:
        ang = rotation[1] * 30
    rtd = ang*(pi/180)

def setStepInverseTask():
    print('Step Inverse Task')
    global ang
    global rtd
    if (trialsLoop.thisN <= 23):
        ang = rotation[1] * 7.5
    elif (trialsLoop.thisN > 23 and trialsLoop.thisN <= 47):
        ang = rotation[1] * 15
    elif (trialsLoop.thisN > 47 and trialsLoop.thisN <= 71):
        ang = rotation[1] * 22.5
    else:
        ang = rotation[1] * 30
    rtd = ang*(pi/180)

# Initialize components for Routine "instruction"
instructionClock = core.Clock()
instructionText = visual.TextStim(win=win, name='instructionText',
    text='default text',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
instructionResp = keyboard.Keyboard()

# Initialize components for Routine "trial"
trialClock = core.Clock()
trialMouse = event.Mouse(win=win)
x, y = [None, None]
trialMouse.mouseClock = core.Clock()
trialTarget = visual.Polygon(
    win=win, name='trialTarget',
    edges=180, size=(0.05, 0.05),
    ori=0, pos=[0,0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1.0, depth=-2.0, interpolate=True)
trialHome = visual.Polygon(
    win=win, name='trialHome',
    edges=180, size=(0.05, 0.05),
    ori=0, pos=[0,0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1.0, depth=-3.0, interpolate=True)
trialCursor = visual.Polygon(
    win=win, name='trialCursor',
    edges=180, size=(0.025, 0.025),
    ori=0, pos=[0,0],
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1.0, depth=-4.0, interpolate=True)
# Set experiment start values for variable component trialStep
trialStep = 0
trialStepContainer = []
trialText = visual.TextStim(win=win, name='trialText',
    text='Any text\n\nincluding line breaks',
    font='Arial',
    pos=(-0.4, 0.4), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-6.0);
testSkip = keyboard.Keyboard()
trialBuff = visual.Polygon(
    win=win, name='trialBuff',
    edges=180, size=[1.0, 1.0],
    ori=0, pos=[0,0],
    lineWidth=1, lineColor=[-1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1.0, depth=-8.0, interpolate=True)
showAngle = visual.TextStim(win=win, name='showAngle',
    text='default text',
    font='Arial',
    pos=(-0.6, 0.3), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-9.0);

# Initialize components for Routine "end"
endClock = core.Clock()
endText = visual.TextStim(win=win, name='endText',
    text='thank you',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "setup"-------
continueRoutine = True
# update component parameters for each repeat
setupResp.keys = []
setupResp.rt = []
_setupResp_allKeys = []
# keep track of which components have finished
setupComponents = [setupText, setupResp]
for thisComponent in setupComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
setupClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "setup"-------
while continueRoutine:
    # get current time
    t = setupClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=setupClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *setupText* updates
    if setupText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        setupText.frameNStart = frameN  # exact frame index
        setupText.tStart = t  # local t and not account for scr refresh
        setupText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(setupText, 'tStartRefresh')  # time at next scr refresh
        setupText.setAutoDraw(True)
    
    # *setupResp* updates
    waitOnFlip = False
    if setupResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        setupResp.frameNStart = frameN  # exact frame index
        setupResp.tStart = t  # local t and not account for scr refresh
        setupResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(setupResp, 'tStartRefresh')  # time at next scr refresh
        setupResp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(setupResp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(setupResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if setupResp.status == STARTED and not waitOnFlip:
        theseKeys = setupResp.getKeys(keyList=['space'], waitRelease=False)
        _setupResp_allKeys.extend(theseKeys)
        if len(_setupResp_allKeys):
            setupResp.keys = _setupResp_allKeys[-1].name  # just the last key pressed
            setupResp.rt = _setupResp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in setupComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "setup"-------
for thisComponent in setupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "setup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
taskLoop = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('taskConds.xlsx', selection=order),
    seed=None, name='taskLoop')
thisExp.addLoop(taskLoop)  # add the loop to the experiment
thisTaskLoop = taskLoop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTaskLoop.rgb)
if thisTaskLoop != None:
    for paramName in thisTaskLoop:
        exec('{} = thisTaskLoop[paramName]'.format(paramName))

for thisTaskLoop in taskLoop:
    currentLoop = taskLoop
    # abbreviate parameter names if possible (e.g. rgb = thisTaskLoop.rgb)
    if thisTaskLoop != None:
        for paramName in thisTaskLoop:
            exec('{} = thisTaskLoop[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "instruction"-------
    continueRoutine = True
    # update component parameters for each repeat
    instructionText.setText(taskVersion)
    instructionResp.keys = []
    instructionResp.rt = []
    _instructionResp_allKeys = []
    # keep track of which components have finished
    instructionComponents = [instructionText, instructionResp]
    for thisComponent in instructionComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    instructionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "instruction"-------
    while continueRoutine:
        # get current time
        t = instructionClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=instructionClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instructionText* updates
        if instructionText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructionText.frameNStart = frameN  # exact frame index
            instructionText.tStart = t  # local t and not account for scr refresh
            instructionText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructionText, 'tStartRefresh')  # time at next scr refresh
            instructionText.setAutoDraw(True)
        
        # *instructionResp* updates
        waitOnFlip = False
        if instructionResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instructionResp.frameNStart = frameN  # exact frame index
            instructionResp.tStart = t  # local t and not account for scr refresh
            instructionResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instructionResp, 'tStartRefresh')  # time at next scr refresh
            instructionResp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(instructionResp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(instructionResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if instructionResp.status == STARTED and not waitOnFlip:
            theseKeys = instructionResp.getKeys(keyList=['space'], waitRelease=False)
            _instructionResp_allKeys.extend(theseKeys)
            if len(_instructionResp_allKeys):
                instructionResp.keys = _instructionResp_allKeys[-1].name  # just the last key pressed
                instructionResp.rt = _instructionResp_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instructionComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "instruction"-------
    for thisComponent in instructionComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "instruction" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trialsLoop = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(condsFile),
        seed=None, name='trialsLoop')
    thisExp.addLoop(trialsLoop)  # add the loop to the experiment
    thisTrialsLoop = trialsLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrialsLoop.rgb)
    if thisTrialsLoop != None:
        for paramName in thisTrialsLoop:
            exec('{} = thisTrialsLoop[paramName]'.format(paramName))
    
    for thisTrialsLoop in trialsLoop:
        currentLoop = trialsLoop
        # abbreviate parameter names if possible (e.g. rgb = thisTrialsLoop.rgb)
        if thisTrialsLoop != None:
            for paramName in thisTrialsLoop:
                exec('{} = thisTrialsLoop[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "trial"-------
        continueRoutine = True
        # update component parameters for each repeat
        # setup some python lists for storing info about the trialMouse
        trialMouse.x = []
        trialMouse.y = []
        trialMouse.leftButton = []
        trialMouse.midButton = []
        trialMouse.rightButton = []
        trialMouse.time = []
        gotValidClick = False  # until a click is received
        trialMouse.mouseClock.reset()
        win.mouseVisible = False
        
        print(taskLoop.thisN)
        print(trialsLoop.thisN % 4)
        
        # taskLoop.thisN refers to the outer loop - can be used to keep track of which loop we're on instead of using
        # loopCount
        if taskLoop.thisN == 0:
            targetangle = targetAngles[taskLoop.thisN][trialsLoop.thisN % 4] # targetAngles defined in instruction1
        else:
            targetangle = targetAngles[taskLoop.thisN][trialsLoop.thisN % 2]
        
        targetangle_rad = pi*(targetangle/180)
        targetPos = (cos(targetangle_rad)*0.4, sin(targetangle_rad)*0.4)
        
        homePos = [0, 0]
        
        targetOpacity = 0
        homeOpacity = 0
        #'buffer' circle set up
        bufferOpacity = 0
        bufferRadius = 0
        #allows cursor opacity changing
        cursorOpacity = 1
        cursorPosX = trialMouse.getPos()[0]
        cursorPosY = trialMouse.getPos()[1]
        
        homeStart = False
        reachOut = False
        
        trialStep = 1
        steps = []
        
        #print('trial: '+str(trials1.thisN)+' ('+str(globalClock.getTime())+')')
        trialText.text = str(trialsLoop.thisN+1)
        
        if phase == 'Align':
            print("Align task")
            
            trialCursor.pos = (1.5,1.5)
            trialMouse.pos = (1.5,1.5)
        elif phase == 'Error Clamped':
            print('Error Clamped Task')
        
            cursorOpacity = 0
        
            trialCursor.pos = (1.5,1.5)
            trialMouse.pos = (1.5,1.5)
        
            theta = (targetangle / 180) * pi
        elif (phase == 'Rotated'):
            trialCursor.pos = (1.5,1.5)
            trialMouse.pos = (1.5,1.5)
        
            if (taskVersion == 'Abrupt'):
                setAbruptMainTask()
            elif (taskVersion == 'Ramped'):
                setRampedMainTask()
            elif (taskVersion == 'Stepped'):
                setStepMainTask()
            else:
                setAbruptMainTask() # Contingency condition don't know if this is needed
                
        elif (phase == 'Inverted'):
            if (taskVersion == 'Abrupt'):
                setAbruptInverseTask()
            elif (taskVersion == 'Ramped'):
                setRampedInverseTask()
            elif (taskVersion == 'Stepped'):
                setStepInverseTask()
            else:
                setAbruptInverseTask() # Contingency condition don't know if this is needed
        
        #    trialText.text = str(ang)
        else:
            print("Align task")
            
            trialCursor.pos = (1.5,1.5)
            trialMouse.pos = (1.5,1.5)
        
        # Show the current angle on screen
        showAngle.text = str(ang)
        
        # Defined in setup
        thisExp.addData('trialNum', trialNum)
        trialNum = trialNum + 1
        thisExp.addData('angle', ang)
        if taskLoop.thisN != 0:
            thisExp.addData('rotationMultiplier', rotation[taskLoop.thisN-1])
        else:
            thisExp.addData('rotationMultiplier', 1)
        
        
        testSkip.keys = []
        testSkip.rt = []
        _testSkip_allKeys = []
        showAngle.setText(ang)
        # keep track of which components have finished
        trialComponents = [trialMouse, trialTarget, trialHome, trialCursor, trialText, testSkip, trialBuff, showAngle]
        for thisComponent in trialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "trial"-------
        while continueRoutine:
            # get current time
            t = trialClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=trialClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # *trialMouse* updates
            if trialMouse.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trialMouse.frameNStart = frameN  # exact frame index
                trialMouse.tStart = t  # local t and not account for scr refresh
                trialMouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trialMouse, 'tStartRefresh')  # time at next scr refresh
                trialMouse.status = STARTED
                prevButtonState = [0, 0, 0]  # if now button is down we will treat as 'new' click
            if trialMouse.status == STARTED:  # only update if started and not finished!
                x, y = trialMouse.getPos()
                trialMouse.x.append(x)
                trialMouse.y.append(y)
                buttons = trialMouse.getPressed()
                trialMouse.leftButton.append(buttons[0])
                trialMouse.midButton.append(buttons[1])
                trialMouse.rightButton.append(buttons[2])
                trialMouse.time.append(trialMouse.mouseClock.getTime())
            CursorTargetDistance = sqrt((trialCursor.pos[0]-trialTarget.pos[0])**2 + (trialCursor.pos[1]-trialTarget.pos[1])**2)
            CursorHomeDistance = sqrt(trialCursor.pos[0]**2 + trialCursor.pos[1]**2)
            
            steps.append(trialStep)
            # steps.push(step)
            
            if phase == 'Align':
                cursorPosX = trialMouse.getPos()[0]
                cursorPosY = trialMouse.getPos()[1]
            
                if not(homeStart):
                    homeOpacity = 1
                    targetOpacity = 0
                    cursorOpacity = 1
                    bufferOpacity = 0
                    trialStep = 1
                    if (CursorHomeDistance < .05):
                        homeStart = True
                        print('end step 1'+' ('+str(globalClock.getTime())+')')
            
                if (not(reachOut) and homeStart):
                    homeOpacity = 0
                    targetOpacity = 1
                    cursorOpacity = 1
                    bufferOpacity = 0
                    trialStep = 2
                    if (CursorTargetDistance < .05):
                        reachOut = True
                        print('end step 2'+' ('+str(globalClock.getTime())+')')
            
                if (reachOut):
                    homeOpacity = 1
                    targetOpacity = 0
                    cursorOpacity = 1
                    bufferOpacity = 0
                    trialStep = 3
                    if (CursorHomeDistance < .05):
                        # maybe this ends the loop prematurely?
                        print('end step 3'+' ('+str(globalClock.getTime())+')')
                        continueRoutine = False
                        
                #steps = steps.append(step)
            elif phase == 'Error Clamped':
                cursorPosX = sqrt((trialMouse.getPos()[0]**2)+(trialMouse.getPos()[1]**2))*(np.cos(theta))
                cursorPosY = sqrt((trialMouse.getPos()[0]**2)+(trialMouse.getPos()[1]**2))*(np.sin(theta))
            
                if not(homeStart):
                    homeOpacity = 1
                    targetOpacity = 0
                    trialStep = 1
                    bufferOpacity = 1
                    bufferRadius = 2*(sqrt(trialCursor.pos[0]**2 + trialCursor.pos[1]**2))
                    cursorOpacity = 0
                    if (CursorHomeDistance < .2):
                        cursorOpacity = 1
                    if (CursorHomeDistance < .075):
                        homeStart = True
                        print('end step 1'+' ('+str(globalClock.getTime())+')')
            
                if (not(reachOut) and homeStart):
                    homeOpacity = 0
                    targetOpacity = 1
                    trialStep = 2
                    bufferOpacity = 0
                    cursorOpacity = 1
                    if (CursorTargetDistance < .025):
                        reachOut = True
                        print('end step 2'+' ('+str(globalClock.getTime())+')')
            
                if (reachOut):
                    homeOpacity = 1
                    targetOpacity = 0
                    trialStep = 3
                    #COntrols the 'buffer'
                    bufferOpacity = 1
                    bufferRadius = 2*(sqrt(trialCursor.pos[0]**2 + trialCursor.pos[1]**2))
                    #controls the cursor
                    cursorOpacity = 0
                    if (CursorHomeDistance < .2):
                        cursorOpacity = 1
                    if (CursorHomeDistance < .075):
                        # maybe this ends the loop prematurely?
                        print('end step 3'+' ('+str(globalClock.getTime())+')')
                        continueRoutine = False
                        
                #steps = steps.append(step)
            elif (phase == 'Rotated' or phase == 'Inverted'):
                cursorPosX = (trialMouse.getPos()[0] * np.cos(rtd))-(trialMouse.getPos()[1] * np.sin(rtd))
                cursorPosY = (trialMouse.getPos()[0] * np.sin(rtd))+(trialMouse.getPos()[1] * np.cos(rtd))
            
                if not(homeStart):
                    homeOpacity = 1
                    targetOpacity = 0
                    cursorOpacity = 1
                    bufferOpacity = 0
                    trialStep = 1
                    if (CursorHomeDistance < .05):
                        homeStart = True
                        print('end step 1'+' ('+str(globalClock.getTime())+')')
            
                if (not(reachOut) and homeStart):
                    homeOpacity = 0
                    targetOpacity = 1
                    cursorOpacity = 1
                    bufferOpacity = 0
                    trialStep = 2
                    if (CursorTargetDistance < .05):
                        reachOut = True
                        print('end step 2'+' ('+str(globalClock.getTime())+')')
            
                if (reachOut):
                    homeOpacity = 1
                    targetOpacity = 0
                    cursorOpacity = 1
                    bufferOpacity = 0
                    trialStep = 3
                    if (CursorHomeDistance < .05):
                        # maybe this ends the loop prematurely?
                        print('end step 3'+' ('+str(globalClock.getTime())+')')
                        continueRoutine = False
                        
                #steps = steps.append(step)
            else:
                cursorPosX = trialMouse.getPos()[0]
                cursorPosY = trialMouse.getPos()[1]
            
                if not(homeStart):
                    homeOpacity = 1
                    targetOpacity = 0
                    cursorOpacity = 1
                    bufferOpacity = 0
                    trialStep = 1
                    if (CursorHomeDistance < .05):
                        homeStart = True
                        print('end step 1'+' ('+str(globalClock.getTime())+')')
            
                if (not(reachOut) and homeStart):
                    homeOpacity = 0
                    targetOpacity = 1
                    cursorOpacity = 1
                    bufferOpacity = 0
                    trialStep = 2
                    if (CursorTargetDistance < .05):
                        reachOut = True
                        print('end step 2'+' ('+str(globalClock.getTime())+')')
            
                if (reachOut):
                    homeOpacity = 1
                    targetOpacity = 0
                    cursorOpacity = 1
                    bufferOpacity = 0
                    trialStep = 3
                    if (CursorHomeDistance < .05):
                        # maybe this ends the loop prematurely?
                        print('end step 3'+' ('+str(globalClock.getTime())+')')
                        continueRoutine = False
                        
                #steps = steps.append(step)
            
            # *trialTarget* updates
            if trialTarget.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trialTarget.frameNStart = frameN  # exact frame index
                trialTarget.tStart = t  # local t and not account for scr refresh
                trialTarget.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trialTarget, 'tStartRefresh')  # time at next scr refresh
                trialTarget.setAutoDraw(True)
            if trialTarget.status == STARTED:  # only update if drawing
                trialTarget.setOpacity(targetOpacity, log=False)
                trialTarget.setPos(targetPos, log=False)
            
            # *trialHome* updates
            if trialHome.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trialHome.frameNStart = frameN  # exact frame index
                trialHome.tStart = t  # local t and not account for scr refresh
                trialHome.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trialHome, 'tStartRefresh')  # time at next scr refresh
                trialHome.setAutoDraw(True)
            if trialHome.status == STARTED:  # only update if drawing
                trialHome.setOpacity(homeOpacity, log=False)
                trialHome.setPos((0, 0), log=False)
            
            # *trialCursor* updates
            if trialCursor.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trialCursor.frameNStart = frameN  # exact frame index
                trialCursor.tStart = t  # local t and not account for scr refresh
                trialCursor.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trialCursor, 'tStartRefresh')  # time at next scr refresh
                trialCursor.setAutoDraw(True)
            if trialCursor.status == STARTED:  # only update if drawing
                trialCursor.setOpacity(cursorOpacity, log=False)
                trialCursor.setPos([cursorPosX, cursorPosY], log=False)
            
            # *trialText* updates
            if trialText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trialText.frameNStart = frameN  # exact frame index
                trialText.tStart = t  # local t and not account for scr refresh
                trialText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trialText, 'tStartRefresh')  # time at next scr refresh
                trialText.setAutoDraw(True)
            
            # *testSkip* updates
            waitOnFlip = False
            if testSkip.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                testSkip.frameNStart = frameN  # exact frame index
                testSkip.tStart = t  # local t and not account for scr refresh
                testSkip.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(testSkip, 'tStartRefresh')  # time at next scr refresh
                testSkip.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(testSkip.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(testSkip.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if testSkip.status == STARTED and not waitOnFlip:
                theseKeys = testSkip.getKeys(keyList=['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm'], waitRelease=False)
                _testSkip_allKeys.extend(theseKeys)
                if len(_testSkip_allKeys):
                    testSkip.keys = _testSkip_allKeys[-1].name  # just the last key pressed
                    testSkip.rt = _testSkip_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # *trialBuff* updates
            if trialBuff.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trialBuff.frameNStart = frameN  # exact frame index
                trialBuff.tStart = t  # local t and not account for scr refresh
                trialBuff.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trialBuff, 'tStartRefresh')  # time at next scr refresh
                trialBuff.setAutoDraw(True)
            if trialBuff.status == STARTED:  # only update if drawing
                trialBuff.setOpacity(bufferOpacity, log=False)
                trialBuff.setPos(homePos, log=False)
                trialBuff.setSize(bufferRadius, log=False)
            
            # *showAngle* updates
            if showAngle.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                showAngle.frameNStart = frameN  # exact frame index
                showAngle.tStart = t  # local t and not account for scr refresh
                showAngle.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(showAngle, 'tStartRefresh')  # time at next scr refresh
                showAngle.setAutoDraw(True)
            if showAngle.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > showAngle.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    showAngle.tStop = t  # not accounting for scr refresh
                    showAngle.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(showAngle, 'tStopRefresh')  # time at next scr refresh
                    showAngle.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store data for trialsLoop (TrialHandler)
        trialsLoop.addData('trialMouse.x', trialMouse.x)
        trialsLoop.addData('trialMouse.y', trialMouse.y)
        trialsLoop.addData('trialMouse.leftButton', trialMouse.leftButton)
        trialsLoop.addData('trialMouse.midButton', trialMouse.midButton)
        trialsLoop.addData('trialMouse.rightButton', trialMouse.rightButton)
        trialsLoop.addData('trialMouse.time', trialMouse.time)
        trialsLoop.addData('trialMouse.started', trialMouse.tStartRefresh)
        trialsLoop.addData('trialMouse.stopped', trialMouse.tStopRefresh)
        # thisExp.addData('step', stepvector)
        # reset the angles for the next task
        ang = None
        rtd = None
        thisExp.addData('step', steps)
        thisExp.addData('targetangle_deg', targetangle)
        
        # psychoJS.experiment.addData('columnName', variable)
        #psychoJS.experiment.addData('step', steps)
        #psychoJS.experiment.addData('targetangle_deg', targetangle)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'trialsLoop'
    
# completed 1 repeats of 'taskLoop'


# ------Prepare to start Routine "end"-------
continueRoutine = True
routineTimer.add(1.000000)
# update component parameters for each repeat
# keep track of which components have finished
endComponents = [endText]
for thisComponent in endComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
endClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "end"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = endClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=endClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *endText* updates
    if endText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        endText.frameNStart = frameN  # exact frame index
        endText.tStart = t  # local t and not account for scr refresh
        endText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(endText, 'tStartRefresh')  # time at next scr refresh
        endText.setAutoDraw(True)
    if endText.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > endText.tStartRefresh + 1.0-frameTolerance:
            # keep track of stop time/frame for later
            endText.tStop = t  # not accounting for scr refresh
            endText.frameNStop = frameN  # exact frame index
            win.timeOnFlip(endText, 'tStopRefresh')  # time at next scr refresh
            endText.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('endText.started', endText.tStartRefresh)
thisExp.addData('endText.stopped', endText.tStopRefresh)

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
