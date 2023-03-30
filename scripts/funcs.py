# This function is used in the main experiment script

import numpy as np
import pandas as pd
import pathlib, time
from psychopy import visual, event, core


def run_block(win, images, yes_key, no_key, category, exp_parameters):
    
    '''
    This is an internal function that shouldn't be called outside of 'run'.
    
    This function plays a block of detection trials for a given category. This block is divided in 2,
    with the detection key assigned to F and to J in each part respectively. Each part of the block
    consists of 185 trials, with one image presented each time.
    
    Parameters
    ——————————
     • win : the psychopy window to display the task in
     • images : the images to show for each trial.
     • keys : answer keys. The first one is the correct one by convention.
     • category : the category to detect during the block.
     • exp_parameters : list of parameters to use (ITI, etc.).
    '''
    
    # create a dictionary to save the data
    data = { # list all the variables of interest we want to save
        'trial_nb': [],
        'rt': [],
        'acc':[],
        'response':[],
        'image': [],
        'category':[],
        'exp_phase':[],
        'yes_key': []
    }

    # show instructions for the task until 'space' is pressed
    visual.ImageStim(win, fr'instructions/q{category}_{yes_key}_{no_key}.png').draw()
    win.flip()
    event.waitKeys(keyList = ('space'))
    
    # plays images, record response
    for n in range(len(images)):
        
        # find the file to show
        stimulus_file = images['stim_file'].values[n]
        # create the image to show
        image = visual.ImageStim(win, image = stimulus_file, size = (500,500)) 
        # show the fixation cross
        visual.ImageStim(win, fr'instructions/cross.png').draw()
        win.flip()
        core.wait(exp_parameters['interval_time'])
        
        # show the stimulus
        image.draw()
        win.flip()
    
        # start measuring the RT
        startTime = time.time()
        # wait for a response
        response = event.waitKeys(keyList = (yes_key, no_key))[0]
        # calculate the RT
        rt = time.time() - startTime
            
        # check the answer, make it true or false
        # if the target was present
        if category == images['stim_cat'].values[n]:
            # the answer is correct if the 'yes' key was pressed
            if response == yes_key:
                acc = True
            # the answer is incorrect if the 'no' key was pressed
            elif response == no_key:
                acc = False
        # else if the target was absent
        elif category != images['stim_cat'].values[n]:
            # the answer is correct if the 'no' key was pressed
            if response == no_key:
                acc = True
            # the answer is incorrect if the 'yes' key was pressed
            elif response == yes_key:
                acc = False
        
        # if training, show feedback
        if images['exp_phase'].values[n] == 'practice':
            if acc: # if the answer was correct show correct feedback
                visual.ImageStim(win, fr'instructions/correct.png').draw()
            elif not acc: # if the answer was incorrect show incorrect feedback
                visual.ImageStim(win, fr'instructions/wrong.png').draw()
            win.flip()
            core.wait(exp_parameters['feedback_time'])
            
        # append data from the trial
        data['trial_nb'].append(n)
        data['rt'].append(rt)
        data['acc'].append(acc)
        data['response'].append(response)
        data['image'].append(pathlib.Path(stimulus_file).stem)
        data['category'].append(images['stim_cat'].values[n])
        data['exp_phase'].append(images['exp_phase'].values[n])
        data['yes_key'].append(yes_key)
    
    # return the collected data
    return data



def run(win, stimuli, exp_phase, categories = ['face', 'object', 'scene', 'body'], keys = ['f', 'j'], interval_time=0.4, feedback_time=0.5):
    
    '''
    This function plays a run of a detection task. A run consists of several conditions, played randomly one 
    after the other. During each condition, participants need to indicate the presence/absence of a 
    scene/body/face/object in the presented picture, by pressing F/J for present. Each condition is associated
    with a detection key, of which the order is chosen randomly.
    
    The total number of conditions will depend on the numbe of inut categories. For instance, a  combination
    of 3 categories to detect and 2 possible detection keys makes up 6 conditions.
    
    Parameters
    ——————————
     • win : a psychopy window to play the task in.
     • stimuli : a dataframe holding the images to present.
     • exp_phase : either practice or main. Will determine which images to use and whether feedback is given.
     • categories : list. Categories to include in the run. Defaults to all the categories.
     • keys : list. The two keys to use to indicate whether the category is present. Defaults to 'f' and 'j'.
     • exp_parameters : the experimental parameters to use in each block.
     
     Returns
    ——————————
     • df : the resulting data from the runs.
    '''
    
    # create an empty dataframe
    df = pd.DataFrame()
    
    # start a block number count
    block_nbr = 0
    
    # start by randomising the order of the categories
    np.random.shuffle(categories)
    
    # run 2 key conditions per category
    for category in categories:
        
        # start by randomising the order of the keys
        np.random.shuffle(keys)
        
        for key in keys:
            
            # define the correct key
            yes_key = key
            # define the incorrect key
            no_key  = [key for key in keys if key != yes_key][0]
            
            # take in the stimuli and randomise their order
            images = stimuli.loc[stimuli['exp_phase']==exp_phase].sample(frac=1)
            
            # run the block for that key and category condition
            data = run_block(
                win = win, 
                images = images, 
                yes_key = yes_key, 
                no_key = no_key, 
                category = category,
                exp_parameters={'interval_time':interval_time, 'feedback_time':feedback_time})
            
            # after the block, increase block number count
            block_nbr += 1
            
            # # play a break after each block except the last one
            if category != categories[-1]:
                visual.ImageStim(win, fr'instructions/break.png').draw()
                win.flip()
                event.waitKeys(keyList = ('space'))
            
            # append the block data to the run data
            datadf = pd.DataFrame.from_dict(data)
            # add some important info
            datadf['block'] = block_nbr
            datadf['task'] = category
            # create the final df to export
            df = pd.concat([df, datadf]).reset_index(drop=True)

    return df



















# def showimage (stimuli_list_for_one_run,is_practice,result_list, win, questions, event_images, exp_parameters):
    
#     '''
#     function to present stimuli of each trial and record details of the response :
#         result_list =response_list_block * block_num = [stimuli_index, category, response_key, correct/wrong, reaction_time]*trial_num*block_num

#     Parameters
#     ----------
#     stimuli_list_for_one_run : stimuli list created by function image_list (qall, block_num)
#     result_list : the list that record the results for one run
#     is_practice : whether the session is practice session or not, if it is practice, there would be feedbacks 

#     Returns : result_list
#     -------

#     '''
    
#     #shuffle the questions and the stimuli
#     np.random.shuffle (questions) #Ask questions twice for each interested category, the left and right hand response keys will be swapped to avoid the effect of motor activity
#     np.random.shuffle(stimuli_list_for_one_run)
    
    
#     #present stimuli for each block: for each block, question will be presented in advance for only once 
#         #if the participant forget the question during this block, they can skip by pressing 'q', and skipped block can be check later
    
#     for m in range(exp_parameters['block_num']):
        
#         show_list_for_one_block = stimuli_list_for_one_run[m] #[stimuli,stimuli_index,category]*trial_num
#         response_list_block = [] #[stimuli_index, category, response_key, correct/wrong, reaction_time,block_number]
        
#         #question and response instructions given in advance
#         questions[m].draw() #ask question
#         win.flip()
#         event.waitKeys(keyList = ('space'))
        
#         correct_num = 0
        
        
            
#         for n in show_list_for_one_block:
            
            
#             image = visual.ImageStim(win, image = n[0], size = (500,500)) 
    
#             event_images['cross'].draw()
#             win.flip()      
#             core.wait(exp_parameters['interval_time'])
            
#             image.draw()
#             win.flip()
            
        
#             #measure the reaction time for each response
#             startTime = time.time()
            
#             response = event.waitKeys(keyList = exp_parameters['response_key'])
            
#             endTime = time.time()
            
#             rt = endTime - startTime
            
          
#             if 'q' in response: #detect 'q to skip this block
#                 used_q = 'skipped'
#                 break
                
              
#                 #[stimuli,stimuli_index,category]
            
#             #faces
#             if questions[m] == event_images['qfaces_f_j']:
                
#                 used_q = 'qfaces_f_j'
                
#                 if 'f' in response and n[2] == 'faces':
#                     evaluation = 'correct'
#                 elif 'j' in response and n[2] in ['bodies','scenes','objects']:
#                     evaluation = 'correct'
#                 else:
#                     evaluation = 'wrong'
            
#             elif questions[m] == event_images['qfaces_j_f']:
#                 used_q = 'qfaces_j_f'
                
#                 if 'j' in response and n[2] == 'faces':
#                     evaluation = 'correct'
#                 elif 'f' in response and n[2] in ['bodies','scenes','objects']:
#                     evaluation = 'correct'
#                 else:
#                     evaluation = 'wrong'
            
#             #bodies
#             elif questions[m] == event_images['qbodies_f_j']:
#                 used_q = 'qbodies_f_j'
                
#                 if 'f' in response and n[2] == 'bodies':
#                     evaluation = 'correct'
#                 elif 'j' in response and n[2] in ['faces','scenes','objects']:
#                     evaluation = 'correct'
#                 else:
#                     evaluation = 'wrong'
            
#             elif questions[m] == event_images['qbodies_j_f']:
#                 used_q = 'qbodies_j_f'
                
#                 if 'j' in response and n[2] == 'bodies':
#                     evaluation = 'correct'
#                 elif 'f' in response and n[2] in ['faces','scenes','objects']:
#                     evaluation = 'correct'
#                 else:
#                     evaluation = 'wrong'
            
#             #scenes
#             elif questions[m] == event_images['qscenes_f_j']:
#                 used_q = 'qscenes_f_j'
                
#                 if 'f' in response and n[2] == 'scenes':
#                     evaluation = 'correct'
#                 elif 'j' in response and n[2] in ['faces','bodies','objects']:
#                     evaluation = 'correct'
#                 else:
#                     evaluation = 'wrong'
            
#             elif questions[m] == event_images['qscenes_j_f']:
#                 used_q = 'qscenes_j_f'
                
#                 if 'j' in response and n[2] == 'scenes':
#                     evaluation = 'correct'
#                 elif 'f' in response and n[2] in ['faces','bodies','objects']:
#                     evaluation = 'correct'
#                 else:
#                     evaluation = 'wrong'
            
  
             
#             #give feedback if it is a practice session
            
#             if is_practice == True:
                
#                 if evaluation == 'correct':
#                     event_images['correct'].draw()
#                 elif evaluation == 'wrong':
#                     event_images['wrong'].draw()
                
#                 win.flip()
#                 core.wait(exp_parameters['feedback_time'])
            
#             #response_list=[stimuli_index, category,response, evaluation, reaction_time,block_number]
#             response_list_block.append ([n[1], n[2], ''.join(response), evaluation, rt, str(m)])
            
#             #calculating correct numbers for answer accuracy
#             if evaluation == 'correct':
#                 correct_num = correct_num +1              
#             else:
#                 correct_num = correct_num +0
                
    
#         accuracy = (correct_num/exp_parameters['trial_num'])*100  
        
#         #result_list = [response_list, accuracy, question_asked_for_this_block/skipped]
#                        #response_list=[stimuli_index, category,response, evaluation, reaction_time,block_number]
        
#         result_list.append([response_list_block,accuracy,used_q])
        
#         if 'q' in response: #skip one block and continue the following blocks
#             continue
                     
#         #break time between blocks
#         if m != (exp_parameters['block_num'] -1) :
#             event_images['rest'].draw()
#             win.flip()
#             event.waitKeys(keyList = ('space'))
    
#     return False
























    
    # #shuffle the questions and the stimuli
    # np.random.shuffle (questions) #Ask questions twice for each interested category, the left and right hand response keys will be swapped to avoid the effect of motor activity
    # np.random.shuffle(stimuli_list_for_one_run)
    
    
    # #present stimuli for each block: for each block, question will be presented in advance for only once 
    #     #if the participant forget the question during this block, they can skip by pressing 'q', and skipped block can be check later
    
    # for m in range(exp_parameters['block_num']):
        
    #     show_list_for_one_block = stimuli_list_for_one_run[m] #[stimuli,stimuli_index,category]*trial_num
    #     response_list_block = [] #[stimuli_index, category, response_key, correct/wrong, reaction_time,block_number]
        
    #     #question and response instructions given in advance
    #     questions[m].draw() #ask question
    #     win.flip()
    #     event.waitKeys(keyList = ('space'))
        
    #     correct_num = 0
        
        
            
    #     for n in show_list_for_one_block:
            
            
    #         image = visual.ImageStim(win, image = n[0], size = (500,500)) 
    
    #         event_images['cross'].draw()
    #         win.flip()      
    #         core.wait(exp_parameters['interval_time'])
            
    #         image.draw()
    #         win.flip()
            
        
    #         #measure the reaction time for each response
    #         startTime = time.time()
            
    #         response = event.waitKeys(keyList = exp_parameters['response_key'])
            
    #         endTime = time.time()
            
    #         rt = endTime - startTime
            
          
    #         if 'q' in response: #detect 'q to skip this block
    #             used_q = 'skipped'
    #             break
                
              
    #             #[stimuli,stimuli_index,category]
            
    #         #faces
    #         if questions[m] == event_images['qfaces_f_j']:
                
    #             used_q = 'qfaces_f_j'
                
    #             if 'f' in response and n[2] == 'faces':
    #                 evaluation = 'correct'
    #             elif 'j' in response and n[2] in ['bodies','scenes','objects']:
    #                 evaluation = 'correct'
    #             else:
    #                 evaluation = 'wrong'
            
    #         elif questions[m] == event_images['qfaces_j_f']:
    #             used_q = 'qfaces_j_f'
                
    #             if 'j' in response and n[2] == 'faces':
    #                 evaluation = 'correct'
    #             elif 'f' in response and n[2] in ['bodies','scenes','objects']:
    #                 evaluation = 'correct'
    #             else:
    #                 evaluation = 'wrong'
            
    #         #bodies
    #         elif questions[m] == event_images['qbodies_f_j']:
    #             used_q = 'qbodies_f_j'
                
    #             if 'f' in response and n[2] == 'bodies':
    #                 evaluation = 'correct'
    #             elif 'j' in response and n[2] in ['faces','scenes','objects']:
    #                 evaluation = 'correct'
    #             else:
    #                 evaluation = 'wrong'
            
    #         elif questions[m] == event_images['qbodies_j_f']:
    #             used_q = 'qbodies_j_f'
                
    #             if 'j' in response and n[2] == 'bodies':
    #                 evaluation = 'correct'
    #             elif 'f' in response and n[2] in ['faces','scenes','objects']:
    #                 evaluation = 'correct'
    #             else:
    #                 evaluation = 'wrong'
            
    #         #scenes
    #         elif questions[m] == event_images['qscenes_f_j']:
    #             used_q = 'qscenes_f_j'
                
    #             if 'f' in response and n[2] == 'scenes':
    #                 evaluation = 'correct'
    #             elif 'j' in response and n[2] in ['faces','bodies','objects']:
    #                 evaluation = 'correct'
    #             else:
    #                 evaluation = 'wrong'
            
    #         elif questions[m] == event_images['qscenes_j_f']:
    #             used_q = 'qscenes_j_f'
                
    #             if 'j' in response and n[2] == 'scenes':
    #                 evaluation = 'correct'
    #             elif 'f' in response and n[2] in ['faces','bodies','objects']:
    #                 evaluation = 'correct'
    #             else:
    #                 evaluation = 'wrong'
            
  
             
    #         #give feedback if it is a practice session
            
    #         if is_practice == True:
                
    #             if evaluation == 'correct':
    #                 event_images['correct'].draw()
    #             elif evaluation == 'wrong':
    #                 event_images['wrong'].draw()
                
    #             win.flip()
    #             core.wait(exp_parameters['feedback_time'])
            
    #         #response_list=[stimuli_index, category,response, evaluation, reaction_time,block_number]
    #         response_list_block.append ([n[1], n[2], ''.join(response), evaluation, rt, str(m)])
            
    #         #calculating correct numbers for answer accuracy
    #         if evaluation == 'correct':
    #             correct_num = correct_num +1              
    #         else:
    #             correct_num = correct_num +0
                
    
    #     accuracy = (correct_num/exp_parameters['trial_num'])*100  
        
    #     #result_list = [response_list, accuracy, question_asked_for_this_block/skipped]
    #                    #response_list=[stimuli_index, category,response, evaluation, reaction_time,block_number]
        
    #     result_list.append([response_list_block,accuracy,used_q])
        
    #     if 'q' in response: #skip one block and continue the following blocks
    #         continue
                     
    #     #break time between blocks
    #     if m != (exp_parameters['block_num'] -1) :
    #         event_images['rest'].draw()
    #         win.flip()
    #         event.waitKeys(keyList = ('space'))
    
    # return False