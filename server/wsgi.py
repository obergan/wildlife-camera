from server import app
from server import scheduler

if __name__ == "__main__":
	scheduler.start()
	app.run()
