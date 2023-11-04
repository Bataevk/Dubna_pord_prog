import psutil
import matplotlib.pyplot as plt
from time import sleep
import threading
import os

run_flag = True

cpu_history = [0]*100
ram_history = [0]*100

def update():
	global run_flag
	while run_flag:
		cpu_history.append(psutil.cpu_percent())
		cpu_history.pop(0)

		ram_history.append(psutil.virtual_memory().percent)
		ram_history.pop(0)

		sleep(0.5)

def stop_thread():
	global run_flag
	run_flag = False

def start_thread():
	update_thread = threading.Thread(target=update)
	update_thread.start()


def create_image():
	fig = plt.figure(figsize=(6, 7))
	fig.add_subplot(2, 2, 2)
	plt.plot(ram_history)
	plt.xlabel('Ram usage')
	plt.ylim([0, 100])

	fig.add_subplot(2, 1, 2)
	plt.plot(cpu_history)
	plt.xlabel('Cpu usage')
	plt.ylim([0, 100])

	fig.add_subplot(2, 2, 1)
	disk = psutil.disk_usage(os.getcwd())
	plt.pie([disk.used, disk.free])
	plt.xlabel('Disk usage')

	#plt.show()
	plt.savefig('system.png')


