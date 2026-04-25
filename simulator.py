#!/usr/bin/env python3
"""Mini hotel group booking simulator.

The simulator asks learners whether to accept or reject a proposed group booking,
then reveals a displacement analysis and explains the decision.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    description: str
    stay_nights: int
    room_nights_requested: int
    group_rate: float
    variable_cost_per_room: float
    expected_displaced_room_nights: int
    expected_transient_rate: float
    ancillary_revenue_per_room_night: float
    meeting_space_cost: float
    hotel_pacing_occupancy: float
    hotel_pacing_rate: float


SCENARIOS: list[Scenario] = [
    Scenario(
        name="Regional Medical Conference",
        description=(
            "A weekday-heavy conference wants 120 rooms per night for 3 nights in "
            "September."
        ),
        stay_nights=3,
        room_nights_requested=360,
        group_rate=189.00,
        variable_cost_per_room=42.00,
        expected_displaced_room_nights=240,
        expected_transient_rate=249.00,
        ancillary_revenue_per_room_night=18.00,
        meeting_space_cost=4200.00,
        hotel_pacing_occupancy=0.87,
        hotel_pacing_rate=252.00,
    ),
    Scenario(
        name="Youth Sports Tournament",
        description=(
            "A weekend tournament asks for 80 rooms per night for 2 nights in a "
            "traditionally soft shoulder period."
        ),
        stay_nights=2,
        room_nights_requested=160,
        group_rate=149.00,
        variable_cost_per_room=35.00,
        expected_displaced_room_nights=40,
        expected_transient_rate=199.00,
        ancillary_revenue_per_room_night=12.00,
        meeting_space_cost=1200.00,
        hotel_pacing_occupancy=0.62,
        hotel_pacing_rate=191.00,
    ),
    Scenario(
        name="Pharma Sales Kickoff",
        description=(
            "A premium group requests 100 rooms per night for 4 nights during your "
            "citywide event period."
        ),
        stay_nights=4,
        room_nights_requested=400,
        group_rate=239.00,
        variable_cost_per_room=48.00,
        expected_displaced_room_nights=310,
        expected_transient_rate=319.00,
        ancillary_revenue_per_room_night=36.00,
        meeting_space_cost=6800.00,
        hotel_pacing_occupancy=0.96,
        hotel_pacing_rate=327.00,
    ),
]


def calculate_group_contribution(s: Scenario) -> float:
    contribution_per_room_night = (
        s.group_rate + s.ancillary_revenue_per_room_night - s.variable_cost_per_room
    )
    return contribution_per_room_night * s.room_nights_requested - s.meeting_space_cost


def calculate_displaced_contribution(s: Scenario) -> float:
    displaced_contribution_per_room_night = (
        s.expected_transient_rate - s.variable_cost_per_room
    )
    return displaced_contribution_per_room_night * s.expected_displaced_room_nights


def recommend_accept(s: Scenario) -> bool:
    return calculate_group_contribution(s) >= calculate_displaced_contribution(s)


def format_money(amount: float) -> str:
    return f"${amount:,.0f}"


def get_user_decision() -> str:
    while True:
        decision = input("To Take or Not Take? (take/not): ").strip().lower()
        if decision in {"take", "not", "not take", "no", "yes"}:
            if decision in {"take", "yes"}:
                return "take"
            return "not"
        print("Please type 'take' or 'not'.")


def print_scenario(idx: int, s: Scenario) -> None:
    print("\n" + "=" * 72)
    print(f"Scenario {idx}: {s.name}")
    print("-" * 72)
    print(s.description)
    print(
        "Current hotel pace: "
        f"{s.hotel_pacing_occupancy:.0%} occupancy at {format_money(s.hotel_pacing_rate)} ADR"
    )
    print(f"Stay length: {s.stay_nights} nights")
    print(f"Group room nights requested: {s.room_nights_requested}")
    print(f"Group ADR: {format_money(s.group_rate)}")
    print(f"Expected displaced transient room nights: {s.expected_displaced_room_nights}")
    print(f"Expected transient ADR: {format_money(s.expected_transient_rate)}")


def print_analysis(s: Scenario, user_decision: str) -> None:
    group_contribution = calculate_group_contribution(s)
    displaced_contribution = calculate_displaced_contribution(s)
    net_impact = group_contribution - displaced_contribution
    should_take = recommend_accept(s)

    print("\nDisplacement analysis")
    print("-" * 72)
    print(
        "Group contribution = "
        f"(group ADR + ancillary - variable cost) x group room nights - meeting cost"
    )
    print(
        f"= ({format_money(s.group_rate)} + {format_money(s.ancillary_revenue_per_room_night)}"
        f" - {format_money(s.variable_cost_per_room)}) x {s.room_nights_requested}"
        f" - {format_money(s.meeting_space_cost)}"
    )
    print(f"= {format_money(group_contribution)}")

    print()
    print("Displaced contribution = (transient ADR - variable cost) x displaced room nights")
    print(
        f"= ({format_money(s.expected_transient_rate)} - {format_money(s.variable_cost_per_room)})"
        f" x {s.expected_displaced_room_nights}"
    )
    print(f"= {format_money(displaced_contribution)}")

    print()
    print(f"Net impact if accepted = {format_money(net_impact)}")
    print("Recommendation: " + ("TAKE" if should_take else "DO NOT TAKE"))

    user_took = user_decision == "take"
    user_correct = user_took == should_take

    print("\nResult")
    print("-" * 72)
    if user_correct:
        print("✅ Correct decision.")
    else:
        print("❌ Not the best decision in this case.")

    if should_take:
        print(
            "Why: The group's total contribution is at least as high as displaced "
            "transient contribution, so accepting improves (or preserves) profit."
        )
    else:
        print(
            "Why: The expected displaced transient demand contributes more profit than "
            "the group offer, so accepting would dilute total profit."
        )


def run_simulator() -> None:
    print("Hotel Group Booking Simulator")
    print("Practice the 'To Take or Not Take' displacement decision.\n")

    for idx, scenario in enumerate(SCENARIOS, start=1):
        print_scenario(idx, scenario)
        decision = get_user_decision()
        print_analysis(scenario, decision)

    print("\nAll scenarios complete. Great work!")


if __name__ == "__main__":
    run_simulator()
