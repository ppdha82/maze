
#-------------------------------------------------------------------------------
# Name:        mouse
# Purpose:     Micro mouse simulator
#
# Author:      hjkim
#
# Created:     05-06-2012
# Copyright:   (c) HyunJun Kim 2012. All Rights Reserved.
# Licence:     GPL 
#-------------------------------------------------------------------------------
# -*- coding: cp949 -*-

import  sys, os
import  time
from    array import *
from    math  import *
from    scipy import integrate
import  re
import  thread
import  Queue

import  wx
import  wx.lib.newevent
import  wx.lib.masked           as masked
import  wx.lib.rcsizer          as rcs

MAZE_SIZE           = ( 16, 16 )

USE_MOUSE_IMAGE = False
DRAW_MOUSE = True

MOUSE_CMD_PAUSE     = 2
MOUSE_CMD_STOP      = 10

MOUSE_SIZE      = ( 0.060, 0.080 )
MOUSE_CENTER    = ( 30, 40 )
MOUSE_L_WHEEL   = ( 2, 40 )
MOUSE_R_WHEEL   = ( 58, 40 )
        
#---------------------------------------------------------------------------
# MouseEnv 
#---------------------------------------------------------------------------

Directions = {
    'N'     :  0,
    'NE'    :  1,
    'E'     :  2,
    'SE'    :  3,
    'S'     :  4,
    'SW'    :  5,
    'W'     :  6,
    'NW'    :  7,
}

Turns = {
    'T0'    : 0,
    'TR45'  : 1,
    'TR90'  : 2,
    'TR135' : 3,
    'T180'  : 4,
    'TL135' : 5,
    'TL90'  : 6,
    'TL45'  : 7,
}
TSTOP = 8

class MouseEnv():
    def __init__(self, parent):

        # wheel and mouse size
        size = self.m_MouseSize = MOUSE_SIZE 
        self.wl = MOUSE_SIZE [ 0 ]

        # mouse velocity and acceleration
        self.vl = self.vr = 0.
        self.sl = self.sr = 0.

        # real mouse position and angle for movement calculation
        self.pc = [ 0., 0. ] 
        self.angle = radians ( 0. )

        # draw time 
        self.starttime = 0.
        self.currtime = 0.
        self.drawtime = 0.02
        self.drawedtime = 0.0

        # maze property 
        self.block = 0.180
        self.poll = 0.012
        self.MazeSize = ( 16, 16 )
        self.MazeStart = None
        self.MazeTarget = None
        self.MazeTargetSection = None 
        self.Walls = []

        # mouse position(x, y), direction in maze
        self.mpos = 35
        self.mdir = 0

        # wall index 
        self.WallIndexEven = None 
        self.WallIndexOdd = None 

    def SetEnv ( self, pos, angle, block, poll, start, target, target_section, drawtime = 0.04 ):
        self.pc = self.position = pos
        self.angle = angle
        self.block = block
        self.poll = poll
        self.MazeStart = start 
        self.MazeTarget = target
        self.MazeTargetSection = target_section
        self.drawtime = drawtime

        self.MakeWallIndex()

    def MakeWallIndex( self ):
        ( w, h ) = self.MazeSize = ( 16, 16 )
        self.WallIndexEven = []
        self.WallIndexOdd = []
        we = self.WallIndexEven
        wo = self.WallIndexOdd
        row = ( w + 1 ) * 2

        self.WallIndexOdd = {
            0: row,     # 'N'  
            1: 1,       # 'NE' 
            2: 0,       # 'E'  
            3: -33,     # 'SE' 
            4: -34,     # 'S'   
            5: -35,     # 'SW' 
            6: 0,       # 'W'  
            7: -1       # 'NW' 
        }
        self.WallIndexEven  = {
            0: 0,       # 'N'  
            1: 35,      # 'NE' 
            2: 2,       # 'E'  
            3: 1,       # 'SE' 
            4: 0,       # 'S'   
            5: -1,      # 'SW' 
            6: -2,      # 'W'  
            7: 33       # 'NW' 
        }

    def GetWallDir( self, widx, dir, turn ):
        ew = self.WallIndexEven
        ow = self.WallIndexOdd

        adir = ( dir + turn ) % 8
        if widx & 1:
            wall = widx + ow [ adir ] 
        else:
            wall = widx + ew [ adir ] 
        
        if widx == wall:
            return ( None, None )
        return ( wall, adir )

    def InitRun ( self ):
        self.vl = self.vr = 0.
        self.sl = self.sr = 0.
        self.currtime = self.starttime = self.drawdtime = time.time ()


#---------------------------------------------------------------------------
# MouseMotor
#---------------------------------------------------------------------------
g_r = 1   # using wheel velocity instead of angluar velocity v = w * r
g_vl0 = g_vr0 = 0.
g_al = g_ar = 0.
g_wl = 0.
g_angle = 0.

def GetAngle ( t ):
    vl0, vr0 = g_vl0, g_vr0
    al, ar  = g_al, g_ar
    wl  = g_wl 
    angle = (vr0 - vl0) / wl * t + ( ar - al ) / ( wl * 2 ) * t**2
    return angle 

def f_x ( t ):
    wl = ( g_vl0 + g_al * t ) / g_r
    wr = ( g_vr0 + g_ar * t ) / g_r
    angle = GetAngle (t)
    angle = angle + g_angle
    x = ( -g_r * sin ( angle ) / 2 ) * wl + ( -g_r * sin ( angle ) / 2 ) * wr
    return x

def f_y ( t ):
    wl = ( g_vl0 + g_al * t ) / g_r
    wr = ( g_vr0 + g_ar * t ) / g_r
    angle = GetAngle (t)
    angle = angle + g_angle
    y = (  g_r * cos ( angle ) / 2 ) * wl + (  g_r * cos ( angle ) / 2 ) * wr
    return y

class MouseMotor(MouseEnv):
    def __init__(self, parent):
        MouseEnv.__init__ ( self, parent )

    #-----------------------------------------------------------------------
    # Methods for overriding
    #-----------------------------------------------------------------------
    def DrawMouse ( self, pc, angle, redraw = True, color = 'White' ):
        print "make this routine"
        pass

    #-----------------------------------------------------------------------
    # Methods for mouse movement 
    #-----------------------------------------------------------------------
    def GetS ( self, al, ar, t ):
        vl0 = self.vl
        vr0 = self.vr
        vc0 = (vl0 + vr0) / 2
        ac  = (al + ar) / 2

        sl = vl0 * t + 0.5 * al * t ** 2
        sr = vr0 * t + 0.5 * ar * t ** 2
        s  = vc0 * t + 0.5 * ac * t ** 2 
        return ( s, sl, sr )

    def GetV ( self, al, ar, t ):
        vl0 = self.vl
        vr0 = self.vr
        vc0 = (vl0 + vr0) / 2
        ac  = (al + ar) / 2

        vl = vl0 + al * t
        vr = vr0 + ar * t
        vc = vr0 + ar * t
        return ( vc, vl, vr )

    def GetAngle ( self, al, ar, t ):
        vl0 = self.vl
        vr0 = self.vr
        wl  = self.wl
        angle = (vr0 - vl0) / wl * t + ( ar - al ) / ( wl * 2 ) * t**2
        return angle 

    def MovePoint ( self, p, l, angle ):
        ( x, y ) = p
        xo = x - l * sin ( angle )
        yo = y + l * cos ( angle )
        return ( xo, yo )

    def GetMove ( self, al, ar, t ):
        angle = self.GetAngle ( al, ar, t )
        ( x, error ) = integrate.quad ( f_x, 0, t )
        ( y, error ) = integrate.quad ( f_y, 0, t )
        return ( x, y, angle )

    def Move ( self, al, ar, dt ):
        global g_vl0, g_vr0, g_al, g_ar, g_wl, g_angle
        g_wl = self.wl
        g_vl0, g_vr0 = self.vl, self.vr
        g_al, g_ar = al, ar
        g_angle = self.angle

        currtime = self.currtime 
        deltadraw = self.drawtime
        while True:
            drawtime = self.drawedtime + deltadraw 
            if drawtime <= currtime + dt :
                if drawtime < currtime:
                    drawtime = currtime

                ( x, y, angle ) = self.GetMove ( al, ar, drawtime - currtime )
                angle = self.angle + angle
                pc = ( self.pc [ 0 ]  + x  , self.pc [ 1 ] + y )
                    
                realtime = time.time ()
                if drawtime > realtime:
                    time.sleep ( drawtime - realtime )

                self.drawedtime = drawtime
                self.DrawMouse( pc, angle, 'Green' )
            else:
                break

        # Updated status
        ( x, y, angle ) = self.GetMove ( al, ar, dt )
        angle = self.angle + angle
        pc = ( self.pc [ 0 ]  + x  , self.pc [ 1 ] + y )
        ( vc, vl, vr ) = self.GetV ( al, ar, dt )
        ( sc, sl, sr ) = self.GetS ( al, ar, dt )

        self.pc = pc
        self.angle = angle
        ( self.vl, self.vr ) = ( vl, vr )
        ( self.sl, self.sr ) = ( sl, sr )
        self.currtime = self.currtime + dt

        self.DrawMouse( pc, angle, 'Green' )
        
        print "RT/T=%.3f,%.3f,A=%.1f,V=%.3f,%.3f,%.3f,S=%.0f" % ( 
                ( time.time () - self.starttime ) * 1000, 
                ( self.currtime - self.starttime ) * 1000, 
                degrees ( self.angle ),
                vc,vl,vr, 
                sc * 1000
                )

    def GetTimeByAccel ( self, a, s, v0 ):
        a = abs ( a )
        if a == 0:
            t = s / v0
        else:
            t = ( -2 * v0 + sqrt( (2*v0)**2 + 8*a*s ) ) / ( 2 * a )
        return t

    def GetTimeByVelocity ( self, a, v, v0 ):
        t = ( v - v0 ) / a
        return t

    def GetAccelByTime ( self, t, s, v0 ):
        a = ( s - v0 * t ) * 2. / ( t**2. )
        return a

    def GetAccelByVelocity ( self, s, v, v0 ):
        a = ( v ** 2 - v0 ** 2 ) / ( 2 * s )
        return a 

    def MoveWithTimeDistance ( self, t, s ):
        a = self.GetAccelByTime ( t, s, self.vl ) 
        self.Move ( a, a, t) 

    def MoveWithAccelDistance ( self, a, s, max_v = 0 ):
        v0 = self.vl
        if not max_v:
            t = self.GetTimeByAccel ( a, s, v0 ) 
            self.Move ( a, a, t) 
        else:
            t = self.GetTimeByAccel ( a, s, v0 ) 
            tm = self.GetTimeByVelocity ( a, max_v, v0 )
            if t >= tm:
                self.Move ( a, a, t) 
            else:
                self.Move ( a, a, tm) 
                self.Move ( a, a, t-tm) 

    def MoveWithVelocityDistance ( self, v, s ):
        v0 = self.vl
        a = self.GetAccelByVelocity ( s, v, v0 ) 
        t = ( v - v0 ) / a
        self.Move ( a, a, t) 

    def MoveTurnAccel ( self, angle, right = False, time = 1 ):
        block = self.block
        poll = self.poll
        v0 = self.vl
        wl = self.wl
        r = block / 2.
        angle = radians ( angle ) 
        t = r * angle / v0 * time
        a = 2 * wl * angle / ( t ** 2 ) 
        
        if right:
            al, ar = 2*a, 0 
        else:
            al, ar = 0, 2*a

        self.Move ( al, ar, t/2) 
        self.Move ( -al, -ar, t/2) 
        
    def MoveTurn90 ( self, right = False ):
        v0 = self.vl
        wl = self.wl
        r = self.block / 2.
        angle = radians ( 90 ) 
        t = r * angle / v0 * 1.07
        a = 2 * wl * angle / ( t ** 2 ) 
        
        if right:
            al, ar = a, -a 
        else:
            al, ar = -a, a

        self.Move ( al, ar, t/2) 
        self.Move ( -al, -ar, t/2) 

    def MoveTurnInPlace ( self, angle, a, right = False ):
        wl = self.wl
        angle = radians ( angle ) / 2 
        t = sqrt ( wl * angle / a )
        
        if right:
            al, ar = a, -a
        else:
            al, ar = -a, a

        self.Move ( al, ar, t) 
        self.Move ( -al, -ar, t) 


#---------------------------------------------------------------------------
# MouseGyroSensor 
#---------------------------------------------------------------------------
class MouseGyroSensor (MouseEnv):
    def __init__(self, parent):
        MouseEnv.__init__ ( self, parent )

    def GetAngle ():
        # integral voltage and get angle and return it
        pass

#---------------------------------------------------------------------------
# MouseOpticalSensor 
#---------------------------------------------------------------------------
# Wall index for lookup
WALL_LU_N   = 0
WALL_LU_E   = 1
WALL_LU_S   = 2
WALL_LU_W   = 3

class MouseOpticalSensor(MouseEnv):
    def __init__(self, parent):
        MouseEnv.__init__ ( self, parent )

    def DetectAllWalls ( self ):
        maze = self.m_Maze

        for wall in range ( len ( self.Walls ) ) :
            print wall
            maze.DetectedWall ( wall, True )
            if self.Walls [ wall ] < WALL_EXIST:
                self.Walls [ wall ] = WALL_NONE
            else:
                self.Walls [ wall ] = WALL_DETECTED

    def DetectWall ( self ):
        maze = self.m_Maze
        pos = self.mpos 
        dir = self.mdir 

        # detectable area 44~84(half block) when mouse height 80
        ( f, d ) = self.GetWallDir( pos, dir, Turns [ 'T0' ] )
        ( l, d ) = self.GetWallDir( pos, dir, Turns [ 'TL45' ] )
        ( r, d ) = self.GetWallDir( pos, dir, Turns [ 'TR45' ] )
        maze.DetectedWall ( f, True )
        maze.DetectedWall ( l, True )
        maze.DetectedWall ( r, True )

        if self.Walls [ f ] < WALL_EXIST:
            self.Walls [ f ] = WALL_NONE
        else:
            self.Walls [ f ] = WALL_DETECTED

        if self.Walls [ l ] < WALL_EXIST:
            self.Walls [ l ] = WALL_NONE
        else:
            self.Walls [ l ] = WALL_DETECTED

        if self.Walls [ r ] < WALL_EXIST:
            self.Walls [ r ] = WALL_NONE
        else:
            self.Walls [ r ] = WALL_DETECTED


#---------------------------------------------------------------------------
# MouseBrain 
#---------------------------------------------------------------------------

# Wall type
WALL_NONE       = 0
WALL_UNKNOWN    = 1
WALL_EXIST      = 2
WALL_DETECTED   = 3
WALL_NO_MOVE    = 0xfe
WALL_MOVE       = 0xff
WALL_MAX_DIST   = 0xffff

MOVE_BLOCK      = 0
MOVE_HBLOCK     = 1
MOVE_LSTURN     = 2
MOVE_RSTURN     = 3
MOVE_BACK       = 4
MOVE_START      = 5
MOVE_STOP       = 6

MouseMoves = {
    'MOVE_BLOCK' : 0,
    'MOVE_HBLOCK': 1,
    'MOVE_LSTURN': 2,
    'MOVE_RSTURN': 3,
    'MOVE_BACK'  : 4,
    'MOVE_START' : 5,
    'MOVE_STOP'  : 6,
    'MOVE_NONE'  : 7,

    'F_T0'      : 30,
    'F_TL45'    : 31,
    'F_TL90'    : 32,
    'F_TL135'   : 33,
    'F_TL180'   : 34,
    'F_TR45'    : 35,
    'F_TR90'    : 36,
    'F_TR135'   : 37,
    'F_TR180'   : 38,
    'F_T0_STOP' : 39,

    'FD_T0'     : 40,
    'FD_TL45'   : 41,
    'FD_TL90'   : 42,
    'FD_TL135'  : 43,
    'FD_TR45'   : 45,
    'FD_TR90'   : 46,
    'FD_TR135'  : 47,
}

MAX_TURN_WEIGHT = 20

TurnsPriorityNormalPath = {
    'T0'    : 1,
    'TL45'  : 2,
    'TR45'  : 2,
    'T0_45' : 3,
    'TL90'  : 4,
    'TR90'  : 4,
    'TL135' : 5,
    'TR135' : 5,
    'T180'  : 5,
}

TurnsPriorityDiagonalPath = {
    'T0'    : 1,
    'T0_45' : 2,
    'TL90'  : 3,
    'TR90'  : 3,
    'TL45'  : 4,
    'TR45'  : 4,
    'TL135' : 5,
    'TR135' : 5,
    'T180'  : 5,
}

class MouseBrain(MouseMotor, MouseOpticalSensor, MouseGyroSensor):
    def __init__(self, parent):
        MouseMotor.__init__ ( self, parent )
        MouseOpticalSensor.__init__ ( self, parent )

        self.DirsMap = []
        self.DistanceMap = []
        self.MouseBuffer = []
        self.CurrWeight = 0
        self.CurrDistance = 0

        self.MouseCnt = 0
        self.TracePosition = []
        self.TraceTurn = []
        self.TraceUnknown = []
        self.TraceUnknownAll = []
        self.DrawRoute1 = []
        self.DrawRoute2 = []

        self.RunCount = 0 # 1st, 1st return, 2st, 2st return

        self.MazeSize = ( 16, 16 )
        self.MazeStart = None
        self.MazeTarget = None
        self.MazeTargetSection = None
        self.MazeUnknownTarget = None
        self.MazeTargetDetermined = None

        self.MaxAccel = 10
        self.MaxVelocity = 4
        self.MaxTurnVelocity = 1
 
    def InitDirsMap ( self, search_unknown ):
        maze = self.m_Maze
        self.MouseBuffer = []
        self.CurrWeight = 0
        self.DirsMap = []
        self.DistanceMap = []

        dirsmap = self.DirsMap
        for wall in self.Walls:
            self.DistanceMap.append ( WALL_MAX_DIST )

            if search_unknown:
                if wall <= WALL_EXIST:
                    dirsmap.append( WALL_MOVE )
                else:
                    dirsmap.append( WALL_NO_MOVE )
            else:
                if wall <= WALL_NONE:
                    dirsmap.append( WALL_MOVE )
                else:
                    dirsmap.append( WALL_NO_MOVE )

    def PushIMouse ( self, pos, dir, weight ):
        w = self.CurrWeight + weight
        buf = self.MouseBuffer
        buf.append ( ( w, pos, dir ) )
        self.DirsMap [ pos ] = dir 
        self.DistanceMap [ pos ] = w 

    def PopIMouse ( self ):
        cw = self.CurrWeight
        minidx = minw = WALL_MAX_DIST 
        buf = self.MouseBuffer

        while buf:
            for idx in range ( len ( buf ) ):
                ( w, p, d ) = buf [ idx ]
                if w == cw:
                    del buf [ idx ]
                    return ( p, d ) 
                if minw > w:
                    minw = w
                    minidx = idx

            if minw != WALL_MAX_DIST:
                self.CurrWeight = minw
                ( w, p, d ) = buf [ minidx ]
                del buf [ minidx ]
                return ( p, d ) 

        return ( None, None )

    def PushCanMove( self, pos, dir ):
        for turn in Turns:
            ( nextwall, nextdir ) = self.GetWallDir( pos, dir, Turns [ turn ] )
            
            if nextwall and self.DirsMap [ nextwall ] == WALL_MOVE:

                if turn == 'T0' and dir!=0 and dir!=2 and dir!=4 and dir!=6 :
                    turn = 'T0_45'
                turn_weight = TurnsPriorityDiagonalPath [ turn ]

                self.PushIMouse ( nextwall, nextdir, turn_weight )

    def RunIMouse ( self, pos, dir ):
        buf = self.MouseBuffer

        self.PushIMouse( pos, dir, 0 )

        while True:
            ( pos, dir ) = self.PopIMouse()
            if pos == None:
                break
            self.PushCanMove( pos, dir )

    def DrawDirsMap ( self ):
        NameOfDirections = {
            0: 'N',
            1: 'NE',
            2: 'E',
            3: 'SE',
            4: 'S',
            5: 'SW',
            6: 'W',
            7: 'NW',
            0xfe: '',
            0xff: 'X',
        }

        maze = self.m_Maze
        infos = []
        for dir in self.DirsMap:
            infos.append ( NameOfDirections [ dir ] )

        maze.SetAllWallInformation ( infos )
        maze.EnableAllWallInformation ( True )

    def DrawDistanceMap ( self ):
        maze = self.m_Maze
        infos = []
        for num in self.DistanceMap:
            if num < WALL_MAX_DIST:
                infos.append ( str ( num ) )
            else:
                infos.append ( '' )

        maze.SetAllWallInformation ( infos )
        maze.EnableAllWallInformation ( True )

    def DrawWallNum ( self ):
        maze = self.m_Maze
        walls = maze.GetAllWalls()
        infos = []
        for index in range ( len ( walls ) ) :
            infos.append ( "%d"%index )

        maze.SetAllWallInformation ( infos )
        maze.EnableAllWallInformation ( True )

    def InitAllTarget ( self ):
        maze = self.m_Maze

        # init start position
        start = maze.GetWallIndex ( self.MazeStart, WALL_LU_N )
        maze.DetectedWall ( start, True )
        self.Walls [ start ] = WALL_NONE

        start = maze.GetWallIndex ( self.MazeStart, WALL_LU_W )
        maze.DetectedWall ( start, True )
        self.Walls [ start ] = WALL_DETECTED

        # init target position
        if self.MazeTargetSection:
            ( ts, te ) = self.MazeTargetSection

            tpos = []

            for x in range ( ts [ 0 ], te [ 0 ]+1 ):
                xy = ( x, ts [ 1 ] )
                idx = maze.GetWallIndex ( xy, WALL_LU_S )
                tpos.append ( idx ) 

                xy = ( x, te [ 1 ] )
                idx = maze.GetWallIndex ( xy, WALL_LU_N )
                tpos.append ( idx ) 

            for y in range ( ts [ 1 ], te [ 1 ]+1 ):
                xy = ( ts [ 0 ], y ) 
                idx = maze.GetWallIndex ( xy, WALL_LU_W )
                tpos.append ( idx ) 

                xy = ( te [ 0 ], y ) 
                idx = maze.GetWallIndex ( xy, WALL_LU_E )
                tpos.append ( idx ) 

            for x in range ( ts [ 0 ], te [ 0 ]+1 ):
                for y in range ( ts [ 1 ], te [ 1 ]+1 ):
                    xy = ( x, y ) 

                    idx = maze.GetWallIndex ( xy, WALL_LU_N )
                    try:
                        tpos.index ( idx )
                    except ValueError:
                        maze.DetectedWall ( idx, True )
                        self.Walls [ idx ] = WALL_NONE

                    idx = maze.GetWallIndex ( xy, WALL_LU_E )
                    try:
                        tpos.index ( idx )
                    except ValueError:
                        maze.DetectedWall ( idx, True )
                        self.Walls [ idx ] = WALL_NONE

                    idx = maze.GetWallIndex ( xy, WALL_LU_S )
                    try:
                        tpos.index ( idx )
                    except ValueError:
                        maze.DetectedWall ( idx, True )
                        self.Walls [ idx ] = WALL_NONE

                    idx = maze.GetWallIndex ( xy, WALL_LU_W )
                    try:
                        tpos.index ( idx )
                    except ValueError:
                        maze.DetectedWall ( idx, True )
                        self.Walls [ idx ] = WALL_NONE

            self.MazeUnknownTarget = tpos
        
    def SetTarget ( self, target ):
        maze = self.m_Maze
        targets = self.MazeUnknownTarget
        self.MazeTargetDetermined = target
        for pos in targets: 
            if pos != target and ( maze.GetWall ( pos ) == WALL_UNKNOWN or maze.GetWall ( pos ) == WALL_EXIST ) :
                maze.DetectedWall ( pos, True )
                self.Walls [ pos ] = WALL_DETECTED

    def GetTarget ( self ):
        if self.MazeTarget:
            return self.MazeTarget

        if self.MazeTargetDetermined:
            return self.MazeTargetDetermined

        targets = self.MazeUnknownTarget
        min = WALL_MAX_DIST
        min_pos = WALL_MAX_DIST
        for pos in targets: 
            if self.DistanceMap [ pos ] < min:
                min = self.DistanceMap [ pos ]
                min_pos = pos
        # print "Target:", min_pos
        return min_pos

    def GetStart ( self ):
        maze = self.m_Maze
        return maze.GetWallIndex ( self.MazeStart, WALL_LU_N )

    def MakeDirsMap ( self, pos, dir, search_unknown = True ):
        self.InitDirsMap ( search_unknown ) 
        self.RunIMouse ( pos, dir )

    def DrawRoute ( self, enable, type ):
        route = self.TracePosition
        if not route or len ( route )<=1 :
            return

        if type == 0:
            if enable:
                if len ( route ) > 1:
                    route = route [ :-2 ]
                    if self.DrawRoute1 :
                        self.m_Maze.EnableWallPoints1 ( self.DrawRoute1, False, False ) 

                    self.m_Maze.EnableWallPoints1 ( route, True, True ) 
                    self.DrawRoute1 = route
            elif self.DrawRoute1:
                self.m_Maze.EnableWallPoints1 ( self.DrawRoute1, False, True ) 
                self.DrawRoute1 = [] 

        elif type == 1:
            if enable:
                if self.DrawRoute2 :
                    self.m_Maze.EnableWallPoints2 ( self.DrawRoute2, False, False ) 

                self.m_Maze.EnableWallPoints2 ( route, True, True ) 
                self.DrawRoute2 = route
            elif self.DrawRoute2:
                self.m_Maze.EnableWallPoints2 ( self.DrawRoute2, False, True ) 
                self.DrawRoute2 = [] 

    def MakeFastRoute ( self, Start=True, Stop_more = True ):
        block = self.block
        diag = sqrt ( 2 ) * ( block / 2. )

        TurnSeqs = self.TurnSeqs = ( 
            ( ( 'F_T0',     'FD_T0'),       ( Turns [ 'T0' ], ) ),
                         
            ( ( 'F_TL180',  ''),            ( Turns [ 'TL45' ], Turns [ 'TL90' ], Turns [ 'TL45' ] ) ),
            ( ( 'F_TL135',  ''),            ( Turns [ 'TL45' ], Turns [ 'TL90' ] ) ),
            ( ( 'F_TL90',   'FD_TL45'),     ( Turns [ 'TL45' ], Turns [ 'TL45' ] ) ),
            ( ( 'F_TL45',   'FD_TL45'),     ( Turns [ 'TL45' ], ) ),
            ( ( '',         'FD_TL135'),    ( Turns [ 'TL90' ], Turns [ 'TL45' ] ) ),
            ( ( '',         'FD_TL90'),     ( Turns [ 'TL90' ], ) ),
                         
            ( ( 'F_TR180',  ''),            ( Turns [ 'TR45' ], Turns [ 'TR90' ], Turns [ 'TR45' ] ) ),
            ( ( 'F_TR135',  ''),            ( Turns [ 'TR45' ], Turns [ 'TR90' ] ) ),
            ( ( 'F_TR90',   'FD_TR45'),     ( Turns [ 'TR45' ], Turns [ 'TR45' ] ) ),
            ( ( 'F_TR45',   'FD_TR45'),     ( Turns [ 'TR45' ], ) ),
            ( ( '',         'FD_TR135'),    ( Turns [ 'TR90' ], Turns [ 'TR45' ] ) ),
            ( ( '',         'FD_TR90'),     ( Turns [ 'TR90' ], ) ),
        )

        TurnDistance = {
            'F_T0'      : ( block, 0 ),
            'F_TL45'    : ( -0.05,  0.0788 ),
            'F_TL90'    : ( -0.024, block-0.024 ),
            'F_TL135'   : ( -0.075, 0),
            'F_TL180'   : ( -0.06,  block-0.06 ),
            'F_TR45'    : ( -0.05,  0.0788 ),
            'F_TR90'    : ( -0.024, block-0.024 ),
            'F_TR135'   : ( -0.075, 0),
            'F_TR180'   : ( -0.06,  block-0.06 ),

            'FD_T0'     : ( diag, 0 ),
            'FD_TL45'   : ( -0.049 , block-0.049 ),
            'FD_TL90'   : ( -diag/2-0.05, diag/2-0.05 ),
            'FD_TL135'  : ( -diag, block-0.075),
            'FD_TR45'   : ( -0.049 , block-0.049 ),
            'FD_TR90'   : ( -diag/2-0.05, diag/2-0.05 ),
            'FD_TR135'  : ( -diag, block-0.075),
        }

        turns = self.TraceTurn
        turns.reverse ()
        moves = []
        diagonal = 0 
        distance = 0
        pre_dist = 0
        post_dist = 0
        if Start:
            post_dist = block / 2

        while turns:
            for ( turn, seq ) in TurnSeqs:
                # print "seq, turns", seq, turns [ 0 : len ( seq ) ]
                if list ( seq ) == turns [ 0 : len ( seq ) ]:

                    # print "turns:", turns
                    if not turn [ diagonal ]:
                        print "#### direction error #1"
                        print "diagonal=%d, turn=%s" % ( diagonal, turn [ diagonal ] )
                        self.Running = False
                        self.Started = False
                        exit ()

                    if turns [ 0 ] != Turns [ 'T0' ]:
                        print "diagonal=%d, turn=%s" % ( diagonal, turn [ diagonal ] )
                        pre_dist = TurnDistance [ turn [ diagonal ] ] [ 0 ]
                        if moves:
                            moves [ -1 ] [ 1 ] = moves [ -1 ] [ 1 ] + pre_dist
                        elif Start:
                            print "#########pre_dist", pre_dist
                            moves.append ( [ 'F_T0',  post_dist+pre_dist ] )

                        post_dist = TurnDistance [ turn [ diagonal ] ] [ 1 ]

                        moves.append ( [ turn [ diagonal ], post_dist ] )

                        if turn  [ diagonal ] == 'FD_TL45' or turn  [ diagonal ] == 'FD_TR45':
                            del turns [ 0 : 1 ]
                        else:
                            del turns [ 0 : len ( seq ) ]
                        diagonal = diagonal ^ ( MouseMoves [ turn [ diagonal ] ] & 1 )

                    count = 0
                    while turns and turns [ 0 ] == Turns [ 'T0' ]:
                        del turns [ 0 ]
                        count = count + 1
                    if count or turns:
                        if not diagonal:
                            # print "Move straight:", count, block * count, post_dist
                            moves.append ( [ 'F_T0', block * count + post_dist ] )
                        else:
                            # print "Move diagonal:", count, diag * count, post_dist
                            moves.append ( [ 'FD_T0', diag * count + post_dist ] )
                    break


        if Stop_more:
            if moves [ -1 ] [ 0 ] == 'F_T0':
                moves [ -1 ] [ 0 ] = 'F_T0_STOP'
                moves [ -1 ] [ 1 ] = moves [ -1 ] [ 1 ] + block/2
            else:
                moves.append ( [ 'F_T0_STOP', post_dist + block/2 ] ) 
            moves.append ( [ 'MOVE_BACK' , 0 ] )

        else:
            if moves [ -1 ] [ 0 ] == 'F_T0':
                moves [ -1 ] [ 0 ] = 'F_T0_STOP'
                moves [ -1 ] [ 1 ] = moves [ -1 ] [ 1 ] + block/2
            else:
                ## FIXME when post_dist>block/2 ##
                moves.append ( [ 'F_T0_STOP', post_dist - block/2 ] ) 
            moves.append ( [ 'MOVE_BACK' , 0 ] )

        print "moves", moves
        #self.DrawDirsMap ()
        return moves

    def TraceRoute ( self, start, target, add_stop=False ):
        maze = self.m_Maze
        dirmap = self.DirsMap
        routes = self.TracePosition

        self.TracePosition = []
        self.TraceTurn = []
        self.TraceUnknown = []

        routes = []
        route_dirs = []
        route_turns = []
        route_unknown = []

        pos = start
        dir = dirmap [ pos ]
        
        new_target = start
        if add_stop:
            if dir == Directions [ 'NE' ] or dir == Directions [ 'SW' ]: 
                if not pos & 1:
                    ( new_target, new_dir ) = self.GetWallDir( pos, dir, Turns [ 'TR45' ] )
                    route_turns.append ( Turns [ 'TR45'] )
                else:
                    ( new_target, new_dir ) = self.GetWallDir( pos, dir, Turns [ 'TL45' ] )
                    route_turns.append ( Turns [ 'TL45'], )

            elif dir == Directions [ 'NW' ] or dir == Directions [ 'SE' ] :
                if not pos & 1:
                    ( new_target, new_dir) = self.GetWallDir( pos, dir, Turns [ 'TL45' ] )
                    route_turns.append ( Turns [ 'TL45'] )
                else:
                    ( new_target, new_dir) = self.GetWallDir( pos, dir, Turns [ 'TR45' ] )
                    route_turns.append ( Turns [ 'TR45'] )

        routes.append ( pos )
        route_dirs.append ( dir ) 

        while pos != target:
            ( npos, bdir ) = self.GetWallDir( pos, dir, Turns [ 'T180' ] )
            ndir = dirmap [ npos ]

            route_turns.append ( ( ( dir - ndir ) + 8 ) % 8 )
            routes.append ( npos )
            route_dirs.append ( ndir ) 

            if maze.GetWall ( npos ) == WALL_UNKNOWN or maze.GetWall ( npos ) == WALL_EXIST:
                route_unknown.append ( npos )

            dir = ndir
            pos = npos
        
        self.TracePosition = routes
        self.TraceTurn = route_turns 
        self.TraceUnknown = route_unknown
        return new_target

    def DoMove ( self, cmd, distance = 0, last_speed = 0, accel = 0 ):
        block = self.block

        if cmd == MouseMoves [ 'MOVE_BLOCK' ] :
            self.MoveWithAccelDistance ( 0, block )
        elif cmd == MouseMoves [ 'MOVE_HBLOCK' ] :
            self.MoveWithAccelDistance ( 0, block/2 )
        elif cmd == MouseMoves [ 'MOVE_LSTURN' ]:
            self.MoveTurn90 ( False )
        elif cmd == MouseMoves [ 'MOVE_RSTURN' ] : 
            self.MoveTurn90 ( True )
        elif cmd == MouseMoves [ 'MOVE_BACK' ] :
            self.MoveTurnInPlace ( 180, 3, False )
        elif cmd == MouseMoves [ 'MOVE_START' ] :
            self.MoveWithVelocityDistance ( 5, block/2 )
            # self.MoveWithAccelDistance ( 10, block/2 )
        elif cmd == MouseMoves [ 'MOVE_STOP' ] :
            self.MoveWithVelocityDistance  ( 0, block/2 )
            # self.MoveWithAccelDistance ( a, block * blocks  )

        # fast moves
        elif cmd == MouseMoves [ 'F_T0' ]:
            if self.vl == 0:  
                self.MoveWithAccelDistance ( 40, distance ) 
            else:
                self.MoveWithAccelDistance ( 0, distance ) 
            # self.MoveWithAccelDistance ( self.MaxAccel, distance * 1 / 2, self.MaxVelocity ) 
            # self.MoveWithVelocityDistance ( self.MaxTurnVelocity, distance * 1 / 2 ) 
        
        elif cmd == MouseMoves [ 'F_T0_STOP' ]:
            self.MoveWithVelocityDistance  ( 0, distance ) 
            # if distance > 2*block:
                # self.MoveWithAccelDistance ( self.MaxAccel, distance * 1 / 2, self.MaxVelocity ) 
                # self.MoveWithVelocityDistance ( 0, distance * 1 / 2 ) 
            # else:
                # self.MoveWithVelocityDistance ( 0, distance )
            self.mdir = ( self.mdir + Turns [ 'T180'] ) % 8

        elif cmd == MouseMoves [ 'FD_T0' ]:
            self.MoveWithAccelDistance ( 0, distance ) 
            # self.MoveWithAccelDistance ( self.MaxAccel, distance * 4 / 5, self.MaxVelocity ) 
            # self.MoveWithVelocityDistance ( self.MaxTurnVelocity, distance * 1 / 5 ) 

        elif cmd == MouseMoves [ 'F_TL45' ]:
            self.MoveTurnAccel ( 45, False )
            self.mdir = ( self.mdir + Turns [ 'TL45'] ) % 8
        elif cmd == MouseMoves [ 'F_TL90' ]:
            self.MoveTurnAccel ( 90, False )
            self.mdir = ( self.mdir + Turns [ 'TL90'] ) % 8
        elif cmd == MouseMoves [ 'F_TL135' ]:
            self.MoveTurnAccel ( 135, False )
            self.mdir = ( self.mdir + Turns [ 'TL135'] ) % 8
        elif cmd == MouseMoves [ 'F_TL180' ]:
            self.MoveTurnAccel ( 180, False )
            self.mdir = ( self.mdir + Turns [ 'T180'] ) % 8

        elif cmd == MouseMoves [ 'F_TR45' ]:
            self.MoveTurnAccel ( 45, True )
            self.mdir = ( self.mdir + Turns [ 'TR45'] ) % 8
        elif cmd == MouseMoves [ 'F_TR90' ]:
            self.MoveTurnAccel ( 90, True )
            self.mdir = ( self.mdir + Turns [ 'TR90'] ) % 8
        elif cmd == MouseMoves [ 'F_TR135' ]:
            self.MoveTurnAccel ( 135, True  )
            self.mdir = ( self.mdir + Turns [ 'TR135'] ) % 8
        elif cmd == MouseMoves [ 'F_TR180' ]:
            self.MoveTurnAccel ( 180, True )
            self.mdir = ( self.mdir + Turns [ 'T180'] ) % 8

        elif cmd == MouseMoves [ 'FD_TL45' ]:
            self.MoveTurnAccel ( 45, False )
            self.mdir = ( self.mdir + Turns [ 'TL45'] ) % 8
        elif cmd == MouseMoves [ 'FD_TL90' ]:
            self.MoveTurnAccel ( 90, False )
            self.mdir = ( self.mdir + Turns [ 'TL45'] ) % 8
        elif cmd == MouseMoves [ 'FD_TL135' ]:
            self.MoveTurnAccel ( 135, False )
            self.mdir = ( self.mdir + Turns [ 'TL135'] ) % 8

        elif cmd == MouseMoves [ 'FD_TR45' ]:
            self.MoveTurnAccel ( 45, True )
            self.mdir = ( self.mdir + Turns [ 'TR45'] ) % 8
        elif cmd == MouseMoves [ 'FD_TR90' ]:
            self.MoveTurnAccel ( 90, True )
            self.mdir = ( self.mdir + Turns [ 'TR45'] ) % 8
        elif cmd == MouseMoves [ 'FD_TR135' ]:
            self.MoveTurnAccel ( 135, True )
            self.mdir = ( self.mdir + Turns [ 'TR135'] ) % 8

    def DoMoveTurn ( self, turn ):
        add_angle = 0
        stop = False
        if turn == TSTOP:
            self.DoMove ( MouseMoves [ 'MOVE_STOP' ] )
            self.DoMove ( MouseMoves [ 'MOVE_BACK' ] )
            stop = True
            turn = Turns [ 'T180' ]

        elif turn == Turns [ 'T0'   ]:
            self.DoMove ( MouseMoves [ 'MOVE_BLOCK' ] )
        
        elif turn == Turns [ 'TL45' ]:
            self.DoMove ( MouseMoves [ 'MOVE_LSTURN' ] )
            add_angle = -1

        elif turn == Turns [ 'TR45' ]:
            self.DoMove ( MouseMoves [ 'MOVE_RSTURN' ] )
            add_angle = 1

        elif turn == Turns [ 'TL90' ]:
            print "DoMoveDir: TL90"

        elif turn == Turns [ 'TR90' ]:
            print "DoMoveDir: TR90"

        elif turn == Turns [ 'TL135']:
            self.DoMove ( MouseMoves [ 'MOVE_STOP' ] )
            self.DoMove ( MouseMoves [ 'MOVE_BACK' ] )
            self.DoMove ( MouseMoves [ 'MOVE_START' ] )
            add_angle = -1
            stop = True

        elif turn == Turns [ 'TR135']:
            self.DoMove ( MouseMoves [ 'MOVE_STOP' ] )
            self.DoMove ( MouseMoves [ 'MOVE_BACK' ] )
            self.DoMove ( MouseMoves [ 'MOVE_START' ] )
            add_angle = 1
            stop = True

        elif turn == Turns [ 'T180' ]:
            self.DoMove ( MouseMoves [ 'MOVE_STOP' ] )
            self.DoMove ( MouseMoves [ 'MOVE_BACK' ] )
            self.DoMove ( MouseMoves [ 'MOVE_START' ] )
            stop = True
        
        ( mpos, mdir ) = self.GetWallDir( self.mpos, self.mdir, turn )
        mdir = ( mdir + add_angle + 8 ) % 8
        self.mdir = mdir
        if not stop:
            self.mpos = mpos

    def RunToTarget ( self, search_unknown ):
        maze = self.m_Maze
        target =None

        self.DoMove ( MOVE_START )
        while self.mpos != target:
            self.GetCommnad ()

            self.DetectWall ()
            self.MakeDirsMap ( self.mpos, self.mdir, search_unknown )
            target = self.GetTarget ()
            # self.DrawDirsMap ()
            # self.DrawDistanceMap ()

            trace_start = target 
            trace_target = self.mpos
            self.TraceRoute ( trace_start, trace_target )
            self.DrawRoute ( 1, 0 ) 

            route_dirs = self.TraceTurn
            turn = route_dirs [ -1 ]
            self.DoMoveTurn ( turn ) 

        self.SetTarget ( target )

        self.DrawRoute ( 0, 0 ) 
        self.DetectWall ()
        self.DoMoveTurn ( TSTOP )
        
    def GetVisitPosition ( self ):
        min = WALL_MAX_DIST
        min_pos = WALL_MAX_DIST
        for pos in self.TraceUnknown:
            if self.DistanceMap [ pos ] < min:
                min = self.DistanceMap [ pos ]
                min_pos = pos
        # print "Will visit:", min_pos
        return min_pos

    def RunForSearch ( self, spos, sdir, tpos ):
        maze = self.m_Maze
        Found = False

        self.DoMove ( MOVE_START )
        while self.mpos != spos:
            self.GetCommnad ()

            self.DetectWall ()

            #====== Search shortest route
            if not Found:
                self.MakeDirsMap ( spos, sdir, True )
                # self.DrawDirsMap ()
                # self.DrawDistanceMap ()

                trace_start = tpos 
                trace_target = spos 
                self.TraceRoute ( trace_start, trace_target )
                self.DrawRoute ( 1, 1 ) 
                # print self.TracePosition

                if not self.TraceUnknown:
                    print "############### found #################"
                    Found = True

            if Found:
                search_unknown = False
            else:
                search_unknown = True

            #====== Go to unknown position 
            self.MakeDirsMap ( self.mpos, self.mdir, search_unknown )

            if Found:
                target = spos
            else:
                target = self.GetVisitPosition ()

            trace_start = target 
            trace_target = self.mpos
            self.TraceRoute ( trace_start, trace_target )
            self.DrawRoute ( 1, 0 ) 

            route_dirs = self.TraceTurn
            turn = route_dirs [ -1 ]
            self.DoMoveTurn ( turn ) 

        self.DrawRoute ( 0, 0 ) 
        self.DrawRoute ( 0, 1 ) 
        self.DoMoveTurn ( TSTOP )

    def RunFastest( self, spos, sdir, tpos, add_stop ):
        maze = self.m_Maze

        print "RunFastest###", spos, sdir, tpos
        self.MakeDirsMap ( spos, sdir, False )
        new_target = self.TraceRoute ( tpos, spos, True )
        print new_target
        turns = self.TraceTurn
        self.DrawRoute ( 1, 1 ) 

        add_start = True
        moves = self.MakeFastRoute ( add_start, add_stop )
        for move in moves:
            print move
            self.GetCommnad ()
            self.DoMove ( MouseMoves [ move [ 0 ] ], move [ 1 ], last_speed = 0, accel = 0 )
            # self.Running = False

        if add_stop:
            self.mpos = new_target
        else:
            self.mpos = tpos

    def GetCommnad ( self ):
        if self.Running:
            if self.CmdQueue.empty ():
                return True

        while True:
            cmd = self.CmdQueue.get ()
            if cmd:
                if cmd == MOUSE_CMD_STOP:
                    self.StopMouse ()
                elif cmd == MOUSE_CMD_PAUSE:
                    if self.Running:
                        self.Running = False
                    else:
                        self.Running = True
                        break
        return True
        
    def MouseMain ( self ):
        maze = self.m_Maze

        self.Walls = maze.GetAllWalls()
        self.InitRun ()
        self.InitAllTarget ()
        start = self.GetStart ()
        self.mpos = start
        self.mdir = Directions [ 'N' ]
        # self.DetectAllWalls ()

        print "############### First Running #################"
        self.RunToTarget ( True )
        time.sleep ( 1 )

        print "############### Search shortest path #################"
        self.RunForSearch ( start, 0, self.GetTarget () ) 
    
        time.sleep ( 1 )

        print "############### Second running #################"
        self.RunFastest( self.mpos, self.mdir, self.GetTarget (), True )
        time.sleep ( 1 )

        print "############### Second comming home #################"
        self.RunFastest( self.mpos, self.mdir, start, False )
        time.sleep ( 1 )

        self.Running = False
        self.Started = False

    def StopMouse ( self ):
        self.DrawRoute ( 0, 0 ) 
        self.DrawRoute ( 0, 1 ) 
        self.Running = False
        self.Started = False
        exit ()

#---------------------------------------------------------------------------
# Mouse 
#---------------------------------------------------------------------------
class Mouse(MouseBrain):
    def __init__(self, parent):
        MouseBrain.__init__ ( self, parent )

        self.m_Maze = parent
        self.Canvas = parent.Canvas

        self.Started = False
        self.Running = False
        self.CmdQueue = Queue.Queue(5)

    #-----------------------------------------------------------------------
    # Methods for draw mouse 
    #-----------------------------------------------------------------------
    def InitMouse(self):
        self.m_MousePoly = None
        self.m_MouseObject = None

    def SetMouse( self, pos, angle, block, poll, start, target, target_section, drawtime = 0.04 ):
        Canvas = self.Canvas
        self.SetEnv ( pos, angle, block, poll, start, target, target_section, drawtime = 0.04 )
        print self.pc, self.angle, start, target
        self.DrawMouse ( pos, angle, color = 'White' )

    def DrawMouse ( self, pc, angle, redraw = True, color = 'White' ):
        self.m_Maze.DrawMouse ( pc, angle, redraw, color ) 

    #-----------------------------------------------------------------------
    # Methods for AI 
    #-----------------------------------------------------------------------
    def RunPause(self, wait = False):
        if not self.Started:
            self.MouseStart ()
            self.Started = True
        else:
            self.Pause ( wait )

    def MouseStart(self):
        self.Running = True
        thread.start_new_thread ( self.MouseMain, () )

    def Pause(self, wait = False):
        run = self.IsRunning ()
        self.CmdQueue.put ( MOUSE_CMD_PAUSE )
        if wait:
            while ( run == self.IsRunning () ):
                time.sleep ( 0.01 )

    def Stop(self):
        if self.Started:
            cnt = 30
            self.CmdQueue.put ( MOUSE_CMD_STOP )
            while cnt and self.Started:
                time.sleep ( 0.1 )
                cnt = cnt - 1

    def IsRunning(self):
        return self.Running


