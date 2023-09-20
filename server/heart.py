import datetime

ACTIVITY_THRESHOLD = datetime.timedelta(seconds=120)

class Heart:
    _instance = None  # Private class-level variable to hold the singleton instance

    def __new__(cls):
        # Check if an instance already exists, and if not, create one
        if cls._instance is None:
            cls._instance = super(Heart, cls).__new__(cls)
            cls._instance.initial_timestamp = datetime.datetime.now()
            cls._instance.latest_timestamp = None
            cls._instance.flat_line = True
        return cls._instance

    def beat(self):
        if self.flat_line:
            self.initial_timestamp = datetime.datetime.now()
        
        self.latest_timestamp = datetime.datetime.now()
        self.flat_line = False

    def update_status(self):
        if not self.flat_line:
            curr_time = datetime.datetime.now()
            time_diff = curr_time - self.latest_timestamp
            print(time_diff)
            if time_diff > ACTIVITY_THRESHOLD:
                self.flat_line = True
                self.initial_timestamp = curr_time
                print(f"Flat Line at: ")
                print(datetime.datetime.now())







