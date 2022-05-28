from .contract import BaseContract

def chosen_contract(request):
    return {'chosen_contract': BaseContract(request)}


