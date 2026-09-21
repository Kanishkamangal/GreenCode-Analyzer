from app.services.windows_energy import (
    create_energy_meter,
)

import time


print(
    "Initializing Windows EMI..."
)

meter = None

try:

    meter = create_energy_meter(
        "RAPL_Package0_PKG"
    )

    print(
        "EMI initialized successfully."
    )

    print()
    print("DEVICE INFORMATION")
    print("------------------")

    info = meter.get_info()

    for key, value in info.items():

        print(
            f"{key}: {value}"
        )

    print()
    print("FIRST MEASUREMENT")
    print("-----------------")

    before = (
        meter.read_package_energy()
    )

    print(
        f"Absolute Energy: "
        f"{before.absolute_energy_pwh} pWh"
    )

    print(
        f"Absolute Time: "
        f"{before.absolute_time}"
    )

    print()
    print(
        "Waiting 2 seconds..."
    )

    time.sleep(2)

    print()
    print("SECOND MEASUREMENT")
    print("------------------")

    after = (
        meter.read_package_energy()
    )

    print(
        f"Absolute Energy: "
        f"{after.absolute_energy_pwh} pWh"
    )

    print(
        f"Absolute Time: "
        f"{after.absolute_time}"
    )

    print()
    print("INTERVAL ENERGY")
    print("----------------")

    delta_pwh = (
        after.absolute_energy_pwh
        -
        before.absolute_energy_pwh
    )

    energy_joules = (
        meter.energy_delta_joules(
            before,
            after,
        )
    )

    print(
        f"Energy Difference: "
        f"{delta_pwh} pWh"
    )

    print(
        f"Energy Consumption: "
        f"{energy_joules:.9f} J"
    )

except Exception as e:

    print()
    print("ERROR")
    print("-----")
    print(type(e).__name__)
    print(e)

finally:

    if meter is not None:
        meter.close()