from abc import ABC, abstractmethod


class Interactable(ABC):
    @abstractmethod
    def interact(self, player: "Player"):
        """

        :return:
        """
        raise NotImplementedError()
