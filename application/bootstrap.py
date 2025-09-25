from __future__ import annotations
from domain.pricing import PricingStrategy, NoDiscount, PercentageDiscount, BulkItemDiscount, CompositeStrategy


def choose_strategy(kind: str, **kwargs) -> PricingStrategy:
    # TODO: Implement strategy selection logic based on the 'kind' parameter
    # Should support: "none", "percent", "bulk", "composite"
    # Each strategy type needs different parameters from **kwargs
    # Return the appropriate strategy instance or raise an error for unknown types
    if kind == "none":
        return NoDiscount()
    elif kind == "percent":
        return PercentageDiscount(kwargs["percent"])
    elif kind == "bulk":
        return BulkItemDiscount(kwargs["sku"], kwargs["threshold"], kwargs["per_item_off"])
    elif kind == "composite":
        # Create composite strategy with both percentage and bulk discount
        strategies = [
            PercentageDiscount(kwargs["percent"]),
            BulkItemDiscount(kwargs["sku"], kwargs["threshold"], kwargs["per_item_off"])
        ]
        return CompositeStrategy(strategies)
    else:
        raise ValueError(f"Unknown strategy kind: {kind}")
