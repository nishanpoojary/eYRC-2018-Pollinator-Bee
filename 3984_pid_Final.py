#!/usr/bin/env python
'''
Team ID: 3984
Author List: Nishan Poojary 
FileName: Positon Hold 
Theme: Pollinator Bot
Functions: __init__(self), arm(self), disarm(self), position_hold(self), calc_pid(self), pid_roll(self), pid_pitch(self), pid_throt(self) ,limit(self, 		   input_value, max_value, min_value), set_pid_alt(self,pid_val), set_pid_roll(self,pid_val), set_pid_pitch(self,pid_val), set_pid_yaw(self,pid_val), 		   get_pose(self,pose) 
Global Variables: None 	  
'''

#The required packages are imported here
from plutodrone.msg import *
from pid_tune.msg import *
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Int32
from std_msgs.msg import Float64
import rospy
import time
import numpy as np

class DroneFly():
	"""docstring for DroneFly"""
	def __init__(self):

		#rospy.init_node('drone_server')
		rospy.init_node('pluto_fly', disable_signals = True)

		self.pluto_cmd = rospy.Publisher('/drone_command', PlutoMsg, queue_size=10)

		rospy.Subscriber('whycon/poses', PoseArray, self.get_pose)
	
		#These Are Subscriber Fucntions For Getting the Values Of Red, Blue and Green Count Respectively From Image Processing Code 
		rospy.Subscriber('/red', Float64 , self.redIM )
		rospy.Subscriber('/green', Float64 , self.greenIM )
		rospy.Subscriber('/blue', Float64 , self.blueIM 

		# To tune the drone during runtime
		rospy.Subscriber('/pid_tuning_altitude', PidTune, self.set_pid_alt)
		rospy.Subscriber('/pid_tuning_roll', PidTune, self.set_pid_roll)
		rospy.Subscriber('/pid_tuning_pitch', PidTune, self.set_pid_pitch)
		rospy.Subscriber('/pid_tuning_yaw', PidTune, self.set_pid_yaw)
		
		self.cmd = PlutoMsg()

		# Position to hold.
		self.Plant_location = [(1, 1, 18), (5.9,-0.8,20.6), (-3.8,1.4,19.5), (1.8,-3.3,26)]
		# This is the BeeHive Locations
		self.Bee_hive = [(1.1, 8.4, 28.5)]

  		#Drone Motor Parameters Initialized  
		self.cmd.rcRoll = 1500
		self.cmd.rcPitch = 1500
		self.cmd.rcYaw = 1500
		self.cmd.rcThrottle = 1000
		self.cmd.rcAUX1 = 1500
		self.cmd.rcAUX2 = 1500
		self.cmd.rcAUX3 = 1500
		self.cmd.rcAUX4 = 1000
		self.cmd.plutoIndex = 0

		#Initialization of Current Drone Location 
		self.drone_x = 0.0
		self.drone_y = 0.0
		self.drone_z = 0.0

		#PID constants for Roll
		self.kp_roll = 11.789#10.852 #20
		self.ki_roll = 0.1463#0.106
		self.kd_roll = 475.129#578.578

		#PID constants for Pitch
		self.kp_pitch = 8.34#13.543
		self.ki_pitch = 0.0932#0.129 
		self.kd_pitch = 375.074#1400.531
		
		#PID constants for Yaw
		self.kp_yaw = 0.0
		self.ki_yaw = 0.0
		self.kd_yaw = 0.0

		#PID constants for Throttle
		self.kp_throt = 27.499#28.31 #23
		self.ki_throt  = 0.518#0.4677 #2
		self.kd_throt = 548.803#650.102 #19.59 #19

		# Correction values after PID is computed
		self.correct_roll = 0.0
		self.correct_pitch = 0.0
		self.correct_yaw = 0.0
		self.correct_throt = 0.0

		# Loop time for PID computation. You are free to experiment with this
		self.last_time = 0.0
		self.loop_time = 0.030

		#Publishing Roll, Pitch And Throttle Errors 
                self.pub1 = rospy.Publisher('/roll_err',Float64, queue_size=1)
                self.zroer = rospy.Publisher('/zero_line', Float64, queue_size=1)
                self.pub2 = rospy.Publisher('/pitch_err',Float64, queue_size=1)
                self.pub3 = rospy.Publisher('/alt_err',Float64, queue_size=1)
                self.dx = rospy.Publisher('/dx', Float64, queue_size=1)
                
		rospy.sleep(.1)

                # self declaration
                self.roll_error = 0.0
                self.pitch_error = 0.0
                self.throttle_error = 0.0
                self.previous_roll_error = 0.0
                self.previous_pitch_error = 0.0
                self.previous_throttle_error = 0.0

	        #Proportional Parameter Of Roll, Throttle & Pitch Respectively
                self.proll = 0.0 
                self.pthrot = 0.0
                self.ppitch = 0.0 

	        #Integral Parameter Of Roll, Throttle & Pitch Respectively
                self.interoll = 0.0 
                self.intepitch = 0.0 
                self.intethrot = 0.0

		#Derivative Parameter Of Roll, Throttle & Pitch Respectively
                self.derivroll = 0.0
                self.derivpitch = 0.0
                self.derivthrot = 0.0
	
		#Take Off Fucntion Variable
                self.takeoff = 1.0

          	#'i' Next Waypoint Indicating Variable
		self.i = 0.0

		#Counter Variable For Position Holding 
                self.go =0.0

	#Arming Of the Drone 
	def arm(self):
		self.cmd.rcAUX4 = 1500
               
		self.cmd.rcThrottle = 1000
		self.pluto_cmd.publish(self.cmd)
		rospy.sleep(.1)

	#Disarming Of the Drone 
	def disarm(self):
		self.cmd.rcAUX4 = 1100
		self.pluto_cmd.publish(self.cmd)
		rospy.sleep(.1)

	#Position Holding Algorithm 
	def position_hold(self):

		rospy.sleep(2)

		print "disarm"
		self.disarm()
		rospy.sleep(.2)
		print "arm"
		self.arm()
		rospy.sleep(.1)

		while True:
			#This Below Algorithm Is Take Off Algorithm Which Runs Only Once And Provdes The Dronw Initial Necessary Height
			if(self.takeoff == 1.0 ):
                            self.cmd.rcThrottle = 1800
		            self.pluto_cmd.publish(self.cmd)
		            time.sleep(2)
  			    self.takeoff = 2
			    
			
                        self.calc_pid()
			#This Provides The Correction Values To the Drone 
			pitch_value = int(1500 + self.correct_pitch)
			self.cmd.rcPitch = self.limit (pitch_value,1600, 1400)
																	
			roll_value = int(1500 + self.correct_roll)
			self.cmd.rcRoll = self.limit(roll_value, 1600,1400)
												
			throt_value = int(1500 - self.correct_throt )
			self.cmd.rcThrottle = self.limit(throt_value, 1800,1200)
															
			self.pluto_cmd.publish(self.cmd)
	
	#Calculation of the PID Parameters
	def calc_pid(self):
		self.seconds = time.time()
		current_time = self.seconds - self.last_time
		if(current_time >= self.loop_time):
			self.pid_throt(current_time)
			self.pid_roll(current_time)
			self.pid_pitch(current_time)
			
			
			self.last_time = self.seconds

	#Calculation Of PID Parameters for Roll
	def pid_roll(self):
	     if(self.i == 0.0):
               self.roll_error = ( self.Plant_location[0][1] - self.drone_y )
             elif(self.i == 1.0):
               self.roll_error = ( self.Plant_location[1][1] - self.drone_y )
	     elif(self.i == 2.0):
               self.roll_error = ( self.Plant_location[2][1] - self.drone_y )
	     elif(self.i == 3.0):
               self.roll_error = ( self.Plant_location[3][1] - self.drone_y )
	     elif(self.i == 4.0):
               self.roll_error = ( self.Bee_hive[0][1] - self.drone_y )

             
             self.proll = ( self.kp_roll * self.roll_error  )
             self.interoll = self.interoll + (self.roll_error/20) 
            
             self.droll = 0.0
             
             self.derivroll = ( ( self.roll_error - self.previous_roll_error )  )
		  
             self.previous_roll_error = self.roll_error
             self.correct_roll = ( self.proll) + (  self.kd_roll * self.derivroll ) + (self.ki_roll * self.interoll )
             
             self.zroer.publish(0.0)
             self.pub1.publish(self.roll_error)
             
		             
	#Calculation Of PID Parameters for Pitch
	def pid_pitch(self):
        
             if(self.i == 0.0):
                self.pitch_error = (self.Plant_location[0][0] - self.drone_x )
             elif(self.i == 1.0):
                self.pitch_error = (self.Plant_location[1][0] - self.drone_x )
	     elif(self.i == 2.0):
                self.pitch_error = (self.Plant_location[2][0] - self.drone_x )
	     elif(self.i == 3.0):
                self.pitch_error = (self.Plant_location[3][0] - self.drone_x )
	     elif(self.i == 4.0):
                self.pitch_error = (self.Bee_hive[0][0] - self.drone_x )

             
             self.ppitch = (self.kp_pitch * self.pitch_error )
             self.intepitch = self.intepitch + (self.pitch_error/20)
             
             self.dpitch = 0.0
             
             self.derivpitch = ( ( self.pitch_error - self.previous_pitch_error )   )
		 
             self.correct_pitch  = ( self.ppitch) + (  self.derivpitch * self.kd_pitch )  + ( self.intepitch * self.ki_pitch )
             self.previous_pitch_error  = self.pitch_error
	     
             self.pub2.publish(self.pitch_error)
	         

	#Calculation Of PID Parameters for Throttle        
	def pid_throt(self):
             
	     #This Is The Calculation Of First Waypoint Error Values & This First Waypopint also Minimize's The Initial Corection Errors In Derivative and Intergral Tearms 
	 
             if(self.i == 0.0):
                self.throttle_error = (self.Plant_location[0][2] - self.drone_z )
                if(((self.roll_error < 0.5 and self.roll_error > -0.5)and(self.pitch_error < 0.5 and self.pitch_error > -0.5)and(self.throttle_error < 2.0 and self.throttle_error > -2.0 ))):

                  #This Is the Counter For Position Holding  
                  if(self.go > 8):  
                    self.i = 1.0
		    self.go = 0.0
		  else :
                    self.go = self.go + 1
		    time.sleep(0.1)

             #This Is The Calculation Of First Waypoint Error Values      
             elif(self.i == 1.0 ):
                self.throttle_error = (self.Plant_location[1][2] - self.drone_z )
                if(((self.roll_error < 0.5 and self.roll_error > -0.5)and(self.pitch_error < 0.5 and self.pitch_error > -0.5)and(self.throttle_error < 2.0 and self.throttle_error > -2.0 )) or self.b==1):

		  #This Is the Counter For Position Holding & This Checks If The Blue Flower Is Lit Or Not And Accordingly Moves TO The Next Point (Configuration Of Flower Can Be changed Accordingly)
                  if(self.go > 14 or self.b==1):
		    self.i = 2.0
		    self.go = 0.0
		  else :
                    self.go = self.go + 1
  	            time.sleep(0.1)

	     #This Is The Calculation Of Second Waypoint Error Values
             elif(self.i == 2.0 ):
                self.throttle_error = (self.Plant_location[2][2] - self.drone_z )
                if(((self.roll_error < 0.1 and self.roll_error > -0.1)and(self.pitch_error < 0.1 and self.pitch_error > -0.1)and(self.throttle_error < 2.0 and self.throttle_error > -2.0 ))or self.r==1):

		  #This Is the Counter For Position Holding & This Checks If The Red Flower Is Lit Or Not And Accordingly Moves TO The Next Point  
		  if(self.go > 4 or self.r==1):
                    self.i = 3.0
		    self.go = 0.0
		  else :
                    self.go = self.go + 1
  	            time.sleep(0.1)

	     #This Is The Calculation Of Third Waypoint Error Values
	     elif(self.i == 3.0):
                self.throttle_error = (self.Plant_location[3][2] - self.drone_z )
                if(((self.roll_error < 0.5 and self.roll_error > -0.5)and(self.pitch_error < 0.5 and self.pitch_error > -0.5)and(self.throttle_error < 2.0 and self.throttle_error > -2.0 ))or self.g==1):

		  #This Is the Counter For Position Holding & This Checks If The Green Flower Is Lit Or Not And Accordingly Moves TO The Next Point  
	          if(self.go > 12 or self.g==1):
                    self.i = 4.0
                    self.go = 0.0
		  else :
                    self.go = self.go + 1
 	            time.sleep(0.1)

	     #This Is The Bee-hive Location Error Calculation 
	     elif(self.i == 4.0):
		 self.throttle_error = (self.Bee_hive[0][2] - self.drone_z )
	         if((self.roll_error < 0.5 and self.roll_error > -0.5)and(self.pitch_error < 0.5 and self.pitch_error > -0.5)and(self.throttle_error < 2.0 and self.throttle_error > -2.0 )):
                 
       		       
                     self.disarm()

             
             self.pthrot = (self.kp_throt * self.throttle_error )
             self.intethrot = self.intethrot + (self.throttle_error/100)
             
             self.dthrot = 0.0
             
             self.derivthrot = ( ( self.throttle_error - self.previous_throttle_error ))
	       
             self.correct_throt  =  (self.pthrot ) + (  self.derivthrot * self.kd_throt )  + (  self.intethrot * self.ki_throt )
             self.previous_throttle_error  = self.throttle_error
                                       

	def limit(self, input_value, max_value, min_value):

		#This function limits the maximum and minimum values you send to your drone

		if input_value > max_value:
			return max_value
		if input_value < min_value:
			return min_value
		else:
			return input_value

	


	def set_pid_alt(self,pid_val):
		
		#This is the subscriber function to get the Kp, Ki and Kd values set through the GUI for Altitude

		self.kp_throt = pid_val.Kp
		self.ki_throt = pid_val.Ki
		self.kd_throt = pid_val.Kd

	def set_pid_roll(self,pid_val):

		#This is the subscriber function to get the Kp, Ki and Kd values set through the GUI for Roll

		self.kp_roll = pid_val.Kp
		self.ki_roll = pid_val.Ki
		self.kd_roll = pid_val.Kd
		
	def set_pid_pitch(self,pid_val):

		#This is the subscriber function to get the Kp, Ki and Kd values set through the GUI for Pitch

		self.kp_pitch = pid_val.Kp
		self.ki_pitch = pid_val.Ki
		self.kd_pitch = pid_val.Kd
		
	def set_pid_yaw(self,pid_val):

		#This is the subscriber function to get the Kp, Ki and Kd values set through the GUI for Yaw

		self.kp_yaw = pid_val.Kp
		self.ki_yaw = pid_val.Ki
		self.kd_yaw = pid_val.Kd
		
	def get_pose(self,pose):

		#This is the subscriber function to get the whycon poses
		#The x, y and z values are stored within the drone_x, drone_y and the drone_z variables
		
		self.drone_x = pose.poses[0].position.x
		self.drone_y = pose.poses[0].position.y
		self.drone_z = pose.poses[0].position.z

  	#This Function Takes The Value From '/red' Published Topic And Pass It To a Variable 
	def redIM(self, data1):
		self.r = 0
		self.r = data1
		#print self.r

 	#This Function Takes The Value From '/blue' Published Topic And Pass It To a Variable
	def blueIM(self, data2):
		self.b = 0
		self.b = data2

	#This Function Takes The Value From '/green' Published Topic And Pass It To a Variable
	def greenIM(self, data3):
		self.g = 0 
		self.g = data3


if __name__ == '__main__':
	while not rospy.is_shutdown():
		temp = DroneFly()
		temp.position_hold()
		rospy.spin()
