import math

from builtin_interfaces.msg import Time
from imu_pkg.converters.imu_converter import ImuConverter
from imu_pkg.utils.gyro_lpf import GyroLowPassFilter
import pytest


@pytest.mark.parametrize('cutoff', [0.0, -5.0, float('nan'), float('inf')])
def test_invalid_cutoff_is_rejected(cutoff):
    with pytest.raises(ValueError):
        GyroLowPassFilter(True, cutoff)


def test_bypass_and_first_sample():
    unfiltered = GyroLowPassFilter(False, 5.0)
    assert unfiltered.update((1.0, 2.0, 3.0), 0) == (1.0, 2.0, 3.0)
    assert unfiltered.update((4.0, 5.0, 6.0), 0) == (4.0, 5.0, 6.0)
    filtered = GyroLowPassFilter(True, 5.0)
    assert filtered.update((1.0, 2.0, 3.0), 0) == (1.0, 2.0, 3.0)


def test_variable_sample_interval_reset_and_duplicate_stamp():
    filtered = GyroLowPassFilter(True, 5.0)
    filtered.update((0.0, 0.0, 0.0), 0)
    first = filtered.update((1.0, 2.0, 3.0), 10_000_000)
    assert first == pytest.approx([
        value * -math.expm1(-2.0 * math.pi * 5.0 * 0.01)
        for value in (1.0, 2.0, 3.0)
    ])
    # Two 10 ms updates at constant input equal one 20 ms training update.
    second = filtered.update((1.0, 2.0, 3.0), 20_000_000)
    assert second == pytest.approx([
        value * -math.expm1(-2.0 * math.pi * 5.0 * 0.02)
        for value in (1.0, 2.0, 3.0)
    ])
    assert filtered.update((99.0, 99.0, 99.0), 20_000_000) == second
    assert filtered.update((4.0, 5.0, 6.0), 1) == (4.0, 5.0, 6.0)
    filtered.reset()
    assert filtered.update((7.0, 8.0, 9.0), 100) == (7.0, 8.0, 9.0)


@pytest.mark.parametrize('dt', [0.01, 0.02])
def test_frequency_response(dt):
    filtered = GyroLowPassFilter(True, 5.0)
    omega = 2.0 * math.pi * 5.0 * dt
    ys = []
    for i in range(1000):
        sample = math.sin(omega * i)
        ys.append(filtered.update((sample,) * 3, round(i * dt * 1e9))[0])
    rms = math.sqrt(sum(y * y for y in ys[500:]) / 500)
    alpha = -math.expm1(-2.0 * math.pi * 5.0 * dt)
    gain = alpha / abs(1.0 - (1.0 - alpha) * complex(
        math.cos(omega), -math.sin(omega)
    ))
    assert rms * math.sqrt(2.0) == pytest.approx(gain, abs=1e-7)


def test_converter_filters_only_ros_angular_velocity():
    common = dict(frame_id='imu_link', zero_orientation_on_start=False)
    raw = ImuConverter(**common)
    filtered = ImuConverter(**common, gyro_lpf_enabled=True, gyro_lpf_cutoff_hz=5.0)
    data = dict(qx=0.0, qy=0.0, qz=0.0, qw=1.0,
                gx=0.0, gy=0.0, gz=0.0, ax=1.0, ay=2.0, az=3.0)
    filtered.to_msg(data, Time(sec=100))
    data.update(gx=180.0, gy=90.0, gz=-30.0)
    stamp = Time(sec=100, nanosec=20_000_000)
    original = raw.to_msg(data, stamp)
    result = filtered.to_msg(data, stamp)
    alpha = -math.expm1(-2.0 * math.pi * 5.0 * 0.02)
    assert [result.angular_velocity.x, result.angular_velocity.y,
            result.angular_velocity.z] == pytest.approx([
                -math.pi / 2 * alpha, math.pi * alpha, -math.pi / 6 * alpha
            ])
    assert result.orientation == original.orientation
    assert result.linear_acceleration == original.linear_acceleration
    assert filtered.to_gravity_msg(data, stamp) == raw.to_gravity_msg(data, stamp)
