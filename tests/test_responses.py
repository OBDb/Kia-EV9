import glob
import os
import pytest
from pathlib import Path
from typing import Dict, Any

# These will be imported from the schemas repository
from schemas.python.can_frame import CANIDFormat
from schemas.python.json_formatter import format_file
from schemas.python.signals_testing import obd_testrunner_by_year

REPO_ROOT = Path(__file__).parent.parent.absolute()

TEST_CASES = [
    {
        "model_year": 2024,
        "tests": [
            # Tire pressures
            ("""
7A8102462C00BFFFFFF
7A821F8000000000200
7A82200000002000000
7A82300020000000002
7A8243BFFFFFFFFFFFF
7A825FFFFAAAAAAAAAA
""", {
    "EV9_TP_FL": 0,
    "EV9_TT_FL": -50,
    "EV9_TP_FR": 0,
    "EV9_TT_FR": -50,
    "EV9_TP_RL": 0,
    "EV9_TT_RL": -50,
    "EV9_TP_RR": 0,
    "EV9_TT_RR": -50,
    }),
            ("""
7A8102462C00BFFFFFF
7A821F8BE3C000400BD
7A8223C000400C13C00
7A8230400C13E000400
7A8243BA4B7A4B7A4B7
7A825A6B7AAAAAAAAAA
""", {
    "EV9_TP_FL": 38,
    "EV9_TT_FL": 10,
    "EV9_TP_FR": 37.8,
    "EV9_TT_FR": 10,
    "EV9_TP_RL": 38.6,
    "EV9_TT_RL": 10,
    "EV9_TP_RR": 38.6,
    "EV9_TT_RR": 12,
    }),
            ("""
7A8102462C00BFFFFFF
7A821F8D44F000600D2
7A8224F000600D65100
7A8230600D250000600
7A8243E93B893B893B8
7A82593B8AAAAAAAAAA
""", {
    "EV9_TP_FL": 42.4,
    "EV9_TT_FL": 29,
    "EV9_TP_FR": 42,
    "EV9_TT_FR": 29,
    "EV9_TP_RL": 42.8,
    "EV9_TT_RL": 31,
    "EV9_TP_RR": 42,
    "EV9_TT_RR": 30,
    }),

            # Odometer
            ("""
7CE101462B002400000
7CE210000B400000000
7CE2200000000000000
""", {
    "EV9_ODO_KM": 0,
    "EV9_ODO_MI": 0,
    }),
            ("""
7CE101462B002D00000
7CE2100FF9A00000000
7CE22184A0000000000
""", {
    "EV9_ODO_KM": 0,
    "EV9_ODO_MI": 6218.0,
    }),
            ("""
7CE101462B002D00000
7CE2100FFB600000000
7CE2218510000000000
""", {
    "EV9_ODO_KM": 0,
    "EV9_ODO_MI": 6225.0,
    }),

            # Battery state
            ("""
7EC103E620101EFFBE7
7EC21EF380000000000
7EC220000152D100E0F
7EC230D0E0F0D003BB2
7EC2470B27C00007D00
7EC250106540000FE99
7EC260000983700008E
7EC27C4005820590019
7EC2899000000000BB8
""", {
    "EV9_HVBAT_SOC": 28,
    "EV9_HVBAT_CHARGING": 0,
    "EV9_HVBAT_PLUG_RAPD": 0,
    "EV9_HVBAT_PLUG_NORM": 0,
    "EV9_HVBAT_CURR": 0,
    "EV9_HVBAT_VDC": 542.1,
    "EV9_HVBAT_T_MAX": 16,
    "EV9_HVBAT_T_MIN": 14,
    "EV9_HVBAT_MOD1_T": 15,
    "EV9_HVBAT_MOD2_T": 13,
    "EV9_HVBAT_MOD3_T": 14,
    "EV9_HVBAT_MOD4_T": 15,
    "EV9_HVBAT_INLET_T": 59,
    "EV9_C_V_MAX": 3.56,
    "EV9_C_V_MAX_ID": 112.0,
    "EV9_C_V_MIN": 3.56,
    "EV9_C_V_MIN_ID": 124,
    "EV9_HVBAT_FAN_STATUS": 0,
    "EV9_HVBAT_FAN": 0,
    "EV9_VPWR": 12.5,
    "EV9_HVBAT_CHRG_TOT_C": 6715.6,
    "EV9_HVBAT_DSCH_TOT_C": 6517.7,
    "EV9_HVBAT_CHRG_TOT_E": 3896.7,
    "EV9_HVBAT_DSCH_TOT_E": 3654.8,
    }),
            ("""
7EC103E620101EFFBE7
7EC21EFBD0000000000
7EC2200CE18430D0A0A
7EC230C0B0A0D0031CC
7EC2427CC4E00008000
7EC25010A8B0000FE9E
7EC2600009AB800008E
7EC27C70058A3860002
7EC286C109600000BB8
""", {
    "EV9_HVBAT_SOC": 94.5,
    "EV9_HVBAT_CHARGING": 0,
    "EV9_HVBAT_PLUG_RAPD": 0,
    "EV9_HVBAT_PLUG_NORM": 0,
    "EV9_HVBAT_CURR": 20.6,
    "EV9_HVBAT_VDC": 621.1,
    "EV9_HVBAT_T_MAX": 13,
    "EV9_HVBAT_T_MIN": 10,
    "EV9_HVBAT_MOD1_T": 10,
    "EV9_HVBAT_MOD2_T": 12,
    "EV9_HVBAT_MOD3_T": 11,
    "EV9_HVBAT_MOD4_T": 10,
    "EV9_HVBAT_INLET_T": 49,
    "EV9_C_V_MAX": 4.08,
    "EV9_C_V_MAX_ID": 39.0,
    "EV9_C_V_MIN": 4.08,
    "EV9_C_V_MIN_ID": 78,
    "EV9_HVBAT_FAN_STATUS": 0,
    "EV9_HVBAT_FAN": 0,
    "EV9_VPWR": 12.8,
    "EV9_HVBAT_CHRG_TOT_C": 6823.5,
    "EV9_HVBAT_DSCH_TOT_C": 6518.2,
    "EV9_HVBAT_CHRG_TOT_E": 3960.8,
    "EV9_HVBAT_DSCH_TOT_E": 3655.1,
    }),
        ]
    },
]

@pytest.mark.parametrize(
    "test_group",
    TEST_CASES,
    ids=lambda test_case: f"MY{test_case['model_year']}"
)
def test_signals(test_group: Dict[str, Any]):
    """Test signal decoding against known responses."""
    # Run each test case in the group
    for response_hex, expected_values in test_group["tests"]:
        try:
            obd_testrunner_by_year(
                test_group['model_year'],
                response_hex,
                expected_values,
                can_id_format=CANIDFormat.ELEVEN_BIT
            )
        except Exception as e:
            pytest.fail(
                f"Failed on response {response_hex} "
                f"(Model Year: {test_group['model_year']}: {e}"
            )

def get_json_files():
    """Get all JSON files from the signalsets/v3 directory."""
    signalsets_path = os.path.join(REPO_ROOT, 'signalsets', 'v3')
    json_files = glob.glob(os.path.join(signalsets_path, '*.json'))
    # Convert full paths to relative filenames
    return [os.path.basename(f) for f in json_files]

@pytest.mark.parametrize("test_file",
    get_json_files(),
    ids=lambda x: x.split('.')[0].replace('-', '_')  # Create readable test IDs
)
def test_formatting(test_file):
    """Test signal set formatting for all vehicle models in signalsets/v3/."""
    signalset_path = os.path.join(REPO_ROOT, 'signalsets', 'v3', test_file)

    formatted = format_file(signalset_path)

    with open(signalset_path) as f:
        assert f.read() == formatted

if __name__ == '__main__':
    pytest.main([__file__])
