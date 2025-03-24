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
