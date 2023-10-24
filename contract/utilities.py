def permit_client(request, contract):
    if contract.contract_type == 'internal':
        user_is_client = request.user == contract.created_by
    else:
        user_is_client = request.user.email == contract.client.email
    return user_is_client


def can_accept_or_reject(contract):
    if contract.contract_type == 'internal':
        activator = contract.team.created_by
    else:
        activator = contract.client
    return activator