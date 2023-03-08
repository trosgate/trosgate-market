from .models import HiringFee


# CONTRACT FEES AND CHARGES STARTS

def get_extcontract_fee_percentage():
    try:
        return HiringFee.objects.get(id=1).extcontract_fee_percentage
    except:
        return 0


def get_contract_fee_percentage():
    try:
        return HiringFee.objects.get(id=1).contract_fee_percentage
    except:
        return 0

def get_contract_fee_extra():
    try:
        return HiringFee.objects.get(id=1).contract_fee_extra
    except:
        return 0

def get_contract_delta_amount():
    try:
        return HiringFee.objects.get(id=1).contract_delta_amount
    except:
        return 0


def get_extra_contract_value(amount):
    contract_extras = 0
    if (int(amount) > int(get_contract_delta_amount())):
        contract_extras = (amount - get_contract_delta_amount())
    return contract_extras


def get_external_contract_fee_calculator(amount):
    return ((amount * get_extcontract_fee_percentage())/100)

def get_external_contract_gross_earning(amount):
    return (amount - get_external_contract_fee_calculator(amount))


def get_contract_fee_calculator(amount):
    contract_total_fee = 0
    contract_fee = 0

    if (0 <= int(amount) <= int(get_contract_delta_amount())):
        contract_total_fee = ((amount * get_contract_fee_percentage())/100)

    elif (int(amount) > int(get_contract_delta_amount())):
        contract_fee = ((get_contract_delta_amount() * get_contract_fee_percentage())/100)
        contract_extras = (amount - get_contract_delta_amount())
        new_contract_extras = ((contract_extras * get_contract_fee_extra())/100)
        contract_total_fee = int(contract_fee) + int(new_contract_extras)

    contract_grand_total_fee = contract_total_fee
    return contract_grand_total_fee


# PROPOSAL FEES AND CHARGES STARTS

def get_proposal_fee_percentage():
    try:
        return HiringFee.objects.get(id=1).proposal_fee_percentage
    except:
        return 0


def get_proposal_fee_extra():
    try:
        return HiringFee.objects.get(id=1).proposal_fee_extra
    except:
        return 0


def get_proposal_delta_amount():
    try:
        return HiringFee.objects.get(id=1).proposal_delta_amount
    except:
        return 0


def get_extra_proposal_value(amount):
    proposal_extras = 0
    if (int(amount) > int(get_proposal_delta_amount())):
        proposal_extras = (amount - get_proposal_delta_amount())
    return proposal_extras


def get_proposal_fee_calculator(amount):
    proposal_total_fee = 0
    proposal_fee = 0

    if (0 <= int(amount) <= int(get_proposal_delta_amount())):
        proposal_total_fee = ((amount * get_proposal_fee_percentage())/100)

    elif (int(amount) > int(get_proposal_delta_amount())):
        proposal_fee = ((get_proposal_delta_amount() * get_proposal_fee_percentage())/100)

        proposal_extras = (amount - get_proposal_delta_amount())
        new_proposal_extras = ((proposal_extras * get_proposal_fee_extra())/100)
        proposal_total_fee = int(proposal_fee) + int(new_proposal_extras)

    proposal_grand_total_fee = proposal_total_fee
    return proposal_grand_total_fee


# APPLICATION FEES AND CHARGES STARTS

def get_application_fee_percentage():
    try:
        return HiringFee.objects.get(id=1).application_fee_percentage
    except:
        return 0


def get_application_fee_extra():
    try:
        return HiringFee.objects.get(id=1).application_fee_extra
    except:
        return 0


def get_application_delta_amount():
    try:
        return HiringFee.objects.get(id=1).application_delta_amount
    except:
        return 0


def get_extra_application_value(amount):
    application_extras = 0
    if (int(amount) > int(get_application_delta_amount())):
        application_extras = (amount - get_application_delta_amount())
    return application_extras


def get_application_fee_calculator(amount):
    application_total_fee = 0
    application_fee = 0

    if (0 <= amount <= get_application_delta_amount()):
        application_total_fee =  ((amount * get_application_fee_percentage())/100)
 
    elif (int(amount) > int(get_application_delta_amount())):
        application_fee =  ((get_application_delta_amount() * get_application_fee_percentage())/100)
        application_extras = (amount - get_application_delta_amount())
        new_application_extras = ((application_extras * get_application_fee_extra())/100)

        application_total_fee = int(application_fee) + int(new_application_extras)
    
    application_grand_total_fee = round(application_total_fee)
    return application_grand_total_fee

