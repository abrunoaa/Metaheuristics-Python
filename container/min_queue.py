from collections import deque


class MinQueue:
  def __init__(self):
    self.data = deque()

  def min(self):
    return self.data[0][0]

  def push(self, x):
    k = 1
    while len(self.data) > 0 and x <= self.data[-1][0]:
      k += self.data[-1][1]
      self.data.pop()
    self.data.append([x, k])

  def pop(self):
    if self.data[0][1] == 1:
      self.data.popleft()
    else:
      self.data[0][1] -= 1
