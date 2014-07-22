#!/usr/bin/python

import curses, curses.textpad, time, sys

maxX, maxY, height, oldheight, quit, rate, pipePos= 0, 0, 0, 0, 1, 0.04, 0

def resetVars(screen):
  global maxX, maxY, quit, pipePos
  maxY, maxX = screen.getmaxyx()
  quit = 1
  setHeight((maxY / 2) - 2)
  resetAccel()
  pipePos = maxX - 15

def initScreen(screen):
  curses.start_color()
  curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
  curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
  screen.bkgd(curses.color_pair(1))
  screen.nodelay(1)
  screen.refresh()

def scrprint(window, x, y, string):
  window.addstr(y, x, string)
  window.refresh()

def setHeight(newheight):
  global height, oldheight
  if (abs(oldheight - height) > 1): oldheight = height
  height = newheight

def setDeltaHeight(dHeight):
  global height, oldheight
  if (abs(oldheight - height) > 1): oldheight = height
  height = height + dHeight

def resetAccel():
  global rate
  rate = 0.04

def gravity():
  global rate
  rate = rate * 1.005

def movePipes():
  global pipePos
  pipePos = pipePos - 0.25
  if (pipePos < 0): pipePos = pipePos + maxX - 10

def drawBird(screen, y):
  screen.addstr(y-1, 2, " ___")
  screen.addstr(y+0, 2, "/__O\_")
  screen.addstr(y+1, 2, "\___/-'")

def drawPipes(screen, y, x):
  bottomPipe = curses.newwin(maxY - y, 10, y, x)
  bottomPipe.bkgd(curses.color_pair(2))
  screen.refresh()
  bottomPipe.refresh()

def refreshScreen(screen):
  if (abs(oldheight - height) >= 1):
    screen.clear()
    screen.box()
    drawBird(screen, int(round(height)))
    drawPipes(screen, 15, int(round(pipePos)))
    screen.refresh()

def flapFall(screen, key):
  global quit
  if (key == 32): 
    setDeltaHeight(-2)
    resetAccel()
  else: 
    setDeltaHeight(rate)
    gravity()
  if (height <= 1 or height >= (maxY - 2)): 
    while (quit != 0): quit = lose()
    resetVars(screen)

def lose():
  centerY = maxY/2
  centerX = maxX/2
  window = curses.newwin(5, 15, 10, 5)
  window.bkgd(curses.color_pair(2))
  window.box()
  window.addstr(1, 2, "YOU LOSE!")
  window.addstr(2, 2, "Try Again?")
  window.addstr(3, 2, "(Y/N)")
  key = window.getch()
  window.clear()
  if (key == 89 or key == 121): return 0
  elif (key == 78 or key == 110 or key == 113): sys.exit(0)
  else: return 1

def main(screen):
  initScreen(screen)
  resetVars(screen)
  c = 0

  while (c != 113):
    time.sleep(1/60.0)
    refreshScreen(screen)
    flapFall(screen, c)
    movePipes()
    c = screen.getch()
    
try:
  curses.wrapper(main)
except KeyboardInterrupt:
  print "Got KeyboardInterrupt exception. Exiting..."
  exit()

