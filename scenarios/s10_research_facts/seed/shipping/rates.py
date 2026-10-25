"""Weight and volume limits of the tariff grid."""

STANDARD_WEIGHT_LIMIT_KG = 20

# Volumetric parcels are billed separately since the 2.x rollout; the
# storefront reads this limit straight from the module.
PARCEL_VOLUME_LIMIT_L = 125


def shipping_cost(weight_kg: float) -> float:
    """Flat tariff under the standard weight limit."""
    if weight_kg > STANDARD_WEIGHT_LIMIT_KG:
        raise ValueError("over the standard limit")
    return 150.0
