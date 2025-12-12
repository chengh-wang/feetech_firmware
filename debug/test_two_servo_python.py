#!/usr/bin/env python3

import sys
import time
import math
import matplotlib.pyplot as plt

# Add parent directory to path to import SCSBus_python
sys.path.insert(0, '..')
from SCSBus_python import SCSBUS

# ============ 配置 ============
PORT_NAME = '/dev/ttyUSB0'
BAUDRATE = 1000000
SERVO_IDS = [0, 1]

POS_MIN = 0
POS_CENTER = 2048
POS_MAX = 3413

def plot_positions(times, desired_pos1, desired_pos2, actual_pos1, actual_pos2, freq1, freq2):
    """
    Plot desired vs actual positions for two servos in two subplots
    
    Args:
        times: List of time values in seconds
        desired_pos1: Desired positions for servo 1
        desired_pos2: Desired positions for servo 2
        actual_pos1: Actual positions for servo 1
        actual_pos2: Actual positions for servo 2
        freq1: Frequency used for servo 1 (Hz)
        freq2: Frequency used for servo 2 (Hz)
    """
    plt.figure(figsize=(10, 8))
    
    # Subplot for Servo 1
    plt.subplot(2, 1, 1)
    plt.plot(times, desired_pos1, label='Desired Pos 1', linestyle='--')
    plt.plot(times, actual_pos1, label='Actual Pos 1')
    plt.title(f'Servo 1 Position Tracking (freq={freq1} Hz)')
    plt.ylabel('Position')
    plt.legend()
    plt.grid(True)
    
    # Subplot for Servo 2
    plt.subplot(2, 1, 2)
    plt.plot(times, desired_pos2, label='Desired Pos 2', linestyle='--')
    plt.plot(times, actual_pos2, label='Actual Pos 2')
    plt.title(f'Servo 2 Position Tracking (freq={freq2} Hz)')
    plt.xlabel('Time (s)')
    plt.ylabel('Position')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    
    # Save the plot with frequency values in the filename
    filename = f'servo_tracking_freq1_{freq1}Hz_freq2_{freq2}Hz.png'
    plt.savefig(filename, dpi=150)
    print(f"Plot saved as: {filename}")
    
    plt.show()

def main():

    servo_bus = SCSBUS("/dev/ttyUSB0", [0, 1])
    amplitude = 500
    center = 500
    phase_offset = math.pi / 2
    
    
    loop_count = 0
    last_status = {0: {}, 1: {}}

    freq1 = 0.2
    freq2 = 0.3

    desired_pos1 = []
    actual_pos1 = []
    desired_pos2 = []
    actual_pos2 = []
    times = []
    servo_bus.sync_write_positions({0: center, 1: center})
    time.sleep(1)
    
    start_time = time.time()
    try:
        while (time.time() - start_time) < 10:
            t = time.time() - start_time
            
            pos0 = int(center + amplitude * math.sin(2 * math.pi * freq1 * t))
            pos1 = int(center + amplitude * math.sin(2 * math.pi * freq2 * t))
            desired_pos1.append(pos0)
            desired_pos2.append(pos1)
            
            # 写入
            servo_bus.sync_write_positions({0: pos0, 1: pos1})
            
            loop_count += 1
            
            # 每 N 次读取一次
            # if loop_count % read_every_n == 0:
            last_status = servo_bus.read_all_positions(SERVO_IDS)
            
            s0 = last_status.get(0, {})
            s1 = last_status.get(1, {})
            actual_pos1.append(s0.get('position',0))
            actual_pos2.append(s1.get('position',0))
            times.append(t)
            
            freq = loop_count / t
            print(f"t={t:5.2f}s | freq={freq:5.1f}Hz | "
                    f"ID0: cmd={pos0:4d} act={s0.get('position',0):4d} spd={s0.get('speed',0):5d} | "
                    f"ID1: cmd={pos1:4d} act={s1.get('position',0):4d} spd={s1.get('speed',0):5d}")
            
            time.sleep(0.001)
            
    except KeyboardInterrupt:
        print("\n用户中断")
    
    final_freq = loop_count / (time.time() - start_time)
    print(f"\n最终控制频率: {final_freq:.1f} Hz")
    
    servo_bus.sync_write_positions({0: POS_CENTER, 1: POS_CENTER}, speed=500)
    servo_bus.close()

    plot_positions(times, desired_pos1, desired_pos2, actual_pos1, actual_pos2, freq1, freq2)

if __name__ == '__main__':
    main()