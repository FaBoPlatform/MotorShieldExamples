#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

import sys
import time

import RTC
import OpenRTM_aist

import lidar
reload(lidar)

lidar_spec = ["implementation_id", "RTCLidar",
              "type_name",         "RTCLidar",
              "description",       "RTCLidar Component",
              "version",           "1.0",
              "vendor",            "GClue, Inc.",
              "category",          "lidar",
              "activity_type",     "DataFlowComponent",
              "max_instance",      "10",
              "language",          "Python",
              "lang_type",         "script",
              "conf.default.i2c_slave_address", "98",
              ""]

class RTCLidar(OpenRTM_aist.DataFlowComponentBase):
    
    def __init__(self, manager):
        print "__init__"
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._i2c_slave_address = [98]
        self.mlidar = lidar.LidarLite()
        return

    def onInitialize(self):
        print "onInitialize"
        self._d_IntOut = RTC.TimedLong(RTC.Time(0,0),0)
        self._IntOutOut = OpenRTM_aist.OutPort("IntOut", self._d_IntOut)
        self.addOutPort("IntOut",self._IntOutOut)
        
        self.bindParameter("i2c_slave_address", self._i2c_slave_address, "98")
        
        return RTC.RTC_OK
    
    def onActivated(self, ec_id):
        print "onActivate"
        print self._i2c_slave_address[0]
        self.mlidar.chageSlaveAddress(int(self._i2c_slave_address[0]))
        print "Finish I2C"
        return RTC.RTC_OK
        
    def onExecute(self, ec_id):
        print "onExcute"
        self._d_IntOut.data = self.mlidar.getDistance()
        OpenRTM_aist.setTimestamp(self._d_IntOut)
        print self._d_IntOut.data
        self._IntOutOut.write()
        return RTC.RTC_OK

def RTCLidarInit(manager):
    print "RTCLidarInit"
    profile = OpenRTM_aist.Properties(defaults_str=lidar_spec )
    manager.registerFactory(profile,
                          RTCLidar,
                          OpenRTM_aist.Delete)

def MyModuleInit(manager):
    print "MyModuleInit"
    RTCLidarInit(manager)

    # Create a component
    comp = manager.createComponent("RTCLidar")

def main():
    print "run"
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()
    
if __name__ == "__main__":
    main()

