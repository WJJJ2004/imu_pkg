import math


class GyroLowPassFilter:
    """Measured gyro only; exponential first-order pole matching ROA training."""

    def __init__(self, enabled=False, cutoff_hz=5.0):
        if not math.isfinite(cutoff_hz) or cutoff_hz <= 0.0:
            raise ValueError('gyro_lpf_cutoff_hz must be finite and positive')
        self.enabled = enabled
        self.cutoff_hz = cutoff_hz
        self.reset()

    def reset(self):
        self._state = None
        self._stamp_ns = None

    def update(self, values, stamp_ns):
        values = tuple(values)
        if not self.enabled:
            return values
        if self._state is None or stamp_ns < self._stamp_ns:
            # Seed the first sample, or restart after a backwards clock jump.
            self._state = values
            self._stamp_ns = stamp_ns
        elif stamp_ns > self._stamp_ns:
            dt = (stamp_ns - self._stamp_ns) * 1.0e-9
            alpha = -math.expm1(-2.0 * math.pi * self.cutoff_hz * dt)
            self._state = tuple(
                previous + alpha * (value - previous)
                for previous, value in zip(self._state, values)
            )
            self._stamp_ns = stamp_ns
        # A duplicate timestamp does not advance state.
        return self._state
