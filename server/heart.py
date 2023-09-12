import datetime

ACTIVITY_THRESHOLD = datetime.timedelta(seconds=120)

class Heart:
    def __init__(self):
        self.initial_timestamp = datetime.datetime.now()
        self.latest_timestamp = None
        self.flat_line = True

    def beat(self):
        
        if self.flat_line:
            # Camera have been inactive for a while
            self.initial_timestamp = datetime.datetime.now() 
        
        # Camera is currently active
        self.latest_timestamp = datetime.datetime.now()
        
        self.flat_line = False
            
    def update_status(self):
        
        # active status
        if not self.flat_line:
            curr_time = datetime.datetime.now()
            time_diff = curr_time - self.latest_timestamp
            print(time_diff)
            if time_diff > ACTIVITY_THRESHOLD:
                # camera dead
                self.flat_line = True
                self.initial_timestamp = curr_time
                print(f"Flat Line at: ")
                print(datetime.datetime.now())

