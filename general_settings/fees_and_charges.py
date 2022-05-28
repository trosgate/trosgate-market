from .models import HiringFee


# CONTRACT FEES AND CHARGES STARTS

def get_contract_fee_percentage():
    try:
        return HiringFee.objects.get(id=1).contract_fee_percentage
    except:
        return 0

def get_contract_fee_extra():
    try:
        return HiringFee.objects.get(id=1).contract_fee_fixed
    except:
        return 0

def get_contract_delta_amount():
    try:
        return HiringFee.objects.get(id=1).contract_delta_amount
    except:
        return 0

def get_contract_fee_calculator(amount):
    contract_total_fee = 0
    contract_fee = 0

    if (0 <= amount <= get_contract_delta_amount()):
        contract_total_fee = ((amount * get_contract_fee_percentage())/100)

    elif (amount > get_contract_delta_amount()):
        contract_fee = ((get_contract_delta_amount() * get_contract_fee_percentage())/100)
        contract_total_fee = contract_fee + get_contract_fee_extra()

    contract_grand_total_fee = round(contract_total_fee)
    return contract_grand_total_fee


# PROPOSAL FEES AND CHARGES STARTS

def get_proposal_fee_percentage():
    try:
        return HiringFee.objects.get(id=1).proposal_fee_percentage
    except:
        return 0

def get_proposal_fee_extra():
    try:
        return HiringFee.objects.get(id=1).proposal_fee_fixed
    except:
        return 0

def get_proposal_delta_amount():
    try:
        return HiringFee.objects.get(id=1).proposal_delta_amount
    except:
        return 0


def get_proposal_fee_calculator(amount):
    proposal_total_fee = 0
    proposal_fee = 0

    if (0 <= amount <= get_proposal_delta_amount()):
        proposal_total_fee = ((amount * get_proposal_fee_percentage())/100)

    elif (amount > get_proposal_delta_amount()):
        proposal_fee = ((get_proposal_delta_amount() * get_proposal_fee_percentage())/100)
        proposal_total_fee = proposal_fee + get_proposal_fee_extra()

    contract_grand_total_fee = round(proposal_total_fee)
    return contract_grand_total_fee

# APPLICATION FEES AND CHARGES STARTS

def get_application_fee_percentage():
    try:
        return HiringFee.objects.get(id=1).application_fee_percentage
    except:
        return 0


def get_application_fee_extra():
    try:
        return HiringFee.objects.get(id=1).application_fee_fixed
    except:
        return 0


def get_application_delta_amount():
    try:
        return HiringFee.objects.get(id=1).application_delta_amount
    except:
        return 0


def get_application_fee_calculator(amount):
    application_total_fee = 0
    application_fee = 0

    if (0 <= amount <= get_application_delta_amount()):
        application_total_fee =  ((amount * get_application_fee_percentage())/100)

    elif (amount > get_application_delta_amount()):

        application_fee =  ((get_application_delta_amount() * get_application_fee_percentage())/100)

        application_total_fee = application_fee + get_application_fee_extra()
    
    application_grand_total_fee = round(application_total_fee)
    return application_grand_total_fee
