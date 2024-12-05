from enum import Enum

class Priority(Enum):
    MEAL="MEAL"
    DRINK="DRINK"

class UserRole(Enum):
    ADMIN=1
    FINANCIAL_MANAGER =2
    WAITER= 3

class UserFeatures(Enum):
    RESTAURANT_MANAGER = 1
    MENU_MANAGER = 2
    MENU_ITEM_MANAGER = 3
    TABLE_MANAGER = 4
    EMPLOYEES = 5
    FINANCIAL_REPORTS = 6
    EXPENSE_TRACKING = 7
    PAYROLLS = 8
    ACCOUNTS = 9
    TAKE_ORDERS = 10
    CUSTOMER_SERVICE = 11
    BILLING = 12
    SIGN_OUT =13




