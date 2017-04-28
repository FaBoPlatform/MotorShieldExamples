#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ch_array.py
 @brief change array 3 to 1
 @date $Date$


"""
import sys
import time
sys.path.append(".")
# Import RTM module
import RTC
import OpenRTM_aist

#import tensorflow
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

# Load graph
def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the 
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we can use again a convenient built-in function to import a graph_def into the 
    # current default Graph
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(
            graph_def, 
            input_map=None, 
            return_elements=None, 
            name="prefix", 
            op_dict=None, 
            producer_op_list=None
        )
    return graph

def detect(input_data):
    predictions = sess.run('prefix/neural_network_model/output_y:0',{'prefix/queue/dequeue_op:0':input_data})
    #predictions = sess.run('prefix/output:0',{'prefix/batch_size:0':1,'prefix/dequeue_op:0':input_data})

    index = np.argmax(predictions)
    if(index == 0):
        return 4
    elif(index == 1):
        return 1
    elif(index == 2):
        return 0
    elif(index == 3):
        return 3
    return "Detect Failed"
graph = load_graph('./pbfile/CAR_Multilayer-Perceptron2_500.pb')
#graph = load_graph('./pbfile/ckpt6_frozen_model.pb')


sess = tf.Session(graph=graph)

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
ch_array_spec = ["implementation_id", "ch_array",
		 "type_name",         "ch_array",
		 "description",       "change array 3 to 1",
		 "version",           "1.0.0",
		 "vendor",            "gclue",
		 "category",          "Category",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class ch_array
# @brief change array 3 to 1
#
#
class ch_array(OpenRTM_aist.DataFlowComponentBase):
	# @brief constructor
	# @param manager Maneger Object
	#
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		in3_arg = [None] * ((len(RTC._d_TimedLong) - 4) / 2)
		self._d_in3 = RTC.TimedLong(*in3_arg)
		"""
		"""
		self._in3In = OpenRTM_aist.InPort("in3", self._d_in3)
		in2_arg = [None] * ((len(RTC._d_TimedLong) - 4) / 2)
		self._d_in2 = RTC.TimedLong(*in2_arg)
		"""
		"""
		self._in2In = OpenRTM_aist.InPort("in2", self._d_in2)
		in1_arg = [None] * ((len(RTC._d_TimedLong) - 4) / 2)
		self._d_in1 = RTC.TimedLong(*in1_arg)
		"""
		"""
		self._in1In = OpenRTM_aist.InPort("in1", self._d_in1)
		
		self._d_out = RTC.TimedLong(RTC.Time(0,0),0)
		"""
		"""
		self._outOut = OpenRTM_aist.OutPort("out", self._d_out)

	def onInitialize(self):
		# Bind variables and configuration variable
		# Set InPort buffers
		self.addInPort("in3",self._in3In)
		self.addInPort("in2",self._in2In)
		self.addInPort("in1",self._in1In)
		# Set OutPort buffers
		self.addOutPort("out",self._outOut)
		# Set service provider to Ports
		# Set service consumers to Ports
		# Set CORBA Service Ports
		return RTC.RTC_OK

	def onExecute(self, ec_id):
		dataBuffer = []
		if self._in1In.isNew() or self._in2In.isNew() or self._in3In.isNew():
			while True:
				a = self._in1In.read().data
				if a != None:
					break
			dataBuffer.append(a)
			while True:
				b = self._in2In.read().data
				if b != None:
					break
			dataBuffer.append(b)
			while True:
				c = self._in3In.read().data
				if c != None:
					break
			dataBuffer.append(c)
			#dataBuffer.append(self._in2In.read().data)
			#dataBuffer.append(self._in3In.read().data)
			self._d_out.data = detect(np.array([[0.0,dataBuffer[0],0.0]]))
			OpenRTM_aist.setTimestamp(self._d_out)
			print dataBuffer[0]
			self._outOut.write()
			#print dataBuffer
		return RTC.RTC_OK

def ch_arrayInit(manager):
	profile = OpenRTM_aist.Properties(defaults_str=ch_array_spec)
	manager.registerFactory(profile,
							ch_array,
							OpenRTM_aist.Delete)

def MyModuleInit(manager):
	ch_arrayInit(manager)

	# Create a component
	comp = manager.createComponent("ch_array")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

