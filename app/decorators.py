from threading import Thread

#multi-threading program wrapper funciton 
def async(f):
	def wrapper(*args, **kwargs):
		thr=Thread(target=f,args=args,kwargs=kwargs)
		thr.start()
	return wrapper