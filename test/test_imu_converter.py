import math

from imu_pkg.converters.imu_converter import ImuConverter
import pytest


def quaternion_from_axis_angle(axis, angle_deg):
    half_angle = math.radians(angle_deg) * 0.5
    scale = math.sin(half_angle)
    components = [axis[0] * scale, axis[1] * scale, axis[2] * scale]
    return [*components, math.cos(half_angle)]


def ebimu_data(quaternion):
    qx, qy, qz, qw = quaternion
    return {'qx': qx, 'qy': qy, 'qz': qz, 'qw': qw}


def assert_quaternion_equal(actual, expected):
    direct_error = max(abs(a - b) for a, b in zip(actual, expected))
    negated_error = max(abs(a + b) for a, b in zip(actual, expected))
    assert min(direct_error, negated_error) < 1.0e-7


@pytest.mark.parametrize(
    ('apply_yaw_offset', 'expected_yaw_deg'),
    [(False, 0.0), (True, -90.0)],
)
def test_yaw_offset_is_independent_when_startup_zero_is_disabled(
    apply_yaw_offset,
    expected_yaw_deg,
):
    converter = ImuConverter(
        frame_id='imu_link',
        zero_orientation_on_start=False,
        apply_yaw_offset=apply_yaw_offset,
    )

    actual = converter.get_output_quaternion(
        ebimu_data([0.0, 0.0, 0.0, 1.0])
    )

    expected = quaternion_from_axis_angle([0.0, 0.0, 1.0], expected_yaw_deg)
    assert_quaternion_equal(actual, expected)


@pytest.mark.parametrize(
    ('apply_yaw_offset', 'expected_yaw_deg'),
    [(False, 0.0), (True, -90.0)],
)
def test_yaw_offset_is_independent_when_startup_zero_is_enabled(
    apply_yaw_offset,
    expected_yaw_deg,
):
    converter = ImuConverter(
        frame_id='imu_link',
        zero_orientation_on_start=True,
        apply_yaw_offset=apply_yaw_offset,
    )
    initial = ebimu_data(quaternion_from_axis_angle([1.0, 0.0, 0.0], 10.0))

    first = converter.get_output_quaternion(initial)
    second = converter.get_output_quaternion(initial)

    expected = quaternion_from_axis_angle([0.0, 0.0, 1.0], expected_yaw_deg)
    assert_quaternion_equal(first, expected)
    assert_quaternion_equal(second, expected)
