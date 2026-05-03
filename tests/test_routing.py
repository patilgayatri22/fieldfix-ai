"""Tests for keyword routing and category detection in main.py."""

import pytest
from backend.main import _resolve_demo, _symptom_is_recognisable
from backend.schemas.repair_output import Category


# ── Demo routing ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("symptom,expected", [
    ("servo buzzing but not moving",         "servo_buzzing"),
    ("servo motor jitter at 45 degrees",     "servo_buzzing"),
    ("stepper motor skipping steps",         "servo_buzzing"),
    ("L298N motor driver overheating",       "servo_buzzing"),
    ("robotic arm not reaching position",    "servo_buzzing"),
    ("encoder not reading correctly",        "servo_buzzing"),
    ("raspberry pi won't boot",              "raspberry_pi_not_booting"),
    ("raspberry pi not booting at all",      "raspberry_pi_not_booting"),
    ("arduino upload failed avrdude",        "raspberry_pi_not_booting"),
    ("esp32 keeps resetting brownout",       "raspberry_pi_not_booting"),
    ("oled display not showing anything",    "raspberry_pi_not_booting"),
    ("i2c device not detected",              "raspberry_pi_not_booting"),
    ("flashlight completely dead",           "flashlight_dead"),
    ("torch not turning on",                 "flashlight_dead"),
    ("headlamp not working",                 "flashlight_dead"),
    ("generator won't start",               "flashlight_dead"),
    ("smoke detector chirping",              "flashlight_dead"),
    ("power bank won't charge",             "flashlight_dead"),
    ("door hinge squeaking",                 "household_quick_fix"),
    ("faucet dripping constantly",           "household_quick_fix"),
    ("toilet keeps running",                 "household_quick_fix"),
    ("bike chain keeps slipping off",        "household_quick_fix"),
    ("wobbly chair leg",                     "household_quick_fix"),
    ("clogged shower drain",                 "household_quick_fix"),
    ("flickering light in living room",      "household_quick_fix"),
    ("deadbolt key very stiff",              "household_quick_fix"),
])
def test_resolve_demo_by_symptom(symptom, expected):
    assert _resolve_demo(symptom, None) == expected


@pytest.mark.parametrize("category,expected", [
    (Category.robotics,           "servo_buzzing"),
    (Category.electronics,        "raspberry_pi_not_booting"),
    (Category.emergency_equipment,"flashlight_dead"),
    (Category.household,          "household_quick_fix"),
    (Category.safety,             "household_quick_fix"),
])
def test_resolve_demo_by_category(category, expected):
    assert _resolve_demo("something generic", category) == expected


# ── Recognisability check ─────────────────────────────────────────────────────

@pytest.mark.parametrize("symptom", [
    "servo buzzing",
    "arduino not uploading",
    "flashlight dead",
    "hinge squeaking",
    "toilet running",
    "smoke detector beeping",
    "raspberry pi won't boot",
])
def test_recognisable_symptom(symptom):
    assert _symptom_is_recognisable(symptom, None) is True


@pytest.mark.parametrize("symptom", [
    "xyzzy frobnicator",
    "my thing is broken",
    "it stopped working",
    "help",
])
def test_unrecognisable_symptom_no_category(symptom):
    assert _symptom_is_recognisable(symptom, None) is False


def test_any_category_makes_recognisable():
    assert _symptom_is_recognisable("xyzzy frobnicator", Category.robotics) is True


# ── False-positive guard ──────────────────────────────────────────────────────

def test_chirping_not_matched_as_rpi():
    """'chirping' contains 'rpi' substring — must NOT route to raspberry_pi."""
    result = _resolve_demo("smoke detector chirping", None)
    assert result == "flashlight_dead"


def test_recipe_not_matched_as_pi():
    """'recipe' contains 'pi' — must NOT match Raspberry Pi routing."""
    result = _resolve_demo("recipe book fell off shelf", None)
    assert result != "raspberry_pi_not_booting"
