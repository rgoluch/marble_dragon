# USAGE
# python client.py --server-ip SERVER_IP

# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time
import cv2
import requests as r

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
	help="ip address of the server to which the client will connect")
ap.add_argument("-c", "--camera-ip", required=True, help="ip address of the camera on the local network to get a feed from")
args = vars(ap.parse_args())

# initialize the ImageSender object with the socket address of the
# server

sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
	args["server_ip"]))

cameras = r.get("http://3.14.117.253:5000/camera")
camera_ip = []
camera_name = []

for c in cameras.json():
	camera_ip.append(c['ip'])
	camera_name.append(c['nickname'])

while True:
	# read the frame from the camera and send it to the server
	for i,j in zip(camera_ip, camera_name):
		rpiName = j
		feed = cv2.VideoCapture("http://" + str(i) + "/video.mjpg")
		if len(feed) > 0:
			time.sleep(2.0)
			ret, frame = feed.read()
			print(i)
			i+=1
			sender.send_image(rpiName, frame)