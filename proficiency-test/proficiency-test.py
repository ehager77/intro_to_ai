import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
pd.options.mode.chained_assignment = None

# Import the database as a Pandas dataframe.
baseball_data = pd.read_csv('./baseball-data.csv')
pd_baseball = baseball_data.dropna()

batting_avg_max = pd_baseball.loc[pd_baseball['Batting Average'].idxmax()]

home_runs_max = pd_baseball.loc[pd_baseball['Home Runs'].idxmax()]

# Which player had the highest batting average? The lowest? Make sure to print out your results.
print('Highest Batting Average was ' + str(batting_avg_max['Batting Average']))
print('Highest Batting Average belonged to' + str(batting_avg_max['PLAYER']).split(',')[1] + " " + str(batting_avg_max['PLAYER']).split(',')[0])

# Which player had the highest # of home-runs per game?
pd_baseball['Home Runs per Game'] = pd_baseball['Home Runs'] / pd_baseball['Games Played']
# print(pd_baseball)
hrpg_max = pd_baseball.loc[pd_baseball['Home Runs per Game'].idxmax()]

print('The most Home Runs per Game was ' + str(hrpg_max['Home Runs per Game']))
print('The most Home Runs per Game belonged to' + str(hrpg_max['PLAYER']).split(',')[1] + " " + str(hrpg_max['PLAYER']).split(',')[0])

# Do players with higher batting averages tend to score more home runs per game? Create a scatter plot and determine if a relationship exists (make sure to include labels!
pd_baseball.plot.scatter(x='Batting Average', y='Home Runs per Game', c='Red')
x,y = pd.Series(pd_baseball['Batting Average']), pd.Series(pd_baseball['Home Runs per Game'])
corr_co = x.corr(y)
print("Correlation coefficient between Batting Average and Home Runs per game is " + str("%.2f" % corr_co))
plt.show()
plt.clf()

# What is the mean number of games played? The median?
games_played = pd_baseball['Games Played'].to_numpy()
print('Median Games Played per Player: ' + str(np.median(games_played)))

# Plot a histogram of this data, choosing an appropriate bin size, and observe the distribution
plt.hist(x, bins = 40)
plt.show()

# Isolate players who play on 1st Base, and those who play outfield.
first_basemen = pd_baseball.loc[pd_baseball['POS'] == '1B']
outfielders = pd_baseball.loc[pd_baseball['POS'] == 'OF']
first_and_out = [first_basemen, outfielders]
first_and_out = pd.concat(first_and_out)

big_hitter = first_and_out.loc[first_and_out['Home Runs'].idxmax()]

# To which position does the highest home-run scoring player belong to?
print('Most home runs by either a 1B or OF was:' + str(big_hitter['PLAYER']).split(',')[1] + ' ' + str(big_hitter['PLAYER']).split(',')[0] + " - " + str(big_hitter['POS']))

# Compare the means and medians of batting averages. Can you conclude that one group hits more successfully than the other?
fb_median_bavg = first_basemen['Batting Average'].to_numpy()
fb_median_bavg = np.median(fb_median_bavg)
print('1B Median Batting Average')
print(fb_median_bavg)

of_median_bavg = outfielders['Batting Average'].to_numpy()
of_median_bavg = np.median(of_median_bavg)
print('OF Median Batting Average')
print(of_median_bavg)

fb_mean_bavg = first_basemen['Batting Average'].to_numpy()
fb_mean_bavg = np.mean(fb_median_bavg)
print('1B Mean Batting Average')
print(fb_median_bavg)

of_mean_bavg = outfielders['Batting Average'].to_numpy()
of_mean_bavg = np.mean(of_median_bavg)
print('OF Mean Batting Average')
print(of_mean_bavg)

# Based on results, mean and median are the same with OF having a slightly better BA on average