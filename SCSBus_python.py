#!/usr/bin/env python3
"""
SCSBus - Feetech SCS servo bus communication module
"""

import sys
import time
import math
import threading

sys.path.append('./FTServo_Python')
from scservo_sdk import *


class SCSBUS():
    def __init__(self, port, ids, baudrate=1000000, pos_limit_max=3413, pos_limit_min=0):
        self.ids = ids
        self.pos_limit_max = pos_limit_max
        self.pos_limit_min = pos_limit_min
        self.pos_center = (pos_limit_max + pos_limit_min) // 2

        self.port = PortHandler(port)
        if not self.port.openPort():
            print(f"[ERROR] Can't open {port}")
            sys.exit(1)
        self.port.setBaudRate(baudrate)
        self.servo = scscl(self.port)

        for sid in self.ids:
            model, result, _ = self.servo.ping(sid)
            if result == COMM_SUCCESS:
                print(f"[OK] ID={sid} online, model={model}")
            else:
                print(f"[WARNING] ID={sid} offline")

    def sync_write_positions(self, positions: dict, speed: int = 0) -> bool:
        for scs_id, pos in positions.items():
            pos = max(0, min(4095, int(pos)))
            self.servo.SyncWritePos(scs_id, pos, 0, speed)
        result = self.servo.groupSyncWrite.txPacket()
        self.servo.groupSyncWrite.clearParam()
        return result == COMM_SUCCESS

    def read_position_and_speed(self, scs_id: int) -> tuple:
        pos, speed, result, error = self.servo.ReadPosSpeed(scs_id)
        if result == COMM_SUCCESS:
            return pos, speed, True
        return 0, 0, False

    def read_all_positions(self, ids: list) -> dict:
        result = {}
        for scs_id in ids:
            pos, speed, ok = self.read_position_and_speed(scs_id)
            result[scs_id] = {'position': pos, 'speed': speed, 'success': ok}
        return result

    def close(self):
        if self.port:
            self.port.closePort()
            print("[OK] 串口已关闭")
