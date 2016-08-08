import goldsberry
import goldsberry.game
import goldsberry.league
import goldsberry.player
import goldsberry.team
import goldsberry.draft
import goldsberry.playtype
import goldsberry.sportvu
from goldsberry.player._Player2 import PlayerList
from goldsberry.game._Game2 import GameIDs
import pandas as pd
import numpy as np
from scipy.stats import binned_statistic_2d
import seaborn as sns
from bokeh.plotting import figure
from math import pi
%matplotlib inline
import urllib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
pd.set_option("display.max_columns", 50)
pd.options.mode.chained_assignment = None 
urllib.__version__
goldsberry.__version__

players = goldsberry.PlayerList()
players2015 = pd.DataFrame(players.players())
players2015.head()

players.GET_raw_data()

players.api_params

players.SET_parameters(IsOnlyCurrentSeason = 0)
players.GET_raw_data()
playersAllTime = pd.DataFrame(players.players())
playersAllTime.head()

#Harden
players2015.ix[players2015['DISPLAY_LAST_COMMA_FIRST'].str.contains("Harden")]

harden_id = '201935'

harden_game_logs = goldsberry.player.game_logs(harden_id)

harden_game_logs_2015 = pd.DataFrame(harden_game_logs.logs())

harden_game_logs_2015.head()

harden_shots = goldsberry.player.shot_chart(harden_id)

harden_shots = pd.DataFrame(harden_shots.chart())

sns.set_style("white")
sns.set_color_codes()
plt.figure(figsize=(12,11))
plt.scatter(harden_shots.LOC_X, harden_shots.LOC_Y)
plt.show()

right = harden_shots[harden_shots.SHOT_ZONE_AREA == "Right Side(R)"]
plt.figure(figsize=(12,11))
plt.scatter(right.LOC_X, right.LOC_Y)
plt.xlim(-300,300)
plt.ylim(-100,500)
plt.show()

from matplotlib.patches import Circle, Rectangle, Arc

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

plt.figure(figsize=(12,11))
plt.scatter(harden_shots.LOC_X, harden_shots.LOC_Y)
draw_court(outer_lines=True)
# Descending values along the axis from left to right
plt.xlim(300,-300)
plt.show()

plt.figure(figsize=(12,11))
plt.scatter(harden_shots.LOC_X, harden_shots.LOC_Y)
draw_court()
# Adjust plot limits to just fit in half court
plt.xlim(-300,300)
# Descending values along th y axis from bottom to top
# in order to place the hoop by the top of plot
plt.ylim(422.5, -47.5)
# get rid of axis tick labels
# plt.tick_params(labelbottom=False, labelleft=False)
plt.show()

def get_player_img(player_id):
    """Returns the image of the player from stats.nba.com

    Parameters
    ----------
    player_id: int
        The player ID used to find the image.
    """
    url = "http://stats.nba.com/media/players/230x185/"+str(player_id)+".png"
    img_file = str(player_id) + ".png"
    img = plt.imread(urllib.urlretrieve(url, img_file)[0])
    return plt.imshow(img)
