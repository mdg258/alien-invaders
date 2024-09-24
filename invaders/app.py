
# ERRORS

# Level Change: Score drop




# IT NOW ADDS HEARTS BUT IT NEEDS TO RESTRICT HOW MUCH IT WILL ADD
# HEARTS SHOULD NOT POPULATE IF THERE ARE X AMOUNT OF HEARTS ALREADY
# IT ALSO NEEDS TO ADD TO PLAYER LIVES WHEN THERE IS A HEART ADDED





################################################################################



"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

Authors:  Aryaman Thareja (aat53)      |   Michael Glenn (mdg258)
Date:     December 9, 2021
"""
from consts import *
from game2d import *
from wave import *
import time
import os

# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py
class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message: Title, Won, Over
    # Invariant: _text is a GLabel object.
    #
    # Attribute _start: the currently active message: Play Game
    # Invariant: _start is a GLabel object.
    #
    # Attribute _press: the currently active message: Continue or Play Again
    # Invariant: _press is a GLabel object.
    #
    # Attribute _lives: the currently active message: Player Lives
    # Invariant: _lives is a GLabel object.
    #
    # Attribute _score: the currently active message: Player Score
    # Invariant: _score is a GLabel object.
    #
    # Attribute _points: the currently active message: Player Score
    # Invariant: _points is a GLabel object.
    #
    # Attribute _pause: the currently active message: Pause Game
    # Invariant: _pause is a GLabel object.
    #
    # Attribute _fire: the currently active message: Fire Bolt
    # Invariant: _fire is a GLabel object.
    #
    # Attribute _background: the background color
    # Invariant: _background is a GRectangle object.
    #
    # Attribute _lastkeys: the keys press last frame.
    # Invariant: _lastkeys is an int.
    #
    # Attribute _currentkeys: the keys pressed this frame.
    # Invariant: _currentkeys is an int.

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        # Game Music
        self.startupMusic = Sound('start.wav')
        self.startupMusic.volume = 0.23
        self.startupMusic.play()
        self.gameMusic = Sound('game.wav')
        self.gameMusic.volume = 0.23
        # HIDDEN ATTRIBUTES
        self._state = STATE_INACTIVE
        self._wave = None
        self._lastkeys = 0
        self._currentkeys = 0
        # HIDDEN ATTRIBUTES  -  GLabel Objects
        self._background = GRectangle(fillcolor=BLACK_COLOR, width=GAME_WIDTH,
        height=GAME_HEIGHT, x=GAME_WIDTH/2, y=GAME_HEIGHT/2)
        self._text = GLabel(x=GAME_WIDTH/2, y=(GAME_HEIGHT/2)+23, font_size=60,
        text="ALIEN  INVADERS", font_name='RetroGame.ttf', linecolor=LIME)
        self._press = GLabel(x=GAME_WIDTH/2, y=GAME_HEIGHT/3, font_size=20,
        text="Press 'S' to Play", font_name='RetroGame.ttf', linecolor=GREY)
        self._start = GLabel(x=GAME_WIDTH/2, y=GAME_HEIGHT/2, font_size=60,
        text="Press 'S' to Play", font_name='Arcade.ttf', linecolor=WHITE_COLOR)
        self._lives = None
        self._level = GLabel(x=GAME_WIDTH/2, y=GAME_HEIGHT-(ALIEN_CEILING/4),
        font_size=27, text='', font_name='Arcade.ttf', linecolor=YELLOW_COLOR)
        self._points = GLabel(x=GAME_WIDTH/2, y=GAME_HEIGHT-(ALIEN_CEILING/4)-27,
        font_size=27, text='', font_name='RetroGame.ttf', linecolor=WHITE_COLOR)
        self._p = GLabel(x=GAME_WIDTH-124, y=self._level.y, font_size=15,
        text="PAUSE:      P",font_name='RetroGame.ttf', linecolor=GREY)
        self._space = GLabel(x=GAME_WIDTH-100, y=self._p.y-20, font_size=15,
        text="FIRE:        SPACE", font_name='RetroGame.ttf', linecolor=GREY)
        self._levelNum = 1
        self._score = 0


    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        #print('Score in App Line 217    '+str(self._score))
        # Determine Game State
        self._determineState()
        # Play Game Music
        if self._state == STATE_INACTIVE:
            self.gameMusic.play(loop=True)
        # Get Wave objects and set state to active
        if self._state == STATE_NEWWAVE:
            self._wave = self._getWave()
            if self._levelNum > 1:
                self._updateWave()
            self._state = STATE_ACTIVE
        # Update Wave object and get Player Score/Lives
        if self._state == STATE_ACTIVE:
            self._wave.update(self.input, dt)
            self._level.text = self._getLevel()
            self._points.text = self._getScore()
            self._lives = self._getLives()
        # Update _press text and Player Score/Lives
        if self._state == STATE_PAUSED:
            self._text.text = "ALIEN  INVADERS"
            self._press.text = "Press 'S' to Continue"
            self._lives = self._getLives()
            self._points.text = self._getScore()
            self._level.text = self._getLevel()
        # Update Wave Objects and set state to active
        if self._state == STATE_CONTINUE:
            self._wave.update(self.input, dt)
            self._updateWave()
            self._continueGame()
            self._state = STATE_ACTIVE
        # Update _text and Play Again
        if self._state == STATE_COMPLETE:
            self._level.text = self._getLevel()
            if self._isGameOver():
                self._text.text = "GAME OVER"
                self._text.linecolor = RED_COLOR
            elif self._isLevelWon():
                self._text.text = "LEVEL COMPLETE"
                self._text.linecolor = LIME
            self._press.text = "Play Again?   [Y/N]"


    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        # Draw Background and Game Play Instructions
        self._background.draw(self.view)
        self._p.draw(self.view)
        self._space.draw(self.view)
        # Draw Title and Play Game
        if self._state == STATE_INACTIVE:
            self._text.draw(self.view)
            self._press.draw(self.view)
        # Draw Title, Lives, Score, and Continue Game
        elif self._state == STATE_PAUSED:
            self._makeHearts()
            #self._lives.draw(self.view)
            self._level.draw(self.view)
            self._points.draw(self.view)
            self._press.draw(self.view)
            self._text.draw(self.view)
        # Draw Game Over / Game Won and Play Again
        elif self._state == STATE_COMPLETE:
            if self._isLevelWon():
                self._makeHearts()
            self._updateWave()
            self._level.draw(self.view)
            self._points.draw(self.view)
            self._press.draw(self.view)
            self._text.draw(self.view)
        # Draw Score, Lives, and Wave
        elif self._state == STATE_ACTIVE:
            self._makeHearts()
            self._points.draw(self.view)
            self._wave.draw(self.view)
            self._level.draw(self.view)


    # HELPER METHODS FOR THE STATES GO HERE
    def _determineState(self):
        """
        Determines the current state and assigns it to self._state

        This method checks for a key press, and if there is one, changes the state
        to the next value.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.  The
        user must release the key and press it again to change the state.
        (specification from Samples provided)
        """
        # Determine the current number of keys pressed
        # Only change if we have just pressed the keys this animation frame
        self._currentkeys = self.input.key_count
        # Play or Continue Game
        change = (self._currentkeys > 0 and self._lastkeys == 0
        and self.input.is_key_down('s'))
        # Restart Game
        restart = (self._currentkeys > 0 and self._lastkeys == 0
        and self.input.is_key_down('y'))
        # Exit Game
        leave = (self._currentkeys > 0 and self._lastkeys == 0
        and self.input.is_key_down('n'))
        # Pause Game
        pause = (self._currentkeys > 0 and self._lastkeys == 0
        and self.input.is_key_down('p'))
        # STATE_INACTIVE
        if change and self._state == STATE_INACTIVE:
            # Click happened.  Change the state
            self._state = STATE_NEWWAVE
            # Update last_keys
            self._lastkeys = self._currentkeys
        # STATE_ACTIVE
        if self._state == STATE_ACTIVE:
            self._score = self._wave._playerScore
            if self._isGameOver() or self._isLevelWon():
                if self._isLevelWon():
                    print('Level Won')
                    print('Hearts:  '+str(3-self._wave._hearts.count(None)))
                    self._levelNum += 1
                # Game done. Change the state
                self._state = STATE_COMPLETE
        if pause and self._state == STATE_ACTIVE:
            # Click happened.  Change the state
            self._state = STATE_PAUSED
            # Update last_keys
            self._lastkeys = self._currentkeys
        if self._state == STATE_ACTIVE and self._isPaused():
            # Game Paused. Change the state.
            self._state = STATE_PAUSED
        # STATE_PAUSED
        if change and self._state == STATE_PAUSED:
            # Click happened.  Change the state
            self._state = STATE_CONTINUE
            # Update last_keys
            self._lastkeys = self._currentkeys
        # STATE_COMPLETE
        if self._state == STATE_COMPLETE:
            # Click happend. Update and play again
            self._updateWave()
            if restart:
                if self._isLevelWon():
                    self._score = self._wave._playerScore
                    self._state = STATE_NEWWAVE
                    self._lastkeys = self._currentkeys
                elif self._isGameOver():
                    os.execl(sys.executable, sys.executable, *sys.argv)
            elif leave:
                # Click happened. Exit program
                sys.exit()
        #reset last keys
        self._lastkeys = 0


    # GETTERS FOR ACCESSING WAVE

    def _getWave(self):
        """
        Returns Wave objects.
        """
        return Wave()

    # Player Lives
    def _getLives(self):
        """
        Returns player lives and changes display color.

        Starts off green if player has 3 lives.
        Switches to yellow when player loses a life.
        Switches to red when player has 1 life left.
        """
        return self._wave._hearts

    def _makeHearts(self):
        """
        Makes heart icons for lives.
        """
        # drawing hearts
        for img in self._wave._hearts:
            if img is not None:
                img.draw(self.view)

    # Player Score
    def _getScore(self):
        """
        Returns players score. Score increments += 10 for every alien killed.
        """
        return str(self._wave._playerScore)

    # Current Level
    def _getLevel(self):
        """
        Returns the current game level.
        """
        return str(self._wave._level)

    # Pause Game
    def _isPaused(self):
        """
        Returns whether ship has been destroyed to pause game.
        """
        return self._wave._shipSprite is None and self._wave._ship is None

    # Game Over
    def _isGameOver(self):
        """
        Returns if game is over by accessing _gameOver() in wave.
        """
        return self._wave._gameOver()

    # Game Complete
    def _isLevelWon(self):
        """
        Returns if game has been won by accessing _winner() in wave.
        """
        return self._wave._winner()

    # Resume Playing
    def _continueGame(self):
        """
        Returns if game should continue by accessing _resumeGame() in wave.
        """
        return self._wave._resumeGame()

    def _updateWave(self):
        """
        SPEC
        """
        self._wave._level = self._levelNum
        self._wave._playerScore = self._score
        self._wave._hearts = self._lives
        self._wave._lives = len(self._wave._hearts)
        self._wave._alienhelper()
