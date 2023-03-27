#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reaction Time experiment

Created on Wed Feb 15 15:11:45 2023
"""


#each block includes all 185 images/trials, 6 blocks (6 types of questions) in one run 


# import random
import pandas
import time
import numpy as np
from psychopy import visual, event, core, gui


# set some parameters
interval_time = 0.3
feedback_time = 0.5

#image information:
    #qall = 1:185; 
    #qfaces = [26:50];                25 faces
    #qbodies = [1:25 101:125];        50 bodies
    #qscenes = [76:100 126:150];      50 scenes
    #qobjects = [51:75 151:185];      60 objects  # we're not interested in this category here



#two-dimension array: 1: stimuli_index, 2: category
qfaces = np.array([(x, y) for x in np.arange(26,51,1,int) for y in ['faces']])
qbodies = np.array([(x, y) for x in np.concatenate((np.arange(1,26,1,int),np.arange(101,126,1,int)), axis = 0) for y in ['bodies']])
qscenes = np.array([(x, y) for x in np.concatenate((np.arange(76,101,1,int),np.arange(126,151,1,int)), axis = 0) for y in ['scenes']]) 
qobjects = np.array([(x, y) for x in np.concatenate((np.arange(51,76,1,int),np.arange(151,186,1,int)), axis = 0) for y in ['objects']]) 

qall = np.concatenate((qfaces,qbodies,qscenes,qobjects), axis = 0)

trail_num = 185 #number of trails/stimuli in each block
block_num = 6 #numbers of blocks in each run = numbers of interested categories * 2

#practice image information:
    #practice_stimuli = 200:221; 
    #practice_qf = [200:202];      2 faces
    #practice_qb = [203:208];      6 bodies
    #practice_qs = [209:214];      6 scenes
    #practice_qo = [215:221];      7 objects

#practice stimuli set
practice_qf = np.array([(x, y) for x in np.arange(200,203,1,int) for y in ['faces']]) 
practice_qb = np.array([(x, y) for x in np.arange(203,209,1,int) for y in ['bodies']])
practice_qs = np.array([(x, y) for x in np.arange(209,215,1,int) for y in ['scenes']]) 
practice_qo = np.array([(x, y) for x in np.arange(215,222,1,int) for y in ['objects']]) 

practice_stimuli = np.concatenate((practice_qf,practice_qb,practice_qs,practice_qo), axis = 0)
practice_trail_num = 22 #number of trails/stimuli in each practice block
practice_block_num = 2 #numbers of blocks in each run


response_key = ('f','j','q') #'f' for yes, 'j' for no, 'q' for skip one block

#to enter the subject info
info= {'ID':'', 'Age':'','Gender':''} # 'ID':''(sona-system ID code), 'Age':'','Gender':''
infoDlg=gui.DlgFromDict(dictionary=info)

def image_list (qall, block_num):
    
    '''
    function to generate stimuli list for one run: [stimuli,stimuli_index,category]*trail_num*block_num
                                

    Parameters
    ----------
    qall:image sets
    trail_num:numbers of trails/stimuli presented in each block
    block_num:numbers of blocks in one run
    
    Returns : stimuli_list_for_one_run
    -------
    None.

    '''
    
    
    stimuli_list_for_one_run = []
    
    for i in range(block_num):
        
        #shuffle the qall array
        np.random.shuffle (qall) #[stimuli_index, category]
        
        block_list = [] #trail_list * block_num

        for stimuli_index, category in qall:
            
            stimuli = (r'stimuli/' +'stim' +str(stimuli_index).zfill(3) + '.bmp')
            block_list.append([stimuli,stimuli_index,category])
        
        stimuli_list_for_one_run.append(block_list)   
        
    return (stimuli_list_for_one_run)




def showimage (stimuli_list_for_one_run,is_practice,block_num,trail_num,result_list):
    
    '''
    function to present stimuli of each trial and record details of the response :
        result_list =response_list_block * block_num = [stimuli_index, category, response_key, correct/wrong, reaction_time]*trail_num*block_num

    Parameters
    ----------
    stimuli_list_for_one_run : stimuli list created by function image_list (qall, block_num) 
    result_list : the list that record the results for one run
    is_practice : whether the session is practice session or not, if it is practice, there would be feedbacks 

    Returns : result_list
    -------

    '''
    
    #shuffle the questions and the stimuli
    np.random.shuffle (questions) #Ask questions twice for each interested category, the left and right hand response keys will be swapped to avoid the effect of motor activity
    np.random.shuffle(stimuli_list_for_one_run) 
    
    
    #present stimuli for each block: for each block, question will be presented in advance for only once 
        #if the participant forget the question during this block, they can skip by pressing 'q', and skipped block can be check later
    
    for m in range(block_num):
        
        show_list_for_one_block = stimuli_list_for_one_run[m] #[stimuli,stimuli_index,category]*trail_num
        response_list_block = [] #[stimuli_index, category, response_key, correct/wrong, reaction_time,block_number]
        
        #question and response instructions given in advance
        questions[m].draw() #ask question
        win.flip()
        event.waitKeys(keyList = ('space'))
        
        correct_num = 0
        
        
            
        for n in show_list_for_one_block:
            
            
            image = visual.ImageStim(win, image = n[0], size = (500,500)) 
    
            cross.draw()
            win.flip()      
            core.wait(interval_time)
            
            image.draw()
            win.flip()
            
        
            #measure the reaction time for each response
            startTime = time.time()
            
            response = event.waitKeys(keyList = response_key)
            
            endTime = time.time()
            
            rt = endTime - startTime
            
          
            if 'q' in response: #detect 'q to skip this block
                used_q = 'skipped'
                break
                
              
                #[stimuli,stimuli_index,category]
            
            #faces
            if questions[m] == qfaces_f_j:
                
                used_q = 'qfaces_f_j'
                
                if 'f' in response and n[2] == 'faces':
                    evaluation = 'correct'
                elif 'j' in response and n[2] in ['bodies','scenes','objects']:
                    evaluation = 'correct'
                else:
                    evaluation = 'wrong'
            
            elif questions[m] == qfaces_j_f:
                used_q = 'qfaces_j_f'
                
                if 'j' in response and n[2] == 'faces':
                    evaluation = 'correct'
                elif 'f' in response and n[2] in ['bodies','scenes','objects']:
                    evaluation = 'correct'
                else:
                    evaluation = 'wrong'
            
            #bodies
            elif questions[m] == qbodies_f_j:
                used_q = 'qbodies_f_j'
                
                if 'f' in response and n[2] == 'bodies':
                    evaluation = 'correct'
                elif 'j' in response and n[2] in ['faces','scenes','objects']:
                    evaluation = 'correct'
                else:
                    evaluation = 'wrong'
            
            elif questions[m] == qbodies_j_f :
                used_q = 'qbodies_j_f'
                
                if 'j' in response and n[2] == 'bodies':
                    evaluation = 'correct'
                elif 'f' in response and n[2] in ['faces','scenes','objects']:
                    evaluation = 'correct'
                else:
                    evaluation = 'wrong'
            
            #scenes
            elif questions[m] == qscenes_f_j:
                used_q = 'qscenes_f_j'
                
                if 'f' in response and n[2] == 'scenes':
                    evaluation = 'correct'
                elif 'j' in response and n[2] in ['faces','bodies','objects']:
                    evaluation = 'correct'
                else:
                    evaluation = 'wrong'
            
            elif questions[m] == qscenes_j_f:
                used_q = 'qscenes_j_f'
                
                if 'j' in response and n[2] == 'scenes':
                    evaluation = 'correct'
                elif 'f' in response and n[2] in ['faces','bodies','objects']:
                    evaluation = 'correct'
                else:
                    evaluation = 'wrong'
            
  
             
            #give feedback if it is a practice session
            
            if is_practice == True:
                
                if evaluation == 'correct':
                    correct.draw()
                elif evaluation == 'wrong':
                    wrong.draw()
                
                win.flip()
                core.wait(feedback_time)
            
            #response_list=[stimuli_index, category,response, evaluation, reaction_time,block_number]
            response_list_block.append ([n[1], n[2], ''.join(response), evaluation, rt, str(m)])
            
            #calculating correct numbers for answer accuracy
            if evaluation == 'correct':
                correct_num = correct_num +1              
            else:
                correct_num = correct_num +0
                
    
        accuracy = (correct_num/trail_num)*100  
        
        #result_list = [response_list, accuracy, question_asked_for_this_block/skipped]
                       #response_list=[stimuli_index, category,response, evaluation, reaction_time,block_number]
        
        result_list.append([response_list_block,accuracy,used_q])
        
        if 'q' in response: #skip one block and continue the following blocks
            continue
                     
        #break time between blocks
        if m != (block_num -1) :
            rest.draw()
            win.flip()
            event.waitKeys(keyList = ('space'))
    
    return False



#settings for visuals 
win = visual.Window(size = (1440,900), fullscr = False, units = 'pix', color ='#BABAB9')

cross = visual.ImageStim(win, r'instructions/cross.png')
general_instructions = visual.ImageStim(win, r'instructions/general_instructions.png') #instruction for this experiment
practice_start = visual.ImageStim(win, r'instructions/practice_start.png') #instruction for practice
main_start = visual.ImageStim(win, r'instructions/formal_start.png') #instruction for offical experiment
run01_finish = visual.ImageStim(win, r'instructions/run1_end.png') #break time after finishing 1 run
run02_finish = visual.ImageStim(win, r'instructions/run2_end.png') #break time after finishing 2 run

#xxx_f_j: f = yes, j = now (left hand yes, right hand no)
#xxx_j_f: f = no, j = yes (left hand no, right hand yes)
qfaces_f_j = visual.ImageStim(win, r'instructions/qfaces_f_j.png')
qfaces_j_f = visual.ImageStim(win, r'instructions/qfaces_j_f.png')
qbodies_f_j = visual.ImageStim(win, r'instructions/qbodies_f_j.png')
qbodies_j_f = visual.ImageStim(win, r'instructions/qbodies_j_f.png')
qscenes_f_j = visual.ImageStim(win, r'instructions/qscenes_f_j.png')
qscenes_j_f = visual.ImageStim(win, r'instructions/qscenes_j_f.png')

questions = [qfaces_f_j,qfaces_j_f, qbodies_f_j,qbodies_j_f,qscenes_f_j,qscenes_j_f]


correct = visual.ImageStim(win, r'instructions/correct.png') #feedback if response is correct
wrong = visual.ImageStim(win, r'instructions/wrong.png') #feedback if response is wrong

rest = visual.ImageStim(win, r'instructions/break.png') #break time between each block
ending_text = visual.ImageStim(win, r'instructions/ending_text.png') #instruction when finished


#generate trial list for practice
practice_list = image_list(practice_stimuli, practice_block_num) 
#generate trial list for offcial experiement
main_list = image_list(qall, block_num)


#--------------start of the experiment----------------

#show general instruction
general_instructions.draw()
win.flip()
event.waitKeys(keyList = ('space'))


#start of practice 
evaluation = False

practice_start.draw()
win.flip()
event.waitKeys(keyList = ('space'))

practice_result = [] #[stimuli_index, category, response, evaluation, reaction_time, block_number]

#use the function to show stimulus
is_practice=True
showimage(practice_list, is_practice , practice_block_num, practice_trail_num, practice_result) 

#end of practice

#start of formal experiement
evaluation = False


main_start.draw()
win.flip()
event.waitKeys(keyList = ('space'))


#run_01

main_result01 = []  #[stimuli_index, category,response, evaluation, reaction_time,block_number]
is_practice=False
showimage(main_list, is_practice, block_num,trail_num, main_result01) 

#half_way info:
run01_finish.draw()
win.flip()
event.waitKeys(keyList = ('space'))


#run_02

evaluation = False
main_result02 = []  #[stimuli_index, category,response, evaluation, reaction_time,block_number]
is_practice=False
showimage(main_list, is_practice, block_num ,trail_num, main_result02) 

#half_way info:
run02_finish.draw()
win.flip()
event.waitKeys(keyList = ('space'))


#run_03
evaluation = False
main_result03 = []  #[stimuli_index, category,response, evaluation, reaction_time,block_num]
is_practice=False
showimage(main_list, is_practice, block_num ,trail_num, main_result03) 


#end of experiement
ending_text.draw()
win.flip()
event.waitKeys()

win.close()


#transform result of formal experiement to dataframe and save it
       
data = np.concatenate([main_result01[0][0],main_result01[1][0],main_result01[2][0],main_result01[3][0],main_result01[4][0],main_result01[5][0],main_result02[0][0],main_result02[1][0],main_result02[2][0],main_result02[3][0],main_result02[4][0],main_result02[5][0],main_result03[0][0],main_result03[1][0],main_result03[2][0],main_result03[3][0],main_result03[4][0],main_result03[5][0]],axis = 1)

data = pandas.DataFrame(data,columns = ['stimuli_index', 'category','response' ,'evaluation','reaction_time','block']*18)
                                        #[stimuli_index, category,response, evaluation, reaction_time,block_num]

#check mean accuracy for each participant
sum_accuracy =0

main_result = [main_result01,main_result02,main_result03]

general_result = []
for a in main_result:
    
    for x in a:
        sum_accuracy = sum_accuracy + x[1]
        
        general_result.append([x[1],x[2]])
    
    tot_accuracy =  + sum_accuracy
    
mean_accuracy = tot_accuracy/18

#add participant info

data.to_csv( r'experiment_data/' + str(info['ID']) +'_' +str(info['Gender']) +'_'  +str(info['Age'])+'_' + str(mean_accuracy) + '.csv')

data.to_excel( r'experiment_data/' + str(info['ID']) +'_' +str(info['Gender']) +'_'  +str(info['Age'])+'_' + '.xlsx')


#information for each block [accuracy, question_asked]

block_info = pandas.DataFrame(general_result,columns = ['accuracy', 'question_asked'])

block_info.to_csv( r'block_info/' + str(info['ID']) +'_' +str(info['Gender']) +'_'  +str(info['Age'])+'_' + str(mean_accuracy) + '.csv')












    
    