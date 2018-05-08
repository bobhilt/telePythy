# telePythy
### A Python implementation of the board game, Telepathy. 
### Implemented by Bob Hiltner as a study in implementing player vs. computer logic and rendering of game play.

### Rules

* Players (or game in player v computer) select a secret square. Players alternate inquiries to zero in on secret square. 

First to correctly solve their opponent's secret square wins. Incorrect attempt to solve result in a loss.

Guessing player offers a single square as (Row, Column, Color, Shape), e..g, "B2 Green Heart.""

Response is either "Yes" (some attribute (row, column, color or shape) of the guess matches at least one of the secret square's attributes, or "No" (none of the attributes match).

Player has one opportunity to choose "solve" and provide their final conclusion.


### Implementation: 
With each guess, game tracks eliminated or potentially included cells. Building game logic before working on rendering and presentation.

Ultimately, game will show cells graphically, with optional highlighting of eliminated cells. Hints may be provided, and should be web app.

### Next:
Complete guess logic

* Track all guesses
* Set cell statuses with each guess
* Provide verbose feedback, e.g., Your guess eliminated n cells, with m remaining.
* Provide list of eliminated cells.
* Provide view by row, column, color, shape, shape + color of eliminated or included cells, with counts.