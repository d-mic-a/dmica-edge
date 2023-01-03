import gi
from time import sleep
import sys

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib


Gst.init()

def main(argv):
	ip = argv[1]
	port = argv[2]
	
	main_loop = GLib.MainLoop()
	main_loop.run()
	
	pipe_opt = "v4l2src device=/dev/video0 num-buffers=-1 ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host={} port={}".format(ip, port)
	pipeline = Gst.parse_launch(pipe_opt)
	pipeline.set_state(Gst.State.PLAYING)
	
	
	try:
		while True:
			sleep(0.1)
	except KeyboardInterrupt:
		pass
	
	pipeline.set_state(Gst.State.NULL)

main(sys.argv)
