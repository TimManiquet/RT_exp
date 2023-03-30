# This function is used by the main experiment script

import numpy as np

def image_list (qall, exp_parameters):
    
    '''
    function to generate stimuli list for one run: [stimuli,stimuli_index,category]*trial_num*block_num
                                

    Parameters
    ----------
    qall:image sets
    trial_num:numbers of trials/stimuli presented in each block
    block_num:numbers of blocks in one run
    
    Returns : stimuli_list_for_one_run
    -------
    None.

    '''
    
    
    stimuli_list_for_one_run = []
    
    for i in range(exp_parameters['block_num']):
        
        #shuffle the qall array
        np.random.shuffle(qall) #[stimuli_index, category]
        
        block_list = [] #trial_list * block_num

        for stimuli_index, category in qall:
            
            stimuli = (r'stimuli/' +'stim' +str(stimuli_index).zfill(3) + '.bmp')
            block_list.append([stimuli,stimuli_index,category])
        
        stimuli_list_for_one_run.append(block_list)   
        
    return (stimuli_list_for_one_run)

