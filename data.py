Users = [
    {'id':1, 'name':"Saksham", 'role':"farmer"},
    {'id':2, 'name':"Tharun", 'role':"inputter"},
    {'id':3, 'name':"Priya", 'role':"processor"},
    {'id':4, 'name':"Ramesh", 'role':"distributor"},
    {'id':5, 'name':"Anita", 'role':"farmer"},
    {'id':6, 'name':"Vikram", 'role':"inputter"},
    {'id':7, 'name':"Lakshmi", 'role':"processor"},
    {'id':8, 'name':"Kiran", 'role':"distributor"}
]

Items = [
    {'id':100, 'name':'banana', 'type':'fruit'},
    {'id':101, 'name':'apple', 'type':'fruit'},
    {'id':102, 'name':'seed', 'type':'raw'},
    {'id':103, 'name':'wheat', 'type':'grain'},
    {'id':104, 'name':'rice', 'type':'grain'},
    {'id':105, 'name':'tomato', 'type':'vegetable'},
    {'id':106, 'name':'potato', 'type':'vegetable'},
    {'id':107, 'name':'fertilizer', 'type':'input'},
    {'id':108, 'name':'pesticide', 'type':'input'}
]

Transit = [
    {'batch_no': "BCH-ABC-001", 'user_from': 2, 'user_to': 1, 'item':102, 'qty':10},
    {'batch_no': "BCH-ABC-002", 'user_from': 6, 'user_to': 3, 'item':107, 'qty':50},
    {'batch_no': "BCH-ABC-003", 'user_from': 4, 'user_to': 5, 'item':100, 'qty':200},
    {'batch_no': "BCH-ABC-004", 'user_from': 2, 'user_to': 7, 'item':101, 'qty':75},
    {'batch_no': "BCH-ABC-005", 'user_from': 8, 'user_to': 1, 'item':103, 'qty':300},
    {'batch_no': "BCH-ABC-006", 'user_from': 6, 'user_to': 4, 'item':105, 'qty':120}
]

Inventory = [
    {'user_id':1, 'item':100, 'qty':4, 'batch_no':"BCH-ABX-001"},
    {'user_id':1, 'item':102, 'qty':15, 'batch_no':"BCH-ABX-002"},
    {'user_id':3, 'item':107, 'qty':80, 'batch_no':"BCH-ABX-003"},
    {'user_id':5, 'item':100, 'qty':250, 'batch_no':"BCH-ABX-004"},
    {'user_id':7, 'item':101, 'qty':60, 'batch_no':"BCH-ABX-005"},
    {'user_id':4, 'item':103, 'qty':400, 'batch_no':"BCH-ABX-006"},
    {'user_id':2, 'item':102, 'qty':25, 'batch_no':"BCH-ABX-007"}
]
