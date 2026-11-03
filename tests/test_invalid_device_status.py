
from unittest.mock import patch

import pytest

from ics_2000.hub import Hub


@pytest.fixture
def hub():
    return Hub("test@example.com", "dummy-password")


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        (
            [
                {"id": 1, "status": {"module": {"functions": [1, 2]}}},
                {"id": 2, "status": {"group": {"functions": [3]}}},
            ],
            {1: [1, 2], 2: [3]},
        ),
        (
            [
                {"id": 1, "status": {"module": {"functions": [1]}}},
                {"id": 17574805, "status": None},
                {"id": 3, "status": {"module": {"functions": [2]}}},
            ],
            {1: [1], 3: [2]},
        ),
        (
            [
                None,
                {"id": 4, "status": {}},
                {"id": 5, "status": {"module": None}},
                {"id": 6, "status": {"module": {"functions": [9]}}},
            ],
            {6: [9]},
        ),
        (None, {}),
    ],
)
def test_get_all_device_statuses_handles_invalid_records(
    hub, response, expected
):
    with patch.object(
        hub, "get_raw_device_statuses", return_value=response
    ) as mocked_get_statuses:
        hub.get_all_device_statuses()

    mocked_get_statuses.assert_called_once_with(False, True)
    assert hub.device_statuses == expected
