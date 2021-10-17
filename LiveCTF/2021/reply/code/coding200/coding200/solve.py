from Utils.thread_manager import *
import queue
from functools import reduce

r = queue.Queue()
pz_tot = []

def runner_find_bottom(pz):
    sol = []
    global pz_tot

    pz_directions = {p:{'down':[],'up':[],'left':[],'right':[]} for p in pz}

    #print(len(pz))
    for i in range(len(pz)):
        p = pz[i]
        p_up=p.split()[0]
        p_down=p.split()[1]
        p_left=p.split()[2]
        p_right=p.split()[3] 

        # p
        #print('p={}'.format(p))
        print(i,end='\r')
        for p1 in pz:
            if p1==p:continue
            #print('p1={}'.format(p1))
            p1_up=p1.split()[0]
            p1_down=p1.split()[1]
            p1_left=p1.split()[2]
            p1_right=p1.split()[3]

            if p1_up==p_down: 
                #pz_directions[p1]['up']+=[p]
                pz_directions[p]['down']+=[p1]
            
            if p1_down==p_up: 
                #pz_directions[p1]['down']+=[p]
                pz_directions[p]['up']+=[p1]
            if p1_left == p_right:
                #pz_directions[p1]['left']+=[p]
                pz_directions[p]['right']+=[p1]

            if p1_right == p_left:
                #pz_directions[p1]['right']+=[p]
                pz_directions[p]['left']+=[p1]


        '''
            if len(pz_directions[p]['up'])==0:
                print('no up: {}'.format(p))
                c+=1
            1,2
        '''
        
        if(len(pz_directions[p]['down']))==0:
            if len(pz_directions[p]['left'])==0:
                #print('no left: {}'.format(p))
                c+=1
                return p


def find_left(pz_tot,bl):
    sol=''
    for p in pz_tot:
        if p.split()[-1]==bl.split()[-2]:
            sol=p
            break
    return sol   

def get_raw(pz_tot,bl):
    sol=[]
    sol+=[bl]
    for i in range(199):
        sol+=[find_left(pz_tot,sol[-1])]
    return sol


if __name__=='__main__':

    pz=[]
    with open('puzzle.txt','r') as f:
    	pz=f.readlines()	

    pz_tot=[l.strip() for l in pz[7:]]

    w_dict = {' '.join(l.split()[:-1]):l.split()[-1] for l in pz if len(l.split()[-1])==1} 
    
    #print(pz)
    pz_tot = [' '.join(l.split()) if len(l.split())==4 else ' '.join(l.split()[:-1]) for l in pz_tot]
    #print(pz)





    bl = '33377 144930 30654 115414' # leftmost identified

    sol = []
    
    for i in range(200):
        print(i)
        sol+=[get_raw(pz_tot,bl)]
        #print(sol[-1])

        for p in pz_tot:
            if p.split()[1]==bl.split()[0]:
                bl=p
                break

        pz_tot = [p for p in pz_tot if p not in sol[-1]]
    
    #RPZwJYegNTPHjNQEALlFigcYxqhDBWVP

    for i in sol[::-1]:
        for p in i[::-1]:
            if p in w_dict.keys():
                print(w_dict[p], end='')










