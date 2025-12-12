# Feetech Firmware

Python library for controlling Feetech servo motors.

## Setup

### 1. Download Feetech FD Software

Download the Feetech FD software from the official website:  
[https://www.feetechrc.com/software.html](https://www.feetechrc.com/software.html)

### 2. Running Feetech FD Software

- **Ubuntu**: Use [Wine](https://www.winehq.org/) to run the Feetech FD software
- **Windows**: Run the Feetech FD software directly

### 3. Configure Servo IDs

Use the Feetech FD software to update the ID for each servo motor.

### Example

| Module | Description |
|--------|-------------|
| `SCSBus_python.py` | SCS servo bus communication class |
| `debug/test_two_servo_python.py` | Example: dual servo sine wave motion test |
