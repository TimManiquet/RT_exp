#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reaction Time experiment

each block includes all 185 images/trials, 6 blocks (6 types of questions) in one run 

Created on Wed Feb 15 15:11:45 2023
"""

### —————————————— Preamble —————————————— ###

# Packages
import pandas as pd
import pathlib, glob
import numpy as np
from psychopy import visual, event, gui
from scripts.funcs import run
import datetime

# Information to collect at the start
info= {'ID':'', 'Age':'','Gender':''} # 'ID':''(sona-system ID code), 'Age':'','Gender':''

# Experimental stimuli
stim_list = glob.glob(r'./stimuli/*.png') # main task stimuli
stim_df = pd.DataFrame({
    'stim_file': stim_list, # stimulus file
    'exp_phase': [(pathlib.Path(file).stem).split('_')[0] for file in stim_list], # practice or main task
    'stim_cat': [(pathlib.Path(file).stem).split('_')[1] for file in stim_list], # category in the image
    'stim_nb' : [(pathlib.Path(file).stem).split('_')[2] for file in stim_list] # number of the image
})

# Window display parameters
size = (1440,900)
fullscr = False
units = 'pix'
screen_color = '#BABAB9'


### —————————————— Experiment —————————————— ###

# Collect information at the start
infoDlg=gui.DlgFromDict(dictionary=info)
# Create the experiment window
win = visual.Window(size = size, fullscr = fullscr, units = units, color = screen_color)

# # Show general instructions
visual.ImageStim(win, fr'instructions/general_instructions.png').draw()
win.flip()
event.waitKeys(keyList = ('space'))

### Practice
# Show the instructions for the practice sessions
visual.ImageStim(win, fr'instructions/practice_start.png').draw()
win.flip()
event.waitKeys(keyList = ('space'))
# start the practice phase
practice_df = run(
    win, # where to play the experiment
    stimuli = stim_df, # which images to use
    exp_phase = 'practice', # only use the practice images
    categories = ['face', 'scene', 'body'], # all except objects
    keys = ['f', 'j'], # which keys to use
    interval_time=0.4, 
    feedback_time=0.5)

### Main task
# Show the instructions for the main task
visual.ImageStim(win, fr'instructions/main_start.png').draw()
win.flip()
event.waitKeys(keyList = ('space'))
# Start run 1
main_df1 = run(
    win, # where to play the experiment
    stimuli = stim_df, # which images to use
    exp_phase = 'main', # only use the practice images
    categories = ['face', 'scene', 'body'], # all except objects
    keys = ['f', 'j'], # which keys to use
    interval_time=0.4, 
    feedback_time=0.5)

# Start run 2
main_df2 = run(
    win, # where to play the experiment
    stimuli = stim_df, # which images to use
    exp_phase = 'main', # only use the practice images
    categories = ['face', 'scene', 'body'], # all except objects
    keys = ['f', 'j'], # which keys to use
    interval_time=0.4, 
    feedback_time=0.5)
# Show the break instructions after run 2
visual.ImageStim(win, fr'instructions/run02_finish.png').draw()
win.flip()
event.waitKeys(keyList = ('space'))

# Start run 3
main_df3 = run(
    win, # where to play the experiment
    stimuli = stim_df, # which images to use
    exp_phase = 'main', # only use the practice images
    categories = ['face', 'scene', 'body'], # all except objects
    keys = ['f', 'j'], # which keys to use
    interval_time=0.4, 
    feedback_time=0.5)

# Finish the experiment
visual.ImageStim(win, fr'instructions/ending_text.png').draw()
win.flip()
event.waitKeys()
win.close()


### —————————————— Collect data —————————————— ###

# add some important info to the dataframes
practice_df['run'] = 0
main_df1['run'] = 1
main_df2['run'] = 2
main_df3['run'] = 3
# create the main output dataframe
df = pd.concat([practice_df, main_df1, main_df2, main_df3])
df['age'] = info['Gender']
df['gender'] = info['Age']
df['ID'] = info['ID']

# Finally export the data
df.to_csv(fr'{str(datetime.date.today())}_ppt{ID}.csv') # include the date in the file name
