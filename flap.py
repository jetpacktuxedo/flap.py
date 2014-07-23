#!/usr/bin/python

import curses, curses.textpad, time, sys

maxX, maxY, quit = 0, 0, 1

class Bird(object):
  height = 0
  oldheight = 0
  rate = 0.04
  xPos = 1
  screen = None

  def __init__(self, screen, height, xPos):
    self.screen = screen
    self.height = height
    self.xPos = xPos

  def setHeight(self, newheight):
    if (abs(self.oldheight - self.height) > 1): self.oldheight = self.height
    self.height = newheight

  def setDeltaHeight(self, dHeight):
    if (abs(self.oldheight - self.height) > 1): self.oldheight = self.height
    self.height += dHeight

  def resetAccel(self):
    self.rate = 0.04

  def gravity(self):
    self.rate *= 1.005

  def draw(self):
    self.screen.addstr(int(round(self.height-1)), int(round(self.xPos)), " ___   ")
    self.screen.addstr(int(round(self.height+0)), int(round(self.xPos)), "/__O\_ ")
    self.screen.addstr(int(round(self.height+1)), int(round(self.xPos)), "\___/-'")

  #Returns true if there is a collision
  def flapFall(self, key):
    global quit
    if (key == 32): 
      self.setDeltaHeight(-2)
      self.resetAccel()
    else: 
      self.setDeltaHeight(self.rate)
      self.gravity()
    if (self.height <= 1 or self.height >= (maxY - 2)): return True
    else: return False

  def moved(self):
    if (abs(self.oldheight - self.height) >= 1): return True
    else: return False

class Pipe(object):
  height = 0
  dist = 0
  thickness = 10

  def __init__(self, height, dist, thickness):
    self.height = height
    self.dist = dist
    self.thickness = thickness

  def advance(self):
    if (self.dist <= 0.25 and self.thickness > 1): 
      self.thickness = self.thickness - 0.25
      self.dist = 0.25
    elif (self.dist <= 0.25 and self.thickness <= 1):
      self.thickness = 0
      self.dist = 0
    else: self.dist = self.dist - 0.25

  def draw(self, screen):
    if (self.thickness == 0): return
    bottomPipe = curses.newwin(maxY - self.height, int(round(self.thickness)), 
            self.height, int(round(self.dist)))
    bottomPipe.bkgd(curses.color_pair(2))
    screen.refresh()
    bottomPipe.refresh()

  def wholePos(self):
    if (self.dist % 1.0 == 0): return True
    else: return False

  def collision(self, birdMinX, birdMaxX, birdMinY, birdMaxY):
    pipeMinX = dist
    pipeMaxX = dist + thickness
    pipeMinY = height
    pipeMaxY = maxY - height
    for x in range(birdMinX, birdMaxX):
      for y in range(birdMinY, birdMaxY):
        if (x in range(pipeMinX, pipeMaxX) and y in range(pipeMinY, pipeMaxY)):
          return True
    return False

def checkPipesForWhole(pipeList):
  for i in pipeList:
    if i.wholePos(): return True
  return False

def checkCollisions(pipeList, birdMinX, birdMaxX, birdMinY, birdMaxY):
  for i in pipeList:
    if i.collision(birdMinX, birdMaxX, birdMinY, birdMaxY): return True
  return False

def resetVars(screen, bird):
  global maxX, maxY, quit, pipePos
  maxY, maxX = screen.getmaxyx()
  quit = 1
  bird.setHeight((maxY / 2) - 2)
  bird.resetAccel()
  pipePos = maxX - 15

def initScreen(screen):
  curses.start_color()
  curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
  curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
  screen.bkgd(curses.color_pair(1))
  screen.nodelay(1)
  screen.refresh()

def refreshScreen(screen, bird, pipeList):
  if (bird.moved() or checkPipesForWhole(pipeList)):
    screen.clear()
    screen.box()
    bird.draw()
    for i in pipeList: i.draw(screen)
    screen.refresh()

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
  global quit
  initScreen(screen)
  bird = Bird(screen, (maxY / 2) - 2, 2)
  resetVars(screen, bird)
  c = 0
  pipeList = []
  pipeList.append(Pipe(15, maxX - 10, 10))
  pipeList.append(Pipe(10, maxX - 25, 10))

  while (c != 113):
    time.sleep(1/60.0)
    for i in pipeList: i.advance()
    refreshScreen(screen, bird, pipeList)

    if bird.flapFall(c):
      while (quit != 0): quit = lose()
      resetVars(screen, bird)
    c = screen.getch()
    
try:
  curses.wrapper(main)
except KeyboardInterrupt:
  print "Got KeyboardInterrupt exception. Exiting..."
  exit()

