from .models import PaymentsControl, DepositControl

# CASH OUTFLOW CONTROL(PAYMENT AND WITHDRAWAL)
def get_min_balance():
    try:
        return PaymentsControl.objects.get(id=1).min_balance 
    except:
        return 0

def get_max_receiver_balance():
    try:
        return PaymentsControl.objects.get(id=1).max_receiver_balance 
    except:
        return 2000

def get_min_transfer():
    try:
        return PaymentsControl.objects.get(id=1).min_transfer 
    except:
        return 20

def get_max_transfer():
    try:
        return PaymentsControl.objects.get(id=1).max_transfer 
    except:
        return 500

def get_min_withdrawal():
    try:
        return PaymentsControl.objects.get(id=1).min_withdrawal 
    except:
        return 20

def get_max_withdrawal():
    try:
        return PaymentsControl.objects.get(id=1).max_withdrawal 
    except:
        return 500


# CASH INFLOW CONTROL(DEPOSIT)

def get_min_depositor_balance():
    try:
        return DepositControl.objects.get(id=1).min_balance 
    except:
        return 0

def get_max_depositor_balance():
    try:
        return DepositControl.objects.get(id=1).max_balance 
    except:
        return 2000

def get_min_deposit():
    try:
        return DepositControl.objects.get(id=1).min_deposit 
    except:
        return 20

def get_max_deposit():
    try:
        return DepositControl.objects.get(id=1).max_deposit 
    except:
        return 500

















































