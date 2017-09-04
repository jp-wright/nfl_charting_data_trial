# NFL Game Charting (mini-project)

Given two game charts from one team per game only, a chart of a team's use of a specific formation for half the season, and a chart show all of a specific QB's passes for half a season, what "football-relative" concepts can we elucidate?  While certain conclusions would be spurious due to having such limited data, trends within these small data subsets can still be discovered and reported.  The point of this mini-project is to show that a data-focused analysis could indeed be an effective tool in revealing aspects to a game, a team, or a player that went previously unnoticed.


## Table of Contents
1. [Dataset](#dataset)
2. [Successful and Explosive Plays](#successful-and-explosive-plays)



<BR><BR>

### Dataset
There were four charts (CSV files), all from the 2016 season.  The play-by-play charts each had only one team from the game.  This means we cannot tell for certain if the opposing team matched the chart's team's score (if we only have the relative score reported at the beginning of each drive for one team, they could end their drive with a field goal and the opponent could match, meaning the relative score would be unchanged at the beginning of the next possession for the team we are seeing data from).

1. Green Bay's play-by-play chart from Chicago @ Green Bay in Week 7.
2. Oakland's play-by-play chart from Denver @ Oakland in Week 9.
3. Seattle's uses of the _3x1_ formation in the first eight weeks of the season.
4. All of Matthew Stafford's pass attempts from the first eight weeks of the season.

I combined the two play-by-play charts to have a larger sample size for some analysis.  If all play-by-play charts for both teams in all games were available, we could combine them all and have a representative dataset for the 2016 season.  This would allow us to see real league averages for any tendency we wanted.  We could then see just how far above or below a given team was compared to the league average.  Maybe Oakland used six offensive linemen (6 OL) personnel at twice the league rate?  Does this suggest they run more in short-yardage or goal line situations?  We could find out by see how often they ran from a 6 OL set in given downs & distances.

Of course we don't have the entire season's worth of data available here, so the two combined play-by-play charts will serve as a proof of concept in how we would approach this analysis.

<BR>


### Successful and Explosive Plays
#### Successful Plays
In modern football parlance, a _successful_ play can be considered one to gain a certain number of required yards given the down and distance situation.  Since there is no single set of yardage percentage weightings that is agreed upon, I have chosen to use the following cutoffs that were originally reported by Pete Palmer, Bob Carroll, and John Thorn in _The Hidden Game of Football_ and have subsequently been the basis for Football Outsiders' [DVOA metric](http://www.footballoutsiders.com/info/methods#DVOA).

A play is a success if it gains the following percent of yards required for a first down on the given down:
+ 1st Down: 45%
+ 2nd Down: 60%
+ 3rd & 4th Down: 100%


#### Explosive Plays
Again, definitions will vary on this categorization.  For this mini-project I had to choose my own cutoffs.  If an entire database of all plays in a season (or many seasons) was processed, we could likely arrive at a certain distance for each type of play, pass and rush, which would statistically be of a certain rarity as to count for "explosiveness."  That aside, I chose what I felt were reasonable distances for "explosiveness" for each play.

+ Pass: 16+ yards
+ Rush: 12+ yards

Barring extreme and rare circumstances, this means that explosive plays will almost always be "successful" plays as well, but the reverse is not true.  Another point to note is that penalties are not counted in "successful" play tallies (this is my choice).  A defensive pass interference penalty results in an automatic 1st down, which would always be considered a "successful" play for the offense, but I wanted to focus on plays the offense actually executed. So, plays with defensive penalties were simply removed from the "successful" play tally, not counting as either good or bad.

Counting such penalties as "successful" plays (i.e. crediting the offense for their occurrence) is likely to be more predictive if modeling future performance.  This short write up is not attempting to do such extensive modeling, so penalties will be discussed in their own section, which I believe works out fine.  


##### What Makes Plays Successful?
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

<BR>


The first thing to note is that while there were more unsuccessful plays (82, 52.6%) than successful (74, 47.4%), the margin was small (8).  This difference was smaller than I expected, to be frank.  I don't know what the exact expected percentages would be, but internally I was expecting something closer to a 2:1 ratio, unsuccessful-to-successful.  While I don't have the entire season's worth of data to investigate, my first hunch is that there are two primary reasons we see a near 1:1 ratio above.

1. Very small sample size.
    + Only 156 plays are being analyzed.  That amounts to about one game's worth of plays (counting both teams).  Any wild variance can be observed in a lone game's sample.  

2. Both offenses charted were good-to-very-good.  
    + Green Bay and Oakland finished 2016 as the 4th and 7th ranked offenses, respectively.
    + Oakland was 4th in offense at the time of their game above (losing QB Carr for the final stretch of the year deceptively lowered their final offensive rating)
    + Green Bay was 10th offensively at the time of their game, but their opponent (Chicago) was 19th in defense.  Green Bay also began to function much more effectively on offense beginning with this game.
    + While both teams changed offensive trajectories during the season, both ultimately were among the best in the league.  Having a small sample only come from two of the best offenses is going to produce a skewed result.

With that said, the most interesting result was that the average distance to go was smaller for plays that were successful vs. ones that weren't.  (There was only one 4th Down play for each category, meaning we can't draw any value from it).  This is what we would expect, overall.  However, generally speaking we would think that 1st downs would be fairly similar in distance since the overwhelming number of 1st downs will be 1st & 10 (penalties are the exception).  

But for 2nd, 3rd, and 4th (if there were enough in the dataset) we would think that "successful" plays are more likely to occur when distances needed for "success" are shorter.  And we do see this, but not in an equally distributed manner.  

###### Average Distances for a 1st Down
Down | Avg. Unsuccessful Distance | Avg. Successful Distance| Difference
-----|----------------------------|-------------------------|-----------
1    | 9.64                       | 9.31                    | -0.33
2    | 8.27                       | 7.40                    | -0.83
__3__| 8.23                       | 3.78                    | __-4.45__

<BR>

The difference between successful and unsuccessful 2nd down plays is less than a yard.  For 3rd downs this difference jumps to 4.45 yards!  That's significant.  Of the 31 third down plays that didn't result in a defensive penalty, 17 resulted in a "failed" outcome.  Of those 17, five led to a field goal and two led to a fourth down attempt, one of which failed and the other which led to a field goal.  This means of all non-penalty third downs, 11 (64.7%) resulted in failed drives.  

Oakland, for example, had five drives which had successful 3rd down conversions.  The results of those drives were a field goal, touchdown, touchdown, punt, and a final punt to effectively end the game.  Oakland had a total of six scoring drives in the game, netting three field goals and three touchdowns.  A 3rd down conversion was made on 50% of those drives.  Without those 3rd down conversions, Oakland would have missed out on 17 points, which would have meant the difference in winning and losing.  Given this is but a single game, we must be cautious about the exact level of importance of converting 3rd downs.    

That said, the point is not to claim that 3rd down conversions account for 50% of all scoring, rather the gist is that 3rd downs are the "drive extending" downs in football and are going to be directly correlated with scoring more points and with surrendering fewer by way of making your opponent drive the ball further to score themselves.  As we see above in the average distances table, the difference between "successful" and "unsuccessful" 3rd downs probably has less to do with how great a single 3rd down play design is, or how great a single team is.  It stands to reason the single biggest predictor of being successful on 3rd down is being successful on 1st down and 2nd down, making 3rd down yardage much smaller to achieve in the first place.



### Team Identity and Success
While the above analysis is likely to stand at a core "football fundamental" level, one thing that's not consistent league-wide is _how_ a team has success.  Admitting premise simplification, we can ask if a team is a power-running of yesteryear team or do they rely on incorporating modern "spread" concepts to advance the ball?  With accurate team-level data we can ask, and answer, such team-level questions.  

The two team game charts we have provide an instructive example -- while Oakland and Green Bay both fielded successful offenses last year, they achieved their success in markedly different manners.  Oakland, with del Rio at the helm, favored a balanced attack that featured "heavy" sets of multiple TEs or six offensive linemen, while Green Bay continued to rely on their All-Pro caliber QB to identify and attack opponents' weaknesses through a spread-out passing game.  For those uncertain, here is a short breakdown of the three major formations used by these two teams.

+ I-Form  
    The QB is under center with a fullback and running back lined up, or 'stacked', behind him in some variation.  Run-focused formation.

+ Singleback  
    The QB is under center and a lone back (usually a halfback) is about five yards behind the QB.  Versatile formation.

+ Shotgun  
    The QB himself is about five yards behind the center.  A running back may or may not be offset from the QB.  Pass-focused formation (usually).

In terms of 'character' of formation with regards to rushing v. passing the formations above are on the spectrum as such:  

More Rushing | Mixed      | More Passing  
-------------|------------|-------------
I-Form       | Singleback | Shotgun

<BR>

Though it is important to realize that these formations are used hundreds of time a season by each team, so they really lie on a continuum of 'usage'.  


Let's take a quick look at the major formation tendencies of both teams from the games above.

###### Formation Breakdown (Sung to the tune of _Communication Breakdown_ by Led Zeppelin)
Team        | Formation     | Uses | Total Plays | % Usage
------------|---------------|------|-------------|---------
Green Bay   | Shotgun       | 62   | 86          | 72.1%
Green Bay   | I-Form        | 14   | 86          | 16.3%
Green Bay   | Singleback    | 8    | 86          | 9.3%
Oakland     | Shotgun       | 37   | 82          | 45.1%
Oakland     | Singleback    | 37   | 82          | 45.1%
Oakland     | I-Form        | 7    | 82          | 8.5%

We can see that Green Bay was in Shotgun nearly three quarters of their snaps while Oakland was in less than half of theirs.  In fact, Oakland was perfectly balanced in their split of Shotgun and Singleback.  

Also, note that Dual- and Triple TE sets occur as variants of the parent formations.  Multiple TE sets _usually_ denote a rushing focus as a team having two valid receiving TEs is rare.

Team        | Formation     | Uses | Total Plays | % Usage
------------|---------------|------|-------------|---------
Green Bay   | Dual TE       | 1    | 86          | 1.2%
Green Bay   | Triple TE     | 0    | 86          | 0%
Oakland     | Dual TE       | 20   | 82          | 24.4%
Oakland     | Triple TE     | 14   | 82          | 17.1%

<BR>

Overall we see the general character of each team further substantiated in how they use their tight ends.  Clearly Green Bay, as a more dynamic passing team, doesn't find much use for multiple TEs which constricts the space on the field for their route combinations.  Correspondingly they do not see themselves as a "power run" offense that wants to overpower opponents at the point of attack with two blocking TEs.  

Oakland, however, values the extra size and force of TEs compared to receivers when running the ball.  They used multiple TE formation variations on a total of 41.5% of total plays!  In this sense, the extra TE acts much like an extra offensive lineman.  Football uses personnel shorthand to denote how many RBs and TEs are in a set, with the remainder of free positions being WRs.  In practice, there are a total of five "variable" positions in a formation, so the number of WRs is 5 minus the sum of RB and TE.  In the shorthand, the number of RBs is listed first followed by the number of TE, as follows:

+ 00 - zero RB, zero TE, 5 WR
+ 01 - zero RB, one TE, 4 WR
+ 02 - zero RB, two TE, 3 WR
+ 10 - one RB, zero TE, 4 WR
+ 11 - one RB, one TE, 3 WR
+ 12 - one RB, two TE, 2 WR
+ 20 - two RB, zero TE, 3 WR
+ 21 - two RB, one TE, 2 WR
+ 22 - two RB, two TE, 1 WR
+ 6 OL - six offensive linemen

The personnel groupings are referred to simply as the integer number they represent, such as "eleven" personnel for "11", etc.  In general, _01_, _11_, _10_, and _00_ are among the most frequently used groupings.  The _6 OL_ grouping usually implies a run, with the extra "assignable" position that the extra offensive lineman replaces usually being a WR.  With that in mind, let's check out each team's proclivity for certain personnel groupings.  

###### Green Bay Personnel
Team        | Personnel     | Uses | Total Plays | % Usage
------------|---------------|------|-------------|---------
Green Bay   | 01            | 42   | 86          | 48.8%
Green Bay   | 00            | 15   | 86          | 17.4%
Green Bay   | 10            | 11   | 86          | 12.8%
Green Bay   | 11            | 7    | 86          | 8.1%
Green Bay   | 20            | 4    | 86          | 4.6%
Green Bay   | 12            | 4    | 86          | 4.6%
Green Bay   | 02            | 1    | 86          | 1.2%
Green Bay   | 6 OL          | 1    | 86          | 1.2%
Green Bay   | 21            | 1    | 86          | 1.2%

<BR>

###### Oakland Personnel
Team        | Personnel     | Uses | Total Plays | % Usage
------------|---------------|------|-------------|---------
Oakland     | 6 OL          | 42   | 82          | 51.2%
Oakland     | 11            | 26   | 82          | 31.7%
Oakland     | 12            | 7    | 82          | 8.5%
Oakland     | 00            | 2    | 82          | 2.4%
Oakland     | 21            | 2    | 82          | 2.4%
Oakland     | 22            | 1    | 82          | 1.2%
Oakland     | 10            | 1    | 82          | 1.2%
Oakland     | 01            | 1    | 82          | 1.2%

<BR>

Here again we see the team identities outlined above emerge in the personnel usage for each offense.  The Packers were in what's known as an "empty set" -- using no RB -- in well _over_ half (67.5%) of their snaps!  With an empty set, we know the play will be a pass and not a run.  Thus Green Bay is overtly advertising "we are going to pass" on almost half their snaps.  Obviously Mike McCarthy's descent from the West Coast coaching tree plays into his willingness to be pass happy, but we have to assume the biggest factor is that he has one of the best QBs of this generation in Aaron Rodgers.  It is a reasonable approach to utilize one of the game's best players as much as possible.  

Oakland takes a different tact with their personnel groupings, employing what is known as a "heavy" approach in placing an extra offensive lineman on the line of scrimmage in just over half (51.2%) of their plays.  Of the 42 plays the Raiders used 6 OL, 32 were with a single back, six were in I-Form, and four were in shotgun.  Of those 42 plays with 6 OL, 32 (76.2%) were rushes.  Surprisingly, the overwhelming majority (61.9%) of these plays came on 1st down.  Regarding distance, just over a quarter (28.5%) came with five yards or fewer to go.  In other words, Oakland used the 6 OL set in common running situations including nine (50%) of their 18 red zone snaps.  Clearly head coach Jack del Rio wants to power his way into the end zone.

<BR>

##### Success by Formation
The header of this entire section is "Team Identity and Success."  Unsurprisingly, we want to go a step further and see how successful each team was when using various formations and personnel groupings.  For this quick investigation we will look first at what share of total "successful" plays came from which formations and then drilling down a step further, we will see the efficiency of each formation in producing successful outcomes.

###### Green Bay Successful Formations
Team       | Formation  | Successful Plays w/ Formation | Total Successful Plays | % Successful w/ Formation
-----------|------------|-------------------------------|------------------------|--------------------------
Green Bay  | Shotgun    | 33                            | 39                     | 84.6%
Green Bay  | I-Form     | 4                             | 39                     | 10.3%
Green Bay  | Singleback | 2                             | 39                     | 5.1%

<BR>

###### Oakland Successful Formations
Team       | Formation  | Successful Plays w/ Formation | Total Successful Plays | % Successful w/ Formation
-----------|------------|-------------------------------|------------------------|--------------------------
Oakland    | Singleback | 17                            | 35                     | 48.6%
Oakland    | Shotgun    | 13                            | 35                     | 37.1%
Oakland    | I-Form     | 4                             | 35                     | 11.4%
Oakland    | Dual TE    | 9                             | 35                     | 25.7%
Oakland    | Triple TE  | 5                             | 35                     | 14.3%

<BR>

In terms of total successful plays, Green Bay was indeed most productive when they hand Rodgers the ball in the Shotgun and ask him to pick apart opposing defenses.  Conversely Oakland was again more balanced, finding good value in both the Singleback and Shotgun sets. I've also included the multiple TE variants and we see that here, too, Oakland managed to find a degree of success.  

But these numbers reflect the raw totals of these formation uses.  Yes, Green Bay had the highest number of effective plays when in the Shotgun, but they also used Shotgun over _four times_ as much as the next major formation.  We want to also see which sets each team was most efficiently successful in.

###### Green Bay Formation Efficiency
Team       | Formation  | Successful Plays w/ Formation | Total Plays w/ Formation | Formation Efficiency
-----------|------------|-------------------------------|--------------------------|--------------------------
Green Bay  | Shotgun    | 33                            | 62                       | 53.2%
Green Bay  | I-Form     | 4                             | 14                       | 28.6%
Green Bay  | Singleback | 2                             | 8                        | 25.0%

<BR>


###### Oakland Formation Efficiency
Team       | Formation  | Successful Plays w/ Formation | Total Successful Plays | % Successful w/ Formation
-----------|------------|-------------------------------|------------------------|--------------------------
Oakland    | Singleback | 17                            | 37                     | 46.0%
Oakland    | Shotgun    | 13                            | 37                     | 35.1%
Oakland    | I-Form     | 4                             | 7                      | 57.1%
Oakland    | Dual TE    | 9                             | 20                     | 45.0%
Oakland    | Triple TE  | 5                             | 14                     | 35.7%










<BR><BR><BR><BR><BR><BR>

cc = ['Team', 'Series', 'Play', 'Quarter', 'Time', 'Score_Margin', 'Down', 'Distance', 'LOS_to_Goal', 'Successful_Play', 'TD', 'Field_Goal']

df.groupby(['Team', 'Series'], as_index=False)[cc].first()

df.loc[(df['Successful_Play'] == 1) & (df['Down'] == 3), cc]




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
