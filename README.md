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