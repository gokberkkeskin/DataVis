import numpy as np
import plotly.express as px

# Plot histogram based on rolling 2 dice
dice_1 = np.random.randint(1, 7, 5000)
dice_2 = np.random.randint(1, 7, 5000)
dice_sum = dice_1 + dice_2
# bins represent the number of bars to make
fig = px.histogram(dice_sum, nbins=11, labels={'value': 'Dice Roll'},
                   title='5000 Dice Roll Histogram', marginal='violin',
                   color_discrete_sequence=['green'])

fig.show(renderer="browser")
