from math import e as euler, log


def calculate_weights(
    dao_spot_price: int,
    supply: int,
    amount: int,
    curve_pad_ratio: float,
    dao_decimals: int,
) -> tuple[int, int]:
    curve_pad = (-log(curve_pad_ratio) / 5e-6) * 10**18
    start_supply = int(curve_pad) + supply

    start_weight = (
        (start_supply + 2e5 * euler ** (-5e-6)) * 10**dao_decimals / dao_spot_price
    )
    end_weight = (
        (start_supply + amount + 2e5 * euler ** (-5e-6))
        * 10**dao_decimals
        / dao_spot_price
    )

    return start_weight, end_weight
