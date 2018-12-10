from stripsProblem import Strips,STRIPS_domain,Planning_problem
from stripsForwardPlanner import Forward_STRIPS
from stripsRegressionPlanner import Regression_STRIPS
from searchMPP import SearcherMPP


boolean = {True, False}
domain = STRIPS_domain(
    #features
    {'T_IDLE': {'T1','T2','T3','T1_T2','T1_T3','T2_T3','T1_T2_T3'},
     'FREE_SOCKET_T1':boolean,'T1_CONNECTTED' : boolean, 'REQUEST_SENT_FROM_T1': boolean, 'RESPONSE_SENT_TO_T1': boolean,
     'FREE_SOCKET_T2':boolean,'T2_CONNECTTED' : boolean, 'REQUEST_SENT_FROM_T2': boolean, 'RESPONSE_SENT_TO_T2': boolean,
     'FREE_SOCKET_T3':boolean,'T3_CONNECTTED' : boolean, 'REQUEST_SENT_FROM_T3': boolean, 'RESPONSE_SENT_TO_T3': boolean,
    'SERVER_LISTENING': boolean },
    
    #actions
    {'insert_bank_card_in_T1':Strips({'T_IDLE': 'T1'},
                                     {'FREE_SOCKET_T1': True,'T1_IDLE': False,'SERVER_LISTENING': True }),
     'insert_bank_card_in_T2':Strips({'T_IDLE': 'T2'},
                                     {'FREE_SOCKET_T2': True,'T2_IDLE': False,'SERVER_LISTENING': True }),
     'insert_bank_card_in_T3':Strips({'T_IDLE': 'T3'},
                                     {'FREE_SOCKET_T3': True,'T3_IDLE': False,'SERVER_LISTENING': True }),
     
     'insert_bank_card_in_T1_&_T2':Strips({'T_IDLE': 'T1_T2'},
                                    {'FREE_SOCKET_T1': True,'FREE_SOCKET_T2': True,'SERVER_LISTENING': True }),
     'insert_bank_card_in_T1_&_T3':Strips({'T_IDLE': 'T1_T3'},
                                    {'FREE_SOCKET_T1': True,'FREE_SOCKET_T3': True,'SERVER_LISTENING': True }),
     'insert_bank_card_in_T2_&_T3':Strips({'T_IDLE': 'T2_T3'},
                                    {'FREE_SOCKET_T2': True,'FREE_SOCKET_T3': True,'SERVER_LISTENING': True }),
     
     'insert_bank_card_in_T1_&_T2_&_T3':Strips({'T_IDLE': 'T1_T2_T3'},
                                    {'FREE_SOCKET_T1': True,'FREE_SOCKET_T2': True,'FREE_SOCKET_T3': True,
                                     'SERVER_LISTENING': True }),
   
     'server_connect_T1':Strips({'SERVER_LISTENING': True, 'FREE_SOCKET_T1': True },{'T1_CONNECTTED': True }),
     'server_process_withdraw_cash_request_from_T1':Strips({'T1_CONNECTTED': True },{'REQUEST_SENT_FROM_T1': True }),
     'cash_pop_out_from_T1':Strips({'REQUEST_SENT_FROM_T1': True },{'RESPONSE_SENT_TO_T1': True }),
     'close_T1_connection': Strips ({'RESPONSE_SENT_TO_T1': True  },
                                    {'T1_CONNECTTED' : False,'SERVER_LISTENING': False,'FREE_SOCKET_T1': False  }),
     
     'server_connect_T2':Strips({'SERVER_LISTENING': True, 'FREE_SOCKET_T2': True },{'T2_CONNECTTED': True }),
     'server_process_withdraw_cash_request_from_T2':Strips({'T2_CONNECTTED': True },{'REQUEST_SENT_FROM_T2': True }),
     'cash_pop_out_from_T2':Strips({'REQUEST_SENT_FROM_T2': True },{'RESPONSE_SENT_TO_T2': True}),
     'close_T2_connection': Strips ({'RESPONSE_SENT_TO_T2': True  },
                                    {'T2_CONNECTTED' : False,'SERVER_LISTENING': False,'FREE_SOCKET_T2': False }),
     
     'server_connect_T3':Strips({'SERVER_LISTENING': True, 'FREE_SOCKET_T3': True },{'T3_CONNECTTED': True }),
     'server_process_withdraw_cash_request_from_T3':Strips({'T3_CONNECTTED': True },{'REQUEST_SENT_FROM_T3': True }),
     'cash_pop_out_from_T3':Strips({'REQUEST_SENT_FROM_T3': True },{'RESPONSE_SENT_TO_T3': True}),
     'close_T3_connection': Strips ({'RESPONSE_SENT_TO_T3': True  },
                                    {'T3_CONNECTTED' : False,'SERVER_LISTENING': False,'FREE_SOCKET_T3': False }),
                            
     }
   
    )

case1 = Planning_problem(domain,
                            {'T_IDLE': 'T1'},
                            {'RESPONSE_SENT_TO_T1':True,'T1_CONNECTTED' : False })

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
                            {'T_IDLE': 'T2_T3'},
                            {'RESPONSE_SENT_TO_T3':True, 'RESPONSE_SENT_TO_T2':True,
                             'T3_CONNECTTED' : False,'T2_CONNECTTED' : False })

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
                            {'T_IDLE': 'T1_T2_T3'},
                            {'RESPONSE_SENT_TO_T1':True, 'RESPONSE_SENT_TO_T2':True, 'RESPONSE_SENT_TO_T3':True,
                             'T1_CONNECTTED' : False,'T2_CONNECTTED' : False,'T3_CONNECTTED' : False})

case3_solution1 = SearcherMPP(Forward_STRIPS(case3)).search() 
case3_solution2 = SearcherMPP(Regression_STRIPS(case3)).search() 

print('---------')
print('case3 forward planner solution:')
print(case3_solution1)
print('---------')
print('case3 regression planner solution:')
print(case3_solution2)
print('---------')