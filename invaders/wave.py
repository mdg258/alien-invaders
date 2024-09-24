"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Authors:  Aryaman Thareja (aat53)      |   Michael Glenn (mdg258)
Date:     December 9, 2021
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class are to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # Attribute _alienShoot: the amount of time before aliens shoot next
    # Invariant: _alienShoot is a int >= 1
    #
    # Attribute _alienSteps: the amount of alien steps taken since shooting
    # Invariant: _alienSteps is an int >= 0
    #
    # Attribute _alienPos: the x-axis position the aliens are moving
    # Invariant: _alienPos is an int in [-1, 1]
    #
    # Attribute _hitEdge: if aliens have hit a screen edge this step
    # Invariant: _hitEdge is a boolean
    #
    # Attribute _shipDeath: if ship has been destroyed
    # Invariant: _shipDeath is a boolean
    #
    # Attribute _shipSprite: the ship sprite to animate ship death
    # Invariant: _shipSprite is a GSprite object or None
    #
    # Attribute _paused: if game should be paused
    # Invariant: _paused is a boolean
    #
    # Attribute _shipAnimationTime: the amount of time this animation frame
    # Invariant: _shipAnimationTime is an int or float >= 0
    #
    # Attribute _animateShip: if ship should be animated
    # Invariant: _animateShip is _makeShipAnimator() or None
    #
    # Attribute _aliensAlive: the amount of aliens still alive
    # Invariant: _aliensAlive is an int >= 0
    #
    # Attribute _playerScore: the player score incremented by += 10
    # Invariant: _playerScore is an int >= 0


    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the wave object.
        """
        # GAME SOUND EFFECTS
        self.shipBlast = Sound('pew1.wav')
        self.shipBlast.volume = 0.50
        self.alienBlast = Sound('pew2.wav')
        self.destroyedShip = Sound('blast1.wav')
        self.destroyedAlien = Sound('pop2.wav')
        self.playerDead = Sound('dead.wav')
        self.lastAlien = Sound('last-alien.wav')
        self.winnerSound = Sound('last-alien.wav')
        # HIDDEN ATTRIBUTES
        self._ship = Ship(GAME_WIDTH/2,SHIP_BOTTOM+(SHIP_HEIGHT/2),SHIP_IMAGE)
        self._aliens = self._alienhelper()
        self._hearts = self._hearthelper()
        self._bolts = []
        self._dline = GPath(points=LINE_POINTS, linecolor=WHITE_COLOR)
        self._tline = GPath(points=TOP_LINE_POINTS, linecolor=GREY)
        self._barriers = self._barriersHelper()
        self._lives = 3
        self._time = 0
        self._alienShoot = random.randint(1, BOLT_RATE)
        self._alienSteps = 0
        self._alienPos = 1
        self._hitEdge = False
        self._shipDeath = False
        self._shipSprite = None
        self._paused = False
        self._shipAnimationTime = 0
        self._animateShip = None
        self._aliensAlive = ALIEN_ROWS*ALIENS_IN_ROW
        self._playerScore = 0
        self._level = 1
        self._extraHeart = None
        self._invincible = False

    def update(self,input,dt):
        """
        Updates the game objects each frame.

        Parameter input: The player key stroke.
        Parameter dt: The number of seconds since the last animation frame.
        """
        # print('Lives:   '+str(self._lives))
        #print('Line 151 in Wave: Score      '+str(self._playerScore))
        if not self._paused:
            addSpeed = (self._level * 0.05)
            if addSpeed >= 1:
                addSpeed = 0.95
            speed = ALIEN_SPEED - addSpeed
            print(speed)
            # moving the ship
            self._moveShip(input)
            # moving the aliens
            self._time += dt
            edge = GAME_WIDTH-(ALIEN_H_SEP+ALIEN_WIDTH)
            if self._time > speed:
                self._moveAlien()
                self._alienSteps += 1
                self._time = 0
            # moving the bolt
            self._fireBolt(input)
            self._collides()
        elif self._paused:
            # animating ship death
            if self._animateShip is not None:
                self._runShipAnimator(dt)
            try:
                self._animateShip = self._makeShipAnimator()
                next(self._animateShip)
            except:
                self._animateShip = None

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the wave objects to the view.

        Parameter view: The viewing screen inherited from app.
        """
        try:
            img = [HEART_PNG, POTION]
            i = random.randint(0,1)
            x = random.randint(0, ALIEN_ROWS)
            y = random.randint(0, ALIENS_IN_ROW)
            if self._level >= 1:
                amt = 0
                for row in self._aliens:
                    for alien in row:
                        if alien.source == HEART_PNG or alien.source == POTION:
                            amt += 1
                if amt == 0:
                    self._aliens[x][y].source = img[i]
                    if img[i] == POTION:
                        self._aliens[x][y].width = 44
                        self._aliens[x][y].height = 44
        except:
            pass
        # drawing aliens
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.draw(view)
        # drawing ship
        try:
            if self._shipSprite == None:
                self._ship.draw(view)
            if self._ship == None:
                self._shipSprite.draw(view)
        except:
            pass
        if self._extraHeart is not None:
            self._extraHeart.draw(view)
        # drawing defense line
        self._dline.draw(view)
        # drawing top line
        self._tline.draw(view)
        # drawing bolt(s)
        for bolt in self._bolts:
            if bolt is not None:
                bolt.draw(view)

    # HELPER METHODS FOR ALIENS, SHIP, BOLT, & COLLISIONS

            ##########       ALIENS        ##########

    # HELPERS TO CREATE AND CHOOSE ALIENS
    def _alienhelper(self):
        """
        Draws ALIEN_ROWS rows of aliens with ALIENS_IN_ROW many aliens
        in each row.
        """
        # create empty list
        allAliens = []
        # create x and y coordinates
        x = ALIEN_H_SEP + ALIEN_WIDTH
        y = GAME_HEIGHT - ALIEN_CEILING - (ALIEN_HEIGHT/2)
        # create rows
        for i in range(1, ALIEN_ROWS+1):
            row = []
            # create aliens
            for j in range(1, ALIENS_IN_ROW+1):
                if i == 1:
                    row.append(Alien(x*j, y, ALIEN_IMAGES[2]))
                elif i == 2 or i == 3:
                    row.append(Alien(x*j, y, ALIEN_IMAGES[1]))
                else:
                    row.append(Alien(x*j, y, ALIEN_IMAGES[0]))
            # set y coordinate for new row
            y -= (ALIEN_V_SEP + ALIEN_HEIGHT)
            # append row to create 2D list
            allAliens.append(row)
        # return alines
        return allAliens


    def _hearthelper(self):
        """
        Draw 3 Hearts to display player lives.
        """
        # create empty list
        allHearts = []

        x = 36
        y = (GAME_HEIGHT - (ALIEN_CEILING/4)) - 15

        for i in range(1,4):
            allHearts.append(Heart(x, y, HEART_PNG))
            x += 38
        return allHearts

    def _barriersHelper(self):
        """
        Draws 3 barriers to safeguard the ship.
        """
        b1 = GPath(points=[0, 100,160,100], linecolor=WHITE_COLOR, linewidth=2)
        b2 = GPath(points=[320, 100,480,100], linecolor=WHITE_COLOR, linewidth=2)
        b3 = GPath(points=[640, 100,800,100], linecolor=WHITE_COLOR, linewidth=2)
        barriers = [b1,b2,b3]
        return barriers


    def _pickalien(self):
        """
        Chooses an alien, at random, to shoot the next bolt.
        The alien is then passed to the _alienBolt helper.

        Chosen aliens are the lowest alien in their column.
        Alien must not be None.
        """
        # create columns
        column = random.randint(0, ALIENS_IN_ROW-1)
        # create row
        row = ALIEN_ROWS - 1
        # choose alien
        while row >= 0:
            if self._aliens[row][column] is not None:
                return self._aliens[row][column]
            row -= 1

    # HELPERS TO MOVE ALIENS: LEFT, RIGHT, & DOWN
    def _moveAlien(self):
        """
        Controls helper functions to move aliens.
        Aliens either move left, right, or down.
        """
        # create left and right margins
        right_edge = GAME_WIDTH-(ALIEN_H_SEP+ALIEN_WIDTH)
        left_edge = ALIEN_H_SEP+ALIEN_WIDTH
        # continue moving if not at margin using helpers
        if self._hitEdge == False:
            if self._alienPos == 1:
                self._alienRight()
            if self._alienPos == -1:
                self._alienLeft()
            # determine if at margin
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        if alien.x >= right_edge or alien.x <= left_edge:
                            self._hitEdge = True
        elif self._hitEdge == True:
            # move down once using helper
            self._alienDown()
            # change direction; continue moving
            self._alienPos *= -1
            # no longer at margin
            self._hitEdge = False

    def _alienLeft(self):
        """
        Moves the aliens to the left.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.x -= ALIEN_H_WALK

    def _alienRight(self):
        """
        Moves the aliens to the right.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.x += ALIEN_H_WALK

    def _alienDown(self):
        """
        Moves the aliens down.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.y -= ALIEN_V_WALK

            ##########        SHIP         ##########

    # HELPER TO MOVE SHIP
    def _moveShip(self, input):
        """
        Moves the ship using the 'left' and 'right' arrow keys.
        Ship stays on screen within a margin of SHIP_WIDTH.

        Parameter input: The player key stroke.
        """
        if input.is_key_down('left') and self._ship.x > SHIP_WIDTH:
            self._ship.x -= SHIP_MOVEMENT
        if input.is_key_down('right') and self._ship.x < GAME_WIDTH-SHIP_WIDTH:
            self._ship.x += SHIP_MOVEMENT

            ##########        BOLTS        ##########

    # HELPER TO FIRE AND DELETE BOLT
    def _fireBolt(self, input):
        """
        Fires and deletes both alien and player bolts.
        Bolts are deleted if collision occurs or bolt goes off screen.

        Parameter input: The player key stroke.
        """
        # helpers for bolt objects
        self._playerBolt(input)
        self._alienBolt()
        for bolt in self._bolts:
            # PLAYER BOLT
            if bolt.player:
                bolt.y += bolt._velocity
                # remove bolt
                if bolt.y >= 612:
                    self._bolts.remove(bolt)
            # ALIEN BOLT
            if not bolt.player:
                bolt.y += (bolt._velocity+2)
                # remove bolt
                if bolt.y < 0:
                    self._bolts.remove(bolt)

    # HELPER TO CREATE PLAYER BOLTS
    def _playerBolt(self, input):
        """
        Creates a player bolt if there is no active player bolt on screen.
        Player bolt is created with the 'spacebar' key.

        Parameter input: The player key stroke.
        """
        if self._shipDeath == False:
            # create y coordinate for player bolt
            SHIP_NOSE = self._ship.y+(SHIP_HEIGHT/2)
            # create player bolt
            if input.is_key_down('spacebar') and self._playerBoltInactive():
                # play sound effect
                self.shipBlast.play()
                bolt = Bolt(x=self._ship.x, y=SHIP_NOSE, player=True)
                self._bolts.append(bolt)

    # HELPER TO DETERMINE IF PLAYER HAS ACTIVE BOLT
    def _playerBoltInactive(self):
        """
        Detects if there is already an active player bolt on screen.
        """
        if len(self._bolts) == 0:
            return True
        else:
            for bolt in self._bolts:
                if bolt.player:
                    return False
        return True

    # HELPER TO CREATE ALIEN BOLTS
    def _alienBolt(self):
        """
        Creates an alien bolt using the _pickalien helper.
        """
        if self._alienSteps == self._alienShoot:
            # choose random alien using helper
            alien = self._pickalien()
            while alien is None or alien.source == HEART_PNG or alien.source == POTION:
                alien = self._pickalien()
            # create y coordinate for alien bolt
            ALIEN_BASE = alien.y-(ALIEN_HEIGHT/2)
            # create bolt
            self.alienBlast.play()
            bolt = Bolt(x=alien.x, y=ALIEN_BASE, player=False)
            self._bolts.append(bolt)
            # create new interval for aliens to shoot
            self._alienShoot = random.randint(1, BOLT_RATE)
            # reset alien steps
            self._alienSteps = 0

            ##########     COLLISIONS     ##########

    # HELPERS TO IDENTIFY BOLT COLLISIONS
    def _collides(self):
        """
        Detects whether there has been a bolt collision.
        Bolts can collide with the ship or aliens.
        """
        # helpers for bolt collisions
        self._collideShip()
        self._collideAlien()


    def _collideShip(self):
        """
        Detects if an alien bolt has collided with the ship.

        If collision has occured:
                The bolt is destroyed.
                The ship is destroyed and set to None.
        """
        # determine if collision has occured
        for bolt in self._bolts:
            if not bolt.player:
                # determine ship corners
                c1 = (bolt.x-(BOLT_WIDTH/2),bolt.y-(BOLT_HEIGHT/2))
                c2 = (bolt.x+(BOLT_WIDTH/2),bolt.y-(BOLT_HEIGHT/2))
                if self._ship.contains(c1) or self._ship.contains(c2):
                    # remove bolt and kill ship
                    self._bolts.remove(bolt)
                    if not self._invincible:
                        self._shipDeath = True
        # collision occured
        if self._shipDeath:
            self.destroyedShip.play()
            del self._hearts[-1]
            self._lives -= 1
            # play sound effect
            if self._lives == 0:
                self.playerDead.play()
            # pause game
            self._paused = True
            # create ship sprite for ship animation
            self._shipSprite = GSprite(source=SHIP_SPRITE, x=self._ship.x,
            y=self._ship.y, width=self._ship.width, height=self._ship.height,
            format=(2,4))
            # remove ship object
            self._ship = None

    def _collideAlien(self):
        """
        Detects if a player bolt has collided with an alien.

        If collision has occured:
                The bolt is destroyed.
                The alien is set to None.
        """
        # determine if collision has occured
        for bolt in self._bolts:
            if bolt.player:
                # determine ship corners
                c1 = (bolt.x-(BOLT_WIDTH/2),bolt.y+(BOLT_HEIGHT/2))
                c2 = (bolt.x+(BOLT_WIDTH/2),bolt.y+(BOLT_HEIGHT/2))
                for row in self._aliens:
                    for alien in row:
                        if alien is not None:
                            if alien.contains(c1) or alien.contains(c2):
                                # play sound effect
                                if self._aliensAlive == 1:
                                    self.lastAlien.play()
                                if alien.source == HEART_PNG:
                                    x_pos = (len(self._hearts) *38) + 36
                                    y = (GAME_HEIGHT - (ALIEN_CEILING/4)) - 15
                                    self._hearts.append(Heart(x_pos, y, HEART_PNG))
                                    self._lives += 1
                                    self.lastAlien.play()
                                if alien.source == POTION:
                                    self.lastAlien.play()
                                    self._ship.width = 27
                                    self._ship.height = 27
                                else:
                                    self.destroyedAlien.play()

                                # locate alien in 2D list
                                r = self._aliens.index(row)
                                a = self._aliens[r].index(alien)
                                # remove alien and bolt
                                self._aliens[r][a] = None
                                self._bolts.remove(bolt)
                                # update aliens alive and player score
                                self._aliensAlive -= 1
                                if r == 0:
                                    self._playerScore += 30
                                if r == 1 or r == 2:
                                    self._playerScore += 20
                                if r == 3 or r == 4:
                                    self._playerScore += 10

    def _makeShipAnimator(self):
        """
        The animation coroutine for the ship.
        """
        # collision occured
        if self._paused and self._shipDeath:
            for bolt in self._bolts:
                # remove bolt
                self._bolts.remove(bolt)
            # animate ship death
            while self._shipAnimationTime < DEATH_SPEED:
                dt = (yield)
                self._shipAnimationTime += dt
                step = self._shipAnimationTime/DEATH_SPEED
                amount = step*8
                self._shipSprite.frame = int(amount)
            # remove ship sprite
            if self._shipAnimationTime >= DEATH_SPEED:
                self._shipSprite = None
            # update player lives and reset ship animation time
            self._shipDeath = False
            self._shipAnimationTime = 0

    def _runShipAnimator(self,dt):
        """
        The driver for the ship's animation coroutine.

        Parameter dt: The number of seconds since the last animation frame
        Precondition: dt is an number >= 0
        """
        # send dt to ship animator or set to None
        try:
            self._animateShip.send(dt)
        except:
            self._animateShip = None

    def _gameOver(self):
        """
        Determines if the game is over.
        Returns True if game is over. False otherwise.

        The game is over if aliens brech defense line
        or the player has lost all lives.
        """
        # determine if aliens crossed defense line; return True
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    if (alien.y - (ALIEN_HEIGHT/2)) <= DEFENSE_LINE:
                        return True
        # determine if player has lost all lives; return True
        if self._lives == 0:
            return True
        # game is not over; return False
        return False

    def _winner(self):
        """
        Determines if player won the game.
        Returns True if player has killed all aliens.

        Player wins if all aliens have been killed.
        """
        # all aliens killed; return True
        if self._aliensAlive == 0:
            return True
        # aliens still alive; return False
        return False

    def _resumeGame(self):
        """
        Resumes game and recreates the ship.
        """
        # create ship and unpause game
        self._ship = Ship(GAME_WIDTH/2, SHIP_BOTTOM+(SHIP_HEIGHT/2), SHIP_IMAGE)
        self._paused = False
