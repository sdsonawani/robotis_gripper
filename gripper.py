#!/usr/bin/env python3

import os
import sys
import time
from dynamixel_sdk import PortHandler, PacketHandler
from grasp_function import Grasp_Distance
import argparse

MAX = 0.10986
MIN = 0.005

class RobotisGripper():

    def __init__(self,port= "/dev/ttyUSB6" ,cls_distance = 100.0):
        self.h_port      = PortHandler(port)
        self.h_packet    = PacketHandler(2.0)
        self.use_gripper = False
        self.cls_distance = cls_distance
        self.grasp_d = Grasp_Distance()


    def __del__(self):
        if self.use_gripper:
            self.openGripper()
            time.sleep(1)
            self.h_packet.write1ByteTxRx(self.h_port, 1, 562, 0)
            self.h_port.closePort()
            print("Successfully shut down the Gripper")

    # Initialize the gripper
    def init(self):
        if self.use_gripper:
            print("Gripper already in use")
            return 

        if not self.h_port.openPort():
            print("Can't connect to Gripper")
            return
        
        if not self.h_port.setBaudRate(57600):
            print("Failed to change the baudrate")
            return

        dxl_comm_result, dxl_error = self.h_packet.write1ByteTxRx(self.h_port, 1, 562, 1)
        if dxl_comm_result != 0 or dxl_error != 0:
            print("Failed to enable gripper: ")
            print("  " + self.h_packet.getTxRxResult(dxl_comm_result))
            print("  " + self.h_packet.getRxPacketError(dxl_error))
            return

        print("Gripper Enabled")
        self.use_gripper = True
        return self.use_gripper


    def closeGripper(self):
        value = self.val(self.cls_distance)
        dxl_comm_result, dxl_error = self.h_packet.write4ByteTxRx(self.h_port, 1, 596, value)
        if dxl_comm_result != 0 or dxl_error != 0:
            print("Failed to enable gripper: ")
            print("  " + self.h_packet.getTxRxResult(dxl_comm_result))
            print("  " + self.h_packet.getRxPacketError(dxl_error))
            return False
        else:
            return True
            
    def openGripper(self):
        dxl_comm_result, dxl_error = self.h_packet.write4ByteTxRx(self.h_port, 1, 596, 1)
        if dxl_comm_result != 0 or dxl_error != 0:
            print("Failed to enable gripper: ")
            print("  " + self.h_packet.getTxRxResult(dxl_comm_result))
            print("  " + self.h_packet.getRxPacketError(dxl_error))
    
    # use learned mapping from distance [mm] to serial for closing distance
    def val(self):  
        out = self.grasp_d.prediction(self.cls_distance)
        if out > MAX and out < MIN:
            raise ValueError("Gripper close value exceeds MIN {} and MAX {} limits".format(MIN,MAX))
        return out

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--port",type=str,default="/dev/ttyUSB6",help="check the port connected to gripper controller")
    parser.add_argument("--close",type=float,default=100.0,help="gripper closing distance in mm")
    args = parser.parse_args()
    
    print(args.port, args.close)
    gripper = RobotisGripper(port = args.port, cls_distance = args.close)
    gripper.init()

    try:
        while True:
            gripper.openGripper()
            time.sleep(2)
            gripper.closeGripper()
            time.sleep(2)
    except KeyboardInterrupt:
        del gripper