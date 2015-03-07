
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# In[2]:

def convert_score_to_spread(play):
    if len(play['Time'].split(':'))!=2:
        return(None)
    spread = np.diff([int(score) for score in str(play['Score']).split('-')])
    return(spread)


# In[3]:

def get_plays(url):
    
    parsed_html = pd.read_html(url)
    
    # Need to handle indices of periods:
    first_ind = 0
    while parsed_html[first_ind].irow(0)[0]!='Time':
        first_ind += 1
    inds = first_ind + np.arange(0,int(np.ceil((len(parsed_html)-4)/2.)))*2
    
    # Concatenate tables to get a table of plays:
    plays = pd.concat([parsed_html[ind].irow(range(1,parsed_html[ind].shape[0])) for ind in inds])
    plays.columns = parsed_html[inds[0]].irow(0)
    plays.index = range(plays.shape[0])

    # Compute seconds in for each play:
    seconds_in = range(plays.shape[0])
    period_counter = 0
    
    for i in range(plays.shape[0]):
        time = plays.irow(i)['Time'].split(':')
        if len(time) != 2:
            seconds_in[i] = None
            period_counter += 1
        else:
            
            if period_counter <= 1:
                offset = period_counter*60*20
            else:
                offset = 60*20+(period_counter-1)*60*5
            seconds = 60*20-60*int(time[0])-int(time[1])
            seconds_in[i] = offset+seconds

    # Add seconds in and point spread to table:
    plays['Seconds In'] = seconds_in
    if(plays.columns[1] == 'Virginia Tech'):
        plays['Spread'] = plays.apply(convert_score_to_spread,axis=1)['Score']
    else:
        plays['Spread'] = -plays.apply(convert_score_to_spread,axis=1)['Score']
    plays = plays[pd.notnull(plays['Score'])]
    
    return(plays)


# In[5]:

if __name__ == '__main__':
    
    get_ipython().magic(u'pylab')
    url = 'http://stats.ncaa.org/game/play_by_play/52182'
    plays = get_plays(url)
    plt.plot(plays['Seconds In'],plays['Spread'])


# In[ ]:



