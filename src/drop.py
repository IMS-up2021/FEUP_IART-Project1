def move(fr, to):
    
    return 0

def split(photon):
    
    return 0

def check_can_move(fr, to): #can move to space (empty and connected)
    
    return 0

def check_can_merge(fr, to): #can merge color
    
    return 0

def check_win(state, goal):
    return state == goal
    
def main():
    state = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    photon = {
                'red':[{'green':'moregreen', 'blue':'purple', 'cyan':'cyan'}, {'green':'yellow', 'blue':'purple'}, []],
                'white':[0, 0, ['red', 'green', 'blue']],
                'blue':[{'red':'violet', 'green':'aqua_green', 'yellow':'light_yellow'}, {'green':'cyan', 'red':'purple'}, []],
                'green':[{'red':'orange', 'blue':'blue_sky', 'purple':'pink'}, {'red':'yellow', 'blue':'cyan'}, []],
                'cyan':[{'red':'beige'},{'red':'white'},['blue', 'green']],
                'yellow':[{'blue':'light_blue'},{'blue':'white'},['red', 'green']],
                'purple':[{'green':'light_green'},{'green':'white'},['red', 'blue']]
    } #{photon:[{pigment:mix}, {photon:mix}, [splits]]}
    
    goal = []
    
    nodes = {0:[2,3,5], 1:[2,4,6], 2:[1,2,4,5], 3:[0,2,5], } #node1 -> node2, node2 -> node1
    
    
    max_mov = 9
    return 0
    