#!/usr/bin/env python
'''
Team ID: 3984
Author List: Nishan Poojary
FileName: Image Processing 
Theme: Pollinator Bot
Functions: __init__(self), image_callback(self,msg):
Global Variables: red, green, blue, redcount, greencount & bluecount 	  
'''
import rospy, cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import	Image
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Int32
from std_msgs.msg import Float64
#Global Variable Declaration 
red = 0.0
green = 0.0
blue = 0.0
redcount = 0.0
greencount = 0.0
bluecount = 0.0
i=0.0
j=0.0
k=0.0
l=0.0
class WayPoint:
    	
	def __init__(self):

		# Creation Of ROS Bridge
		rospy.init_node('ros_bridge')
		self.ros_bridge = cv_bridge.CvBridge()

		# Subscribe to whycon image_out
		self.image_sub = rospy.Subscriber('/whycon/image_out', Image, self.image_callback)
		
		#Creating Publisher Varables For Publishing The Count Of Red, Blue & Green Contours  
		self.pub1 = rospy.Publisher('/red', Float64 ,queue_size=10)
                self.pub2 = rospy.Publisher('/blue', Float64  , queue_size=10)
                self.pub3 = rospy.Publisher('/green', Float64 , queue_size=10)
		print'START'
		self.i=1.0
                self.j=1.0
                self.k=1.0
		self.l=1.0
		#print greencount  
                
	#Image Processing Algorithm To Detect Red, Blue & Green Objects  		
	def image_callback(self,msg):
            global i
	    global red
            global green
            global blue
            global redcount
	    global greencount
	    global bluecount
            global j
	    global k	
            global l        
	    if(self.l==1.0):	
	      	#Using RosBridge For Converting Subscribed Image Into OpenCV frame  
		image = self.ros_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
                #This cv2.cvtColor() Converts Blue Green Image From Frame To HSV
                hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
		#blue_lower, blue_upper & green_lower, green_upper & red_lower, red_upper are Lower And Upper HSV Values For Blue, Green & Red Respectively 
		#These Lower And Upper Values Are Passed To The np.array 
  		blue_lower = np.array([110,50,50],np.uint8)
  		blue_upper = np.array([130,255,255],np.uint8)
  		green_lower = np.array([50,50,50],np.uint8)
  		green_upper = np.array([70,255,255],np.uint8)
  		red_lower = np.array([136,87,111],np.uint8)
  		red_upper = np.array([180,255,255],np.uint8)

  		kernal = np.ones((5,5),"uint8")
		#This CV2.InRange() Detects Colours Between blue_lower & blue_upper
  		blue = cv2.inRange(hsv,blue_lower,blue_upper)
		#CV2.Dilate() Dilates The Colour 
  		blue = cv2.dilate(blue,kernal)
		#CV2.Bitwise_and() Shows Colour Blue 
  		res = cv2.bitwise_and(image,image,mask= blue)
		#Below Line Find's Contour 
  		_, contours,hierarchy = cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                for pic, contour in enumerate(contours):
		#The Below Line Find's Contour Area
                    area = cv2.contourArea(contour)
                    if(area>300 ):
   		#These Below Variables Are Bounding Variables 
                      x,y,w,h = cv2.boundingRect(contour)
		#This Below Line Draws Rectangle Of Colour Blue And Of Width '2' 
                      image = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                      bluecount = bluecount + 1.0
		      if (bluecount > 1.0 ):
                       bluecount = 1.0
		      if(bluecount==1.0 and self.j==1.0):	
		          print 'Pollinated ',bluecount ,'Blue Delphinium'
                          
		          self.j=self.j+1.0  
		#This CV2.InRange() Detects Colours Between green_lower & green_upper        
  		green = cv2.inRange(hsv,green_lower,green_upper) 
		#CV2.Dilate() Dilates The Colour
 	 	green = cv2.dilate(green,kernal)
		#CV2.Bitwise_and() Shows Colour Green
  		res1 = cv2.bitwise_and(image,image,mask= green)
		#Below Line Find's Contour
  		_, contours,_ = cv2.findContours(green,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                for pic, contour in enumerate(contours):
        	 area = cv2.contourArea(contour)
        	 if(area>300):
            	#These Below Variables Are Bounding Variables
          	   x,y,w,h = cv2.boundingRect(contour)
		#This Below Line Draws Rectangle Of Colour Green And Of Width '2'
         	   image = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
		   greencount = greencount + 1.0
	           if (greencount > 1.0 ):
                       greencount = 1.0
		   if(greencount==1 and self.i ==1.0):
		       print 'Pollinated ',greencount,' Green Carnation'
                       
		       self.i = self.i+1.0
		#This CV2.InRange() Detects Colours Between red_lower & red_upper
         	red = cv2.inRange(hsv,red_lower,red_upper)
		#CV2.Dilate() Dilates The Colour
  		red = cv2.dilate(red,kernal)
		#CV2.Bitwise_and() Shows Colour Red
  		res2 = cv2.bitwise_and(image,image,mask= red) 
		#Below Line Find's Contour
  		_, contours,hierarchy = cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  
                for pic, contour in enumerate(contours):
          	   area = cv2.contourArea(contour)
         	   if(area>300):
            	#These Below Variables Are Bounding Variables
                     x,y,w,h = cv2.boundingRect(contour)
		#This Below Line Draws Rectangle Of Colour Red And Of Width '2'
                     image = cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
                     redcount =  redcount + 1.0
		     if (redcount > 1.0 ):
                       redcount = 1.0
		    
	             if(redcount==1 and self.k ==1.0):
		       print 'Pollinated ',redcount,'Red Daylily'
                       #print redcount
		       self.k = self.k+1.0		
                     #print 'Pollination Done!',redcount,'Red Daylily'
		#Output Video
  		cv2.imshow('Video',image)
                
                
     		#Publishing The Count Of Red , Blue & Green Contour
                self.pub1.publish(redcount)
        	self.pub2.publish(bluecount)
       	 	self.pub3.publish(greencount)	
		
                if cv2.waitKey(32) == ord('q'):
                    
		    print 'Pollination Done! Pollinated',redcount,'Red Daylily',greencount,'Green Carnation and',bluecount,'Blue Delphinium'
		    print 'STOP'
		    cv2.destroyAllWindows()
	            self.l=self.l+1.0
		    
		    
	        
if __name__ == '__main__':
	test = WayPoint()
	#test.image_callback()
       #	global redcount
#	global greencount
#	global bluecount	

	rospy.spin()
		
