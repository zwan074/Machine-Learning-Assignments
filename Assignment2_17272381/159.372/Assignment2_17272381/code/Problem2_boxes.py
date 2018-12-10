from stripsProblem import Strips,STRIPS_domain,Planning_problem
from stripsForwardPlanner import Forward_STRIPS
from stripsRegressionPlanner import Regression_STRIPS
from searchMPP import SearcherMPP


def room (x,y):
    return 'room_('+ str(x) +','+ str(y) + ')'

def push_box1_right (row,col,box2_row,box2_col):
    return 'Rob_push_box1_rigt'  + '_from_room_(' + str(row) + ',' + str(col) + ')_to_room_(' +\
        str(row) + ',' + str(col+1) +')_and_' + 'Rob_move_right_from_room_(' + str(row)  + ',' +\
        str(col-1) + ')_to_room_(' + str(row)  + ',' +str(col) + ')' + '_box2_is_at_(' +\
        str(box2_row) + ',' +str(box2_col) + ')' 

def push_box1_left (row,col,box2_row,box2_col):
    return 'Rob_push_box1_left'  + '_from_room_(' + str(row) + ',' + str(col) + ')_to_room_(' +\
        str(row) + ',' + str(col-1) +')_and_' + 'Rob_move_left_from_room_(' + str(row)  + ',' +\
        str(col+1) + ')_to_room_(' + str(row)  + ',' +str(col) + ')' + '_box2_is_at_(' +\
        str(box2_row) + ',' +str(box2_col) + ')' 

def push_box1_up (row,col,box2_row,box2_col):
    return 'Rob_push_box1_up'  + '_from_room_(' + str(row) + ',' + str(col) + ')_to_room_(' +\
        str(row-1) + ',' + str(col) +')_and_' + 'Rob_move_up_from_room_(' + str(row+1)  + ',' +\
        str(col) + ')_to_room_(' + str(row)  + ',' +str(col) + ')' + '_box2_is_at_(' +\
        str(box2_row) + ',' +str(box2_col) + ')' 

def push_box1_down (row,col,box2_row,box2_col):
    return 'Rob_push_box1_down'  + '_from_room_(' + str(row) + ',' + str(col) + ')_to_room_(' +\
        str(row+1) + ',' + str(col) +')_and_' + 'Rob_move_down_from_room_(' + str(row-1)  + ',' +\
        str(col) + ')_to_room_(' + str(row)  + ',' +str(col) + ')' + '_box2_is_at_(' +\
        str(box2_row) + ',' +str(box2_col) + ')' 

def push_box2_right (row,col,box1_row,box1_col):
    return 'Rob_push_box2_right'  + '_from_room_(' + str(row) + ',' + str(col) + ')_to_room_(' +\
        str(row) + ',' + str(col+1) +')_and_' + 'Rob_move_right_from_room_(' + str(row)  + ',' +\
        str(col-1) + ')_to_room_(' + str(row)  + ',' +str(col) + ')' + '_box1_is_at_(' +\
        str(box1_row) + ',' +str(box1_col) + ')' 

def push_box2_left (row,col,box1_row,box1_col):
    return 'Rob_push_box2_left'  + '_from_room_(' + str(row) + ',' + str(col) + ')_to_room_(' +\
        str(row) + ',' + str(col-1) +')_and_' + 'Rob_move_left_from_room_(' + str(row)  + ',' +\
        str(col+1) + ')_to_room_(' + str(row)  + ',' +str(col) + ')' + '_box1_is_at_(' +\
        str(box1_row) + ',' +str(box1_col) + ')' 

def push_box2_up (row,col,box1_row,box1_col):
    return 'Rob_push_box2_up'  + '_from_room_(' + str(row) + ',' + str(col) + ')_to_room_(' +\
        str(row-1) + ',' + str(col) +')_and_' + 'Rob_move_up_from_room_(' + str(row+1)  + ',' +\
        str(col) + ')_to_room_(' + str(row)  + ',' +str(col) + ')' + '_box1_is_at_(' +\
        str(box1_row) + ',' +str(box1_col) + ')' 

def push_box2_down (row,col,box1_row,box1_col):
    return 'Rob_push_box2_down'  + '_from_room_(' + str(row) + ',' + str(col) + ')_to_room_(' +\
        str(row+1) + ',' + str(col) +')_and_' + 'Rob_move_down_from_room_(' + str(row-1)  + ',' +\
        str(col) + ')_to_room_(' + str(row)  + ',' +str(col) + ')' + '_box1_is_at_(' +\
        str(box1_row) + ',' +str(box1_col) + ')' 

def mov_Rob (from_x,from_y,to_x,to_y, box1_row,box1_col,box2_row,box2_col):
    return 'Rob_move_from_room_(' + str(from_x) + ',' + str(from_y) + ')_to_room_(' +\
        str(to_x) + ',' + str(to_y) +')_and_box1_at_room_(' + str(box1_row) + ',' +\
        str(box1_col) + ')'+ '_box2_at_(' + str(box2_row) + ',' +str(box2_col) + ')' 

def create_strips_domain(x,y):
    
    #features
    #Rob Box1, Box2 features 
    feats_vals = { 'Rob' : { room(row,col) for row in range(x) for col in range(y)},
                   'Box1' : { room(row,col) for row in range(x) for col in range(y)},
                   'Box2' : { room(row,col) for row in range(x) for col in range(y)},
                   }
    #actions
    #Rob move box1 right left up down
    smap_box1_right = { push_box1_right (row,col,box2_row,box2_col):
                        Strips ( {'Rob': room (row,col-1) , 'Box1': room (row,col) , 'Box2': room(box2_row,box2_col) },
                        {'Rob': room (row,col)  ,  'Box1': room (row,col+1), 'Box2': room(box2_row,box2_col)  })
                        for row in range (x)
                        for col in range (1,y-1)
                        for box2_row in range(x)
                        for box2_col in range(y)
                        if not (box2_row == row and box2_col == col+1) and not (box2_row == row and box2_col == col)
                        and not (box2_row == row and box2_col == col-1)}

    smap_box1_left = {  push_box1_left (row,col,box2_row,box2_col):
                        Strips ( {'Rob': room (row,col+1)  ,'Box1' : room (row,col), 'Box2': room(box2_row,box2_col) },
                                 {'Rob' : room (row,col),   'Box1': room(row,col-1) , 'Box2': room(box2_row,box2_col)  })
                        for row in range (x)
                        for col in range (1,y-1)
                        for box2_row in range(x)
                        for box2_col in range(y)
                        if not (box2_row == row and box2_col == col+1) and not (box2_row == row and box2_col == col)
                        and not (box2_row == row and box2_col == col-1)}

    smap_box1_up = { push_box1_up (row,col,box2_row,box2_col):
                     Strips ( {'Rob': room (row+1,col)  , 'Box1' : room (row,col) , 'Box2': room(box2_row,box2_col) },
                          {'Rob': room (row,col), 'Box1': room(row-1,col), 'Box2': room(box2_row,box2_col) })
                     for row in range (1,x-1)
                     for col in range (y)
                     for box2_row in range(x)
                     for box2_col in range(y)
                     if not (box2_row == row+1 and box2_col == col) and not (box2_row == row and box2_col == col)
                     and not (box2_row == row-1 and box2_col == col)}

    smap_box1_down = { push_box1_down (row,col,box2_row,box2_col): 
                       Strips ( {'Rob': room (row-1,col)  , 'Box1' : room (row,col), 'Box2': room(box2_row,box2_col)  },
                                {'Rob': room (row,col), 'Box1': room(row+1,col), 'Box2': room(box2_row,box2_col) })
                        for row in range (1,x-1)
                        for col in range (y)
                        for box2_row in range(x)
                        for box2_col in range(y)
                        if not (box2_row == row+1 and box2_col == col) and not (box2_row == row and box2_col == col)
                        and not (box2_row == row-1 and box2_col == col)}
    #Rob move box2 right left up down
    smap_box2_right = { push_box2_right (row,col,box1_row,box1_col): 
                        Strips ( {'Rob': room (row,col-1) , 'Box2': room (row,col) , 'Box1': room(box1_row,box1_col) },
                                 {'Rob': room (row,col)  ,  'Box2': room (row,col+1),'Box1': room(box1_row,box1_col)  })
                        for row in range (x)
                        for col in range (1,y-1)
                        for box1_row in range(x)
                        for box1_col in range(y)
                        if not (box1_row == row and box1_col == col+1) and not (box1_row == row and box1_col == col)
                        and not (box1_row == row and box1_col == col-1)}

    smap_box2_left = { push_box2_left (row,col,box1_row,box1_col): 
                       Strips ( {'Rob': room (row,col+1)  ,'Box2' : room (row,col),  'Box1': room(box1_row,box1_col)},
                                {'Rob' : room (row,col),   'Box2': room(row,col-1) , 'Box1': room(box1_row,box1_col)  })
                        for row in range (x)
                        for col in range (1,y-1)
                        for box1_row in range(x)
                        for box1_col in range(y)
                        if not (box1_row == row and box1_col == col+1) and not (box1_row == row and box1_col == col)
                        and not (box1_row == row and box1_col == col-1)}

    smap_box2_up = { push_box2_up (row,col,box1_row,box1_col): 
                     Strips ( {'Rob': room (row+1,col)  , 'Box2' : room (row,col) , 'Box1': room(box1_row,box1_col) },
                              {'Rob': room (row,col), 'Box2': room(row-1,col), 'Box1': room(box1_row,box1_col) })
                     for row in range (1,x-1)
                     for col in range (y)
                     for box1_row in range(x)
                     for box1_col in range(y)
                     if not (box1_row == row+1 and box1_col == col) and not (box1_row == row and box1_col == col)
                     and not (box1_row == row-1 and box1_col == col)}

    smap_box2_down = { push_box2_down (row,col,box1_row,box1_col): 
                       Strips ( {'Rob': room (row-1,col)  , 'Box2' : room (row,col),  'Box1': room(box1_row,box1_col)  },
                                {'Rob': room (row,col), 'Box2': room(row+1,col),  'Box1': room(box1_row,box1_col) })
                                   for row in range (1,x-1)
                                   for col in range (y)
                                   for box1_row in range(x)
                                   for box1_col in range(y)
                                   if not (box1_row == row+1 and box1_col == col) and not (box1_row == row and box1_col == col)\
                                   and not (box1_row == row-1 and box1_col == col)}
    
    #Rob move itselft right left up down 
    smap_Rob_right = { mov_Rob (row,col,row,col+1,box1_row,box1_col,box2_row,box2_col): 
                       Strips ( {'Rob': room (row,col), 'Box1' : room (box1_row,box1_col) , 'Box2' : room (box2_row,box2_col) },
                                {'Rob': room (row,col+1),'Box1' : room (box1_row,box1_col),'Box2' : room (box2_row,box2_col) })
                                for row in range (x)
                                for col in range (y-1)
                                for box1_row in range(x)
                                for box1_col in range(y)
                                for box2_row in range(x)
                                for box2_col in range(y)
                                if not (box1_row == row and box1_col == col+1) and not (box1_row == row and box1_col == col) 
                                and not (box2_row == row and box2_col == col+1) and not (box2_row == row and box2_col == col)
                                and not (box1_row == box2_row and box1_col == box2_col)  }

    smap_Rob_left= {mov_Rob (row,col,row,col-1,box1_row,box1_col,box2_row,box2_col): 
                    Strips ( {'Rob': room (row,col), 'Box1' : room (box1_row,box1_col) , 'Box2' : room (box2_row,box2_col)},
                             {'Rob': room (row,col-1),'Box1' : room (box1_row,box1_col) , 'Box2' : room (box2_row,box2_col)})
                            for row in range (x)
                            for col in range (1,y)
                            for box1_row in range(x)
                            for box1_col in range(y)
                            for box2_row in range(x)
                            for box2_col in range(y)
                            if not (box1_row == row and box1_col == col-1) and not (box1_row == row and box1_col == col) 
                            and not (box2_row == row and box2_col == col-1) and not (box2_row == row and box2_col == col)
                            and not (box1_row == box2_row and box1_col == box2_col) }

    smap_Rob_up= { mov_Rob (row,col,row-1,col,box1_row,box1_col,box2_row,box2_col): 
                   Strips ( {'Rob': room (row,col), 'Box1' : room (box1_row,box1_col) , 'Box2' : room (box2_row,box2_col) },
                            {'Rob': room (row-1,col), 'Box1' : room (box1_row,box1_col) , 'Box2' : room (box2_row,box2_col) })
                            for row in range (1,x)
                            for col in range (y)
                            for box1_row in range(x)
                            for box1_col in range(y)
                            for box2_row in range(x)
                            for box2_col in range(y)
                            if not (box1_row == row-1 and box1_col == col) and not (box1_row == row and box1_col == col) 
                            and not (box2_row == row-1 and box2_col == col) and not (box2_row == row and box2_col == col)
                            and not (box1_row == box2_row and box1_col == box2_col)}

                                                             
    smap_Rob_down= { mov_Rob (row,col,row+1,col,box1_row,box1_col,box2_row,box2_col): 
                     Strips ( {'Rob': room (row,col), 'Box1' : room (box1_row,box1_col) , 'Box2' : room (box2_row,box2_col)},
                              {'Rob': room (row+1,col),'Box1' : room (box1_row,box1_col) , 'Box2' : room (box2_row,box2_col)})
                                for row in range (x-1)
                                for col in range (y)
                                for box1_row in range(x)
                                for box1_col in range(y)
                                for box2_row in range(x)
                                for box2_col in range(y)
                                if not (box1_row == row+1 and box1_col == col) and not (box1_row == row and box1_col == col) 
                                and not (box2_row == row+1 and box2_col == col) and not (box2_row == row and box2_col == col)
                                and not (box1_row == box2_row and box1_col == box2_col)}
    
    #combine all stirp maps
    smap = {}
    
    smap.update(smap_box1_right)
    smap.update(smap_box1_left)
    smap.update(smap_box1_up)
    smap.update(smap_box1_down)
    
    smap.update(smap_box2_right)
    smap.update(smap_box2_left)
    smap.update(smap_box2_up)
    smap.update(smap_box2_down)
    
    smap.update(smap_Rob_right)
    smap.update(smap_Rob_left) 
    smap.update(smap_Rob_up)
    smap.update(smap_Rob_down)
    
    return STRIPS_domain(feats_vals, smap)


domain = create_strips_domain(4,4)

case1 = Planning_problem(domain,
                        { 'Rob' : room(0,0), 'Box1':room(1,1),'Box2':room(3,2)  },
                        { 'Rob' : room(0,0), 'Box1':room(0,3),'Box2':room(2,3)  })
case1_solution1 = SearcherMPP(Forward_STRIPS(case1)).search() 
case1_solution2 = SearcherMPP(Regression_STRIPS(case1)).search() 

print('---------')
print('case1 forward planner solution:')
print(case1_solution1)
print('---------')
print('case1 regression planner solution:')
print(case1_solution2)
print('---------')

case2 = Planning_problem(domain,
                        { 'Rob' : room(0,0), 'Box1':room(1,1),'Box2':room(2,2)  },
                        { 'Rob' : room(0,0), 'Box1':room(2,2),'Box2':room(3,3)  })

case2_solution1 = SearcherMPP(Forward_STRIPS(case2)).search() 
case2_solution2 = SearcherMPP(Regression_STRIPS(case2)).search() 

print('---------')
print('case2 forward planner solution:')
print(case2_solution1)
print('---------')
print('case2 regression planner solution:')
print(case2_solution2)
print('---------')



case3 = Planning_problem(domain,
                        { 'Rob' : room(0,0), 'Box1':room(1,1),'Box2':room(2,2)  },
                        { 'Rob' : room(0,0), 'Box1':room(0,1),'Box2':room(3,0)  })
case3_solution1 = SearcherMPP(Forward_STRIPS(case3)).search() 
case3_solution2 = SearcherMPP(Regression_STRIPS(case3)).search() 
 
print('---------')
print('case3 forward planner solution:')
print(case3_solution1)
print('---------')
print('case3 regression planner solution:')
print(case3_solution2)
print('---------')