import random
import time
from datetime import datetime

# Normal system limits
NORMAL_VOLTAGE = 230.0
MIN_VOLTAGE = 200.0
MAX_CURRENT = 100.0

# Fault probability for simulation
FAULT_PROBABILITY = 0.25


def generate_phase_data():
    """
    Generate simulated three-phase voltage and current values.

    In a real system, replace this function with measurements
    obtained from appropriate isolated measurement hardware.
    """

    voltage_a = random.uniform(220, 240)
    voltage_b = random.uniform(220, 240)
    voltage_c = random.uniform(220, 240)

    current_a = random.uniform(20, 80)
    current_b = random.uniform(20, 80)
    current_c = random.uniform(20, 80)

    # Occasionally simulate a fault
    if random.random() < FAULT_PROBABILITY:

        fault_type = random.choice([
            "PHASE_A_FAULT",
            "PHASE_B_FAULT",
            "PHASE_C_FAULT",
            "EARTH_FAULT"
        ])

        if fault_type == "PHASE_A_FAULT":
            voltage_a = random.uniform(80, 160)
            current_a = random.uniform(110, 150)

        elif fault_type == "PHASE_B_FAULT":
            voltage_b = random.uniform(80, 160)
            current_b = random.uniform(110, 150)

        elif fault_type == "PHASE_C_FAULT":
            voltage_c = random.uniform(80, 160)
            current_c = random.uniform(110, 150)

        elif fault_type == "EARTH_FAULT":
            voltage_a = random.uniform(50, 120)
            current_a = random.uniform(120, 160)

    return (
        voltage_a,
        voltage_b,
        voltage_c,
        current_a,
        current_b,
        current_c
    )


def detect_fault(
    voltage_a,
    voltage_b,
    voltage_c,
    current_a,
    current_b,
    current_c
):
    """Detect possible transmission-line faults."""

    faults = []

    voltages = {
        "Phase A": voltage_a,
        "Phase B": voltage_b,
        "Phase C": voltage_c
    }

    currents = {
        "Phase A": current_a,
        "Phase B": current_b,
        "Phase C": current_c
    }

    # Check undervoltage
    for phase, voltage in voltages.items():

        if voltage < MIN_VOLTAGE:
            faults.append(
                f"{phase}: Undervoltage"
            )

    # Check overcurrent
    for phase, current in currents.items():

        if current > MAX_CURRENT:
            faults.append(
                f"{phase}: Overcurrent"
            )

    # Detect earth-fault-like condition
    if (
        current_a > MAX_CURRENT
        and voltage_a < 150
    ):
        faults.append("Possible Earth Fault")

    # Detect phase imbalance
    average_voltage = (
        voltage_a + voltage_b + voltage_c
    ) / 3

    voltage_deviation = max(
        abs(voltage_a - average_voltage),
        abs(voltage_b - average_voltage),
        abs(voltage_c - average_voltage)
    )

    if voltage_deviation > 25:
        faults.append("Voltage Phase Imbalance")

    if faults:
        return True, faults

    return False, []


def main():

    print("=" * 70)
    print("          TRANSMISSION LINE FAULT DETECTION")
    print("=" * 70)

    try:

        while True:

            (
                voltage_a,
                voltage_b,
                voltage_c,
                current_a,
                current_b,
                current_c
            ) = generate_phase_data()

            fault_detected, faults = detect_fault(
                voltage_a,
                voltage_b,
                voltage_c,
                current_a,
                current_b,
                current_c
            )

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            print("\n---------------------------------------------")
            print(f"Time: {timestamp}")

            print("\nThree-Phase Voltage:")
            print(f"Phase A: {voltage_a:.2f} V")
            print(f"Phase B: {voltage_b:.2f} V")
            print(f"Phase C: {voltage_c:.2f} V")

            print("\nThree-Phase Current:")
            print(f"Phase A: {current_a:.2f} A")
            print(f"Phase B: {current_b:.2f} A")
            print(f"Phase C: {current_c:.2f} A")

            if fault_detected:

                print("\n⚠ FAULT DETECTED")

                for fault in faults:
                    print(f"  - {fault}")

            else:

                print("\n✓ SYSTEM STATUS: NORMAL")

            print("---------------------------------------------")

            time.sleep(5)

    except KeyboardInterrupt:

        print("\nFault monitoring stopped.")


if __name__ == "__main__":
    main()
