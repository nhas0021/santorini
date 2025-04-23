from abc import ABC, abstractmethod

class God(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def modify_move(self, worker, board):
        """modify movement behavior."""
        pass

    @abstractmethod
    def modify_build(self, worker, board):
        """modify building behavior."""
        pass


class Artemis(God):
    def __init__(self):
        super().__init__(
            name="Artemis",
            description="Your Worker may move one additional time, but not back to its initial space."
        )

    def modify_move(self, worker, board):
        pass

    def modify_build(self, worker, board):
        pass


class Demeter(God):
    def __init__(self):
        super().__init__(
            name="Demeter",
            description="Your Worker may build one additional time, but not on the same space."
        )

    def modify_move(self, worker, board):
        pass

    def modify_build(self, worker, board):
        pass
