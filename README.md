# NFL Game Charting (mini-project)

Given two game charts from one team per game only, a chart of a team's use of a specific formation for half the season, and a chart show all of a specific QB's passes for half a season, what "football-relative" concepts can we elucidate?  While certain conclusions would be spurious due to having such limited data, trends within these small data subsets can still be discovered and reported.  The point of this mini-project is to show that a data-focused analysis could indeed be an effective tool in revealing aspects to a game, a team, or a player that went previously unnoticed.


## Table of Contents
1. [Successful and Explosive Plays](#successful-and-explosive-plays)



<BR><BR>

### Successful and Explosive Plays
##### Successful Plays
In modern football parlance, a _successful_ play can be considered one to gain a certain number of required yards given the down and distance situation.  Since there is no single set of yardage percentage weightings that is agreed upon, I have chosen to use the following cutoffs that were originally reported by Pete Palmer, Bob Carroll, and John Thorn in _The Hidden Game of Football_ and have subsequently been the basis for Football Outsiders' [DVOA metric](http://www.footballoutsiders.com/info/methods#DVOA).

A play is a success if it gains the following percent of yards required for a first down on the given down:
+ 1st Down: 45%
+ 2nd Down: 60%
+ 3rd & 4th Down: 100%


##### Explosive Plays
Again, definitions will vary on this categorization.  For this mini-project I had to choose my own cutoffs.  If an entire database of all plays in a season (or many seasons) was processed, we could likely arrive at a certain distance for each type of play, pass and rush, which would statistically be of a certain rarity as to count for "explosiveness."  That aside, I chose what I felt were reasonable distances for "explosiveness" for each play.

+ Pass: 16+ yards
+ Rush: 12+ yards

Barring extreme and rare circumstances, this means that explosive plays will almost always be "successful" plays as well, but the reverse is not true.












For each:
situations, directions, margin, packages, shotgun/I-Form, motion, target dir, target align, rushers, yard line, what plays did they follow? follow penalties?

1. explosive / success plays
2. TD plays — same info
3. Sacks — same info
4. Packages — most common and in what situations, most successful, least successful, team character (6 OL v 3x1),
5. Does shotgun = better passing?  Worse rushing? What about I-Form?
6. Would certain QBs do better throwing to one side of the field?
7. Do explosive plays come earlier or later in game?  Any correlation?  Do they happen more with certain players?
8. Did Sacks kill drives?
9. How did penalties affect drives?
