users = [
    {'id':1, 'name':"Saksham", 'role':"producer"},
    {'id':2, 'name':"Tharun", 'role':"supplier"},
    {'id':3, 'name':"Priya", 'role':"processor"},
    {'id':4, 'name':"Ramesh", 'role':"distributor"},
    {'id':5, 'name':"Anita", 'role':"producer"},
    {'id':6, 'name':"Vikram", 'role':"supplier"},
    {'id':7, 'name':"Lakshmi", 'role':"processor"},
    {'id':8, 'name':"Kiran", 'role':"distributor"}
]

items = [
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

from datetime import datetime

transit = [
    {
        'batch_no': "BCH-ABC-001",
        'user_from': 2,
        'user_to': 1,
        'item': 102,
        'qty': 10,
        'status': "delivered",
        'tracking_number': "TRK001",
        'expected_delivery': "2026-03-01",
        'placed_at': datetime(2026, 2, 20, 10, 30),
        'dispatched_at': datetime(2026, 2, 21, 9, 0),
        'delivered_at': datetime(2026, 2, 23, 14, 15)
    },
    {
        'batch_no': "BCH-ABC-002",
        'user_from': 6,
        'user_to': 3,
        'item': 107,
        'qty': 50,
        'status': "in_transit",
        'tracking_number': "TRK002",
        'expected_delivery': "2026-03-03",
        'placed_at': datetime(2026, 2, 22, 11, 45),
        'dispatched_at': datetime(2026, 2, 23, 8, 30),
        'delivered_at': None
    },
    {
        'batch_no': "BCH-ABC-003",
        'user_from': 4,
        'user_to': 5,
        'item': 100,
        'qty': 200,
        'status': "packaging",
        'tracking_number': None,
        'expected_delivery': "2026-03-05",
        'placed_at': datetime(2026, 2, 25, 16, 10),
        'dispatched_at': None,
        'delivered_at': None
    },
    {
        'batch_no': "BCH-ABC-004",
        'user_from': 2,
        'user_to': 7,
        'item': 101,
        'qty': 75,
        'status': "shipping",
        'tracking_number': "TRK004",
        'expected_delivery': "2026-03-04",
        'placed_at': datetime(2026, 2, 24, 13, 0),
        'dispatched_at': datetime(2026, 2, 25, 7, 45),
        'delivered_at': None
    },
    {
        'batch_no': "BCH-ABC-005",
        'user_from': 8,
        'user_to': 1,
        'item': 103,
        'qty': 300,
        'status': "delivered",
        'tracking_number': "TRK005",
        'expected_delivery': "2026-03-02",
        'placed_at': datetime(2026, 2, 19, 9, 20),
        'dispatched_at': datetime(2026, 2, 20, 10, 0),
        'delivered_at': datetime(2026, 2, 22, 18, 40)
    },
    {
        'batch_no': "BCH-ABC-006",
        'user_from': 6,
        'user_to': 4,
        'item': 105,
        'qty': 120,
        'status': "cancelled",
        'tracking_number': None,
        'expected_delivery': "2026-03-06",
        'placed_at': datetime(2026, 2, 26, 14, 30),
        'dispatched_at': None,
        'delivered_at': None
    }
]

inventory = [
    {'user_id':1, 'item':100, 'qty':4, 'batch_no':"BCH-ABX-001"},
    {'user_id':1, 'item':102, 'qty':15, 'batch_no':"BCH-ABX-002"},
    {'user_id':3, 'item':107, 'qty':80, 'batch_no':"BCH-ABX-003"},
    {'user_id':5, 'item':100, 'qty':250, 'batch_no':"BCH-ABX-004"},
    {'user_id':7, 'item':101, 'qty':60, 'batch_no':"BCH-ABX-005"},
    {'user_id':4, 'item':103, 'qty':400, 'batch_no':"BCH-ABX-006"},
    {'user_id':2, 'item':102, 'qty':25, 'batch_no':"BCH-ABX-007"}
]