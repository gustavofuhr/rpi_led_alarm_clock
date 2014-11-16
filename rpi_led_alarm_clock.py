import RPi.GPIO as GPIO
import yaml
import sched, time
from datetime import datetime


def time_now():
	d = datetime.now()
	stime = str(d.hour) + ":" + str(d.minute)
	FMT = '%H:%M'
	return datetime.strptime(stime, FMT) 



class RpiLedAlarmClock:
	def __init__(self, config_filename = './config.yaml'):
		self.read_config(config_filename)


	def read_config(self, config_filename):

		with open(config_filename) as stream:
			yconfig = yaml.load(stream)
			try:
				settings = yconfig['alarm_settings'];
				self.hour = settings['hour']
				self.gpio_pin = settings['gpio_pin']
				self.play_song = settings['play_song']
				if self.play_song:
					print('Gonna play songs...')
					self.song_file = settings['song_settings']['song_file']
			except Exception as err:
				print('Problem reading the configuration file..')
				raise err;
			

	def turn_on_LED(self, how_long = 60*60*4):
		channel = self.gpio_pin

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(channel, GPIO.OUT)
		GPIO.output(channel, GPIO.HIGH)

		if how_long != -1: # -1 is forever
			time.sleep(how_long)
			GPIO.cleanup()


	def wakeup(self):
		print('Wake up pretty girl!')
		self.turn_on_LED()


	def activate(self):
		print('Waiting for wakeup hour...')
		s = sched.scheduler(time.time, time.sleep)

		FMT = '%H:%M'
		tdelta = datetime.strptime(self.hour, FMT) - time_now()
		seconds2wait = tdelta.total_seconds()
		
		s.enter(seconds2wait, 1, self.wakeup, ())
		s.run()

		



