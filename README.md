# imu_pkg

**IMU** package for EBIMU on ROS 2.

## Development Environment

| Component | Version |
|-----------|---------|
| **OS** | Ubuntu 22.04 |
| **ROS** | Humble Hawksbill |
| **IMU** | EBIMU |
| **Python** | Python 3.10 |

---

## 1. Setup

### 1.1 Install Python Dependencies

This package uses `pyserial` to communicate with the EBIMU device.

```bash
pip install pyserial

cd ~/colcon_ws
chmod 755 src/imu_pkg/scripts/install_udev_rules.sh
sudo ./src/imu_pkg/scripts/install_udev_rules.sh
```

---

## 2. Firmware Setting 

| Category | Parameter | Current Value | Description |
|---|---|---:|---|
| Device | Version response | `imu9dofv510` | Device firmware identifier |
| Communication | `sb` | 5 | Baud rate selection code |
| Output | `sor` | 10 | Output interval: 10 ms (100 Hz) |
| Output | `soc` | 1 | Output code setting |
| Output | `sof` | 2 | Orientation output format selection |
| Output | `sog` | 1 | Gyroscope data output enabled |
| Output | `soa` | 1 | Accelerometer data output enabled |
| Output | `som` | 0 | Magnetometer data output disabled |
| Output | `sod` | 0 | Position/distance output selection |
| Output | `sot` | 0 | Temperature output disabled |
| Output | `sots` | 0 | Timestamp output disabled |
| Magnetometer | `sem` | **0** | **Magnetometer disabled** |
| Sensor Range | `ssg` | 5 | Gyroscope measurement range selection |
| Sensor Range | `ssa` | 3 | Accelerometer measurement range selection |
| Filtering | `lpfg` | 2 | Gyroscope low-pass filter selection |
| Filtering | `lpfa` | 2 | Accelerometer low-pass filter selection |
| Filtering | `sffa` | 10 | Accelerometer filter factor |
| Filtering | `sffm` | 10 | Magnetometer filter factor |
| Robust Attitude Algorithm | `raa_l` | 0.200000 | RAA level parameter |
| Robust Attitude Algorithm | `raa_t` | 10000 | RAA time parameter |
| Robust Heading Algorithm | `rha_l` | 0.100000 | RHA level parameter |
| Robust Heading Algorithm | `rha_t` | 10000 | RHA time parameter |
| Auto Gyroscope Calibration | `agc_e` | 1 | AGC enabled |
| Auto Gyroscope Calibration | `agc_t` | 0.800000 | AGC threshold parameter |
| Auto Gyroscope Calibration | `agc_d` | 0.500000 | AGC duration parameter |
| Orientation Offset | `cmo` | 0 | Motion offset setting |
| Position Filter | `posf_sl` | 0.020000 | Position filter SL parameter |
| Position Filter | `posf_st` | 0 | Position filter ST parameter |
| Position Filter | `posf_sr` | 0.000000 | Position filter SR parameter |
| Position Filter | `posf_ar` | 1.000000 | Position filter AR parameter |
| Active Vibration Cancellation | `avca_e` | 1 | Accelerometer AVC enabled |
| Active Vibration Cancellation | `avcg_e` | 1 | Gyroscope AVC enabled |
| Startup | `pons` | 1 | Automatic operation on power-up enabled |
