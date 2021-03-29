import sys
import time
import threading
import itertools


class Spinner:
  busy = False
  delay = 0.1
  iterable = itertools.cycle(list('⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'))

  def __init__(self, delay=0.1, desc=''):
    self.desc = desc
    self.delay = delay

  def spinner_task(self):
    while self.busy:
      sys.stdout.write('\r')
      sys.stdout.flush()
      sys.stdout.write(f'{next(self.iterable)} {self.desc}...')
      sys.stdout.flush()
      time.sleep(self.delay)

  def __enter__(self):
    self.busy = True
    threading.Thread(target=self.spinner_task).start()

  def __exit__(self, exception, value, tb):
    self.busy = False
    time.sleep(self.delay)
    if exception is not None:
      sys.stdout.write('\r')
      sys.stdout.flush()
      print(f'✖️ {self.desc} failed')
      return False
    else:
      sys.stdout.write('\r')
      sys.stdout.flush()
      print(f'✔️ {self.desc}   ')
