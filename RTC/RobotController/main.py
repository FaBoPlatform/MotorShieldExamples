
# coding: utf-8
#!/usr/bin/env python
# -*- Python -*-

import sys
import time

import RTC
import OpenRTM_aist

import robotcar

seqin_spec = ["implementation_id", "RobotCarIn",
              "type_name",         "RobotCarComponent",
              "description",       "RobotCar InPort component",
              "version",           "1.0",
              "vendor",            "GClue, Inc.",

              "category",          "robot",
              "activity_type",     "DataFlowComponent",
              "max_instance",      "10",
              "language",          "Python",
              "lang_type",         "script",
              ""]
def valueMap(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


class RobotCarIn(OpenRTM_aist.DataFlowComponentBase):
    
    def __init__(self, manager):
        print "__init__"
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        
        return

    def onInitialize(self):
        print "onInitialize"
        self._r = robotcar.Robot()
        self._r.handle_init()
        self._floatSeq  = RTC.TimedFloatSeq(RTC.Time(0,0),[])        
        self._floatSeqIn  = OpenRTM_aist.InPort("FloatSeq", self._floatSeq)

        # Set InPort buffer
        self.addInPort("FloatSeq", self._floatSeqIn)
        return RTC.RTC_OK
    
    def onExecute(self, ec_id):
        
        floatSeq_  = self._floatSeqIn.read()        
        floatSize_  = len(floatSeq_.data)
        
        if floatSize_ > 0:
            power = int(floatSeq_.data[1])
            handle = int(floatSeq_.data[0])
            sys.stdout.write("\r%d  %d   " % (power, handle))
            sys.stdout.flush()
        
            if power < -10:
                power = valueMap(-power, 0, 150, 0, 100)
                self._r.car_back(power)
            elif power > 10:
                power = valueMap(power, 0, 150, 0, 100)
                self._r.car_forward(power)
            else:
                self._r.car_stop()
                
            handle = valueMap(handle, -150, 150, 7.5, 10.5)
            if handle < 8.9 or handle > 9.1:
                self._r.handle_move(handle)
            else:
                self._r.handle_move(9)
            
        time.sleep(0.5)
        return RTC.RTC_OK

def RobotCarInInit(manager):
    print "RobotCarInInit"
    profile = OpenRTM_aist.Properties(defaults_str=seqin_spec)
    manager.registerFactory(profile,
                          RobotCarIn,
                          OpenRTM_aist.Delete)

def MyModuleInit(manager):
    print "MyModuleInit"
    RobotCarInInit(manager)

    # Create a component
    comp = manager.createComponent("RobotCarIn")

def main():
    print "run"
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()
    
if __name__ == "__main__":
    main()