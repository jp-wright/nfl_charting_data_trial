# NFL Game Charting (mini-project)

Given two game charts from one team per game only, a chart of a team's use of a specific formation for half the season, and a chart show all of a specific QB's passes for half a season, what "football-relative" concepts can we elucidate?  While certain conclusions would be spurious due to having such limited data, trends within these small data subsets can still be discovered and reported.  The point of this mini-project is to show that a data-focused analysis could indeed be an effective tool in revealing aspects to a game, a team, or a player that went previously unnoticed.


## Table of Contents
1. [Dataset](#dataset)
2. [Successful and Explosive Plays](#successful-and-explosive-plays)



<BR><BR>

### Dataset
There were four charts (CSV files), all from the 2016 season.  The play-by-play charts each had only one team from the game.

1. Green Bay's play-by-play chart from Chicago @ Green Bay in Week 7.
2. Oakland's play-by-play chart from Denver @ Oakland in Week 9.
3. Seattle's uses of the _3x1_ formation in the first eight weeks of the season.
4. All of Matthew Stafford's pass attempts from the first eight weeks of the season.

I combined the two play-by-play charts to have a larger sample size for some analysis.  If all play-by-play charts for both teams in all games were available, we could combine them all and have a representative dataset for the 2016 season.  This would allow us to see real league averages for any tendency we wanted.  We could then see just how far above or below a given team was compared to the league average.  Maybe Oakland used six offensive linemen (6 OL) personnel at twice the league rate?  Does this suggest they run more in short-yardage or goal line situations?  We could find out by see how often they ran from a 6 OL set in given downs & distances.

Of course we don't have the entire season's worth of data available here, so the two combined play-by-play charts will serve as a proof of concept in how we would approach this analysis.

<BR>


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

Barring extreme and rare circumstances, this means that explosive plays will almost always be "successful" plays as well, but the reverse is not true.  Another point to note is that penalties are not counted in "successful" play tallies (this is my choice).  A defensive pass interference penalty results in an automatic 1st down, which would always be considered a "successful" play for the offense, but I wanted to focus on plays the offense actually executed. So, plays with defensive penalties were simply removed from the "successful" play tally, not counting as either good or bad.

Counting such penalties as "successful" plays (i.e. crediting the offense for their occurrence) is likely to be more predictive if modeling future performance.  This short write up is not attempting to do such extensive modeling, so penalties will be discussed in their own section, which I believe works out fine.  

The most basic component to examining what contributes to successful plays is the _down & distance_ situation the team is in that has success.  Using the two game charting files combined, and removing defensive penalties, left us with 156 total plays.  The average distance to go per down and the number of times that down produced a successful or unsuccessful play were found.  

###### Successful Plays
Result       | Count | Percent Total
-------------|-------|--------------
Unsuccessful | 82    | 52.6%
Successful   | 74    | 47.4%

<BR>

###### Successful Play Breakdown by Down & Distance
Result           | Down | Avg. Dist. for 1D | Count | % Total Plays per Down
-----------------|------|-------------------|-------|-----------------------
Unsuccessful     | 1    | 9.64              | 42    | 59.1%
Unsuccessful     | 2    | 8.27              | 22    | 42.3%
Unsuccessful     | 3    | 8.23              | 17    | 54.8%
Unsuccessful     | 4    | 1.00              | 1     | 50%
Successful       | 1    | 9.31              | 29    | 40.9%
Successful       | 2    | 7.40              | 30    | 57.7%
__Successful__   | __3__| __3.78__          | __14__ | 45.2%
Successful       | 4    | 4.00              | 1     | 50%




The first thing to note is that while there were more unsuccessful plays (82, 52.6%) than successful (74, 47.4%), the margin was small (8).  This difference was smaller than I expected, to be frank.  I don't know what the exact expected percentages would be, but internally I was expecting something closer to a 2:1 ratio, unsuccessful-to-successful.  While I don't have the entire season's worth of data to investigate, my first hunch is that there are two primary reasons we see a near 1:1 ratio above.

1. Very small sample size.
    + Only 156 plays are being analyzed.  That amounts to about one game's worth of plays (counting both teams).  Any wild variance can be observed in a lone game's sample.  

2. Both offenses charted were good-to-very-good.  
    + Green Bay and Oakland finished 2016 as the 4th and 7th ranked offenses, respectively.
    + Oakland was 4th in offense at the time of their game above (losing QB Carr for the final stretch of the year deceptively lowered their final offensive rating)
    + Green Bay was 10th offensively at the time of their game, but their opponent (Chicago) was 19th in defense.  Green Bay also began to function much more effectively on offense beginning with this game.
    + While both teams changed offensive trajectories during the season, both ultimately were among the best in the league.  Having a small sample only come from two of the best offenses is going to produce a skewed result.

With that said, the most interesting result was that the average distance to go was smaller for plays that were successful vs. ones that weren't.  (There was only one 4th Down play for each category, meaning we can discard it).  This is what we would expect, overall.  However, generally speaking we would think that 1st downs would be fairly similar in distance since the overwhelming number of 1st downs will be 1st & 10 (penalties are the exception).  

But for 2nd, 3rd, and 4th (if there were enough in the dataset) we would think that "successful" plays are more likely to occur when distances needed for "success" are shorter.  And we do see this, but not in an equally distributed manner.  

###### Average Distances for a 1st Down
Down | Avg. Unsuccessful Distance | Avg. Successful Distance| Difference
-----|----------------------------|-------------------------|-----------
1    | 9.64                       | 9.31                    | -0.33
2    | 8.27                       | 7.40                    | -0.83
__3__| 8.23                       | 3.78                    | __-4.45__


The difference between successful and unsuccessful 2nd down plays is less than a yard.  For 3rd downs this difference jumps to 4.45 yards!  That's significant.




df.groupby(['Successful_Play', 'Down'])['Down'].count().sort_values(ascending=False)
['Series', 'Play', 'Quarter', 'Time', 'Score_Margin', 'Down', 'Distance',
       'POS', 'Play_Type', 'Personnel', 'Formation', 'Motion', 'Runner',
       'Lead_Block', 'Target', 'Catch', 'Gain', 'Penalty', 'Play_Action',
       'Pass_Area', 'Pass_Depth', 'Run_Area', 'Def_Package', 'Def_Front',
       'Pass_Rushers', 'Team', 'Home/Road', 'Opponent', 'Goal_Line',
       'LOS_to_Goal', 'Net_Gain', 'Minute', 'Second', 'Num_RB', 'Num_TE',
       'Num_WR', '6_OL', 'Left_Split', 'Right_Split', 'Shotgun',
       'Shotgun_Offset', 'I-Form', 'I-Form_Offset', 'Motion_Bool',
       'Motion_Pos', 'Motion_Dir', 'Target_Pos', 'Target_Align', 'Pass_Dir',
       'TD', 'Explosive_Pass', 'Explosive_Pass_Yd', 'Explosive_Run',
       'Explosive_Run_Yd', 'Explosive_Play', 'Successful_Pass',
       'Successful_Run', 'Successful_Play', 'Sack_TFL', 'Sack_TFL_Yards',
       'Penalty_Team', 'Penalty_Type', 'Penalty_Yards']















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
