#!/usr/bin/env python
import rospy
import os
import datetime
from gopher_sentience_msgs.msg import Reality

class delivery_info:
  status = { 
    0 : 'bored', 
    1 : 'Parking', 
    2 : 'UnParking',
    3 : 'Docking',
    4 : 'Undoking',
    5 : 'Traveling',
    8 : 'Will_Depart',
    9  : 'Canceling',
    10 : 'Other',
    50 : 'For_Authentication',
    51 : 'For_Input',
    100 : 'Paused_Emergency',
    101 : 'Paused_By_User',
    200 : 'Error',
  }
  start_time = 0
  end_time = 0
  cnt = 0
  start_flag = True
  bored_flag = False

  def __init__(self):
    self.filename = datetime.datetime.now()
  
  def callback(self,msg):
    print(self.status[msg.status])
    
    if msg.status == 2:
      if self.start_flag == True:
        self.start_time = datetime.datetime.now()
        self.cnt += 1
        self.start_flag = False

    if msg.status == 1:
      self.end_time = datetime.datetime.now()
      self.bored_flag = True

    if msg.status == 0:
      if self.bored_flag == True:
        with open(os.getcwd() + "/delivery_file/" + str(self.filename), 'a') as deli:
          deli.write(str(self.cnt) + '\t' + str(self.end_time - self.start_time))
        self.bored_flag = False

      self.start_flag = True
      print(self.end_time - self.start_time)

    if msg.status == 200:
      print("ERROR")
   
if __name__ == "__main__":
  rospy.init_node('delivery_info', anonymous=True)  
  delivery = delivery_info()
  if not os.path.exists(os.getcwd() + "/delivery_file"):
    os.makedirs(os.getcwd() + "/delivery_file")
  
  while not rospy.is_shutdown():
    rospy.Subscriber('/sentience/reality', Reality, delivery.callback)
    rospy.spin()