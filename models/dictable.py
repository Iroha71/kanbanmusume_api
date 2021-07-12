from abc import ABCMeta, abstractmethod
class Dictable(metaclass=ABCMeta):
  @abstractmethod
  def to_dict(self):
    pass