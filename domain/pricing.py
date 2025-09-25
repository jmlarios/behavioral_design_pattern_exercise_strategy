from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class LineItem:
    sku: str
    qty: int
    unit_price: float


class PricingStrategy(ABC):
    # TODO: Define the common interface for all pricing strategies.
    # This should include a method that takes pricing parameters and returns a calculated value.
    @abstractmethod
    def apply(self, subtotal: float, items: list[LineItem]) -> float:
        pass
    
    @abstractmethod
    def calculate(self, subtotal: float, items: list[LineItem]) -> float:
        pass


class NoDiscount(PricingStrategy):
    # TODO: Implement a strategy that returns the original value without changes
    def __init__(self):
        super().__init__()

    def apply(self, subtotal: float, items: list[LineItem]) -> float:
        return subtotal
    
    def calculate(self, subtotal: float, items: list[LineItem]) -> float:
        return subtotal


class PercentageDiscount(PricingStrategy):
    def __init__(self, percent: float) -> None:
        # TODO: Store the percentage value and validate it's in the correct range
        super().__init__()
        if not (0 <= percent <= 100):
            raise ValueError("Percentage must be between 0 and 100.")
        self.percent = percent

    # TODO: Implement the main calculation method that reduces the input by a percentage
    def apply(self, subtotal: float, items: list[LineItem]) -> float:
        discount = subtotal * (self.percent / 100)
        return subtotal - discount
    
    def calculate(self, subtotal: float, items: list[LineItem]) -> float:
        return self.apply(subtotal, items)

class BulkItemDiscount(PricingStrategy):
    """If any single item's quantity >= threshold, apply a per-item discount for that SKU."""
    def __init__(self, sku: str, threshold: int, per_item_off: float) -> None:
        # TODO: Store the parameters needed to identify items and calculate reductions
        super().__init__()

        self.sku = sku
        self.threshold = threshold
        self.per_item_off = per_item_off

    # TODO: Implement logic to iterate through items and apply reductions based on quantity thresholds
    def apply(self, subtotal: float, items: list[LineItem]) -> float:
        total_discount = sum(item.qty * self.per_item_off for item in items if item.sku == self.sku and item.qty >= self.threshold)
        return subtotal - total_discount
    
    def calculate(self, subtotal: float, items: list[LineItem]) -> float:
        return self.apply(subtotal, items)


class CompositeStrategy(PricingStrategy):
    """Compose multiple strategies; apply in order."""
    def __init__(self, strategies_or_first, *rest_strategies: PricingStrategy) -> None:
        # TODO: Store the collection of strategies to be applied sequentially
        super().__init__()
        if isinstance(strategies_or_first, list):
            # Called with a list: CompositeStrategy([strategy1, strategy2])
            self.strategies = strategies_or_first
        else:
            # Called with individual args: CompositeStrategy(strategy1, strategy2)
            self.strategies = [strategies_or_first] + list(rest_strategies)

    # TODO: Implement method that applies each strategy in sequence, using the output of one as input to the next
    def apply(self, subtotal: float, items: list[LineItem]) -> float:
        current_total = subtotal

        for strategy in self.strategies:
            current_total = strategy.apply(current_total, items)

        return current_total
    
    def calculate(self, subtotal: float, items: list[LineItem]) -> float:
        return self.apply(subtotal, items)


def compute_subtotal(items: list[LineItem]) -> float:
    return round(sum(it.unit_price * it.qty for it in items), 2)