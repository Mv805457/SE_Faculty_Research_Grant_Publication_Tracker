"""Review one grant budget head, using integer paise throughout."""
import json
from pathlib import Path


def _is_paise(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _reason(claim, remaining, seen):
    """Return the rejection reason or an empty string for an eligible claim."""
    if not isinstance(claim, dict):
        return "invalid claim"
    invoice = claim.get("invoice")
    if not isinstance(invoice, str) or not invoice.strip():
        return "missing invoice"
    if invoice.strip().casefold() in seen:
        return "duplicate invoice"
    amount = claim.get("paise")
    if not _is_paise(amount) or amount <= 0:
        return "invalid amount"
    if amount > remaining:
        return "over budget"
    return ""


def review(cap, claims):
    """Process claims in order. Only approved invoices consume funds."""
    if not _is_paise(cap) or cap < 0:
        raise ValueError("cap must be a nonnegative integer in paise")
    if not isinstance(claims, list):
        raise ValueError("claims must be a list")
    remaining = cap
    approved = []
    rejected = []
    seen = set()
    for position, claim in enumerate(claims, start=1):
        reason = _reason(claim, remaining, seen)
        if reason:
            rejected.append({"row": position, "reason": reason})
            continue
        invoice = claim["invoice"].strip()
        approved.append(invoice)
        seen.add(invoice.casefold())
        remaining -= claim["paise"]
    return {"remaining_paise": remaining, "approved": approved,
            "rejected": rejected}


if __name__ == "__main__":
    sample = Path(__file__).with_name("claims.json")
    with sample.open(encoding="utf-8") as stream:
        batch = json.load(stream)
    print(json.dumps(review(batch["cap_paise"], batch["claims"]), indent=2))
