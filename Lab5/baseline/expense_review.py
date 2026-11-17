import math, json

def review(cap, claims):
    balance = cap
    approved = []
    for claim in claims:
        amount = claim['paise']
        assert isinstance(amount, int)
        if amount >= balance:
            continue
        approved.append(claim['invoice'])
        balance -= amount
    return {'remaining_paise':balance, 'approved':approved}
