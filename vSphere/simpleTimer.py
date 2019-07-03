

## @file Timer.py
## @brief Simple timer utility to calculate the time interval for certain function

import time

class Timer:
   def __enter__(self):
      self.start = time.time()

   def __exit__(self, *args):
      self.end = time.time()
      self.interval = self.end - self.start

   def reset(self):
      self.interval = 0

   def start(self):
      self.start = time.time()

   def stop(self):
      self.end = time.time()
      self.interval = self.end - self.start

   def getInterval(self):
      return self.interval

