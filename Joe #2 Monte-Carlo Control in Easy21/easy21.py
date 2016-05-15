from enum import Enum
import copy
import random
random.seed(1)



class State:
    def __init__(self, dealer_card, player_card, is_terminal=False):
        """
        :type self.is_terminal: bool
        :type self.dealer: int
        :type self.player: int
        """
        self.dealer = dealer_card.value
        self.player = player_card.value
        self.term = is_terminal
        self.r = 0


class Card:
    def __init__(self, force_black=False):
        """
        :type self.value: int
        """

        self.value = random.randint(1,10)
        self.absolute_value = self.value
        if force_black or random.randint(1,3) != 1:
            self.is_black = True
        else:
            self.is_black = False
            self.value = 0 - self.value
        self.is_red = not self.is_black


class Actions(Enum):

    # Possible actions
    hit = 0
    stick = 1

    @staticmethod
    def to_action(n):
        return Actions.hit if n==0 else Actions.stick

    @staticmethod
    def as_int(a):
        return 0 if a == Actions.hit else 1


class Environment:
    def __init__(self):
        self.player_values_count = 21
        self.dealer_values_count = 10
        self.actions_count = 2 # number of possible actions

    def get_start_state(self):
        s = State(Card(True), Card(True))
        return s


    def step(self, s, a):
        # type: (object, object) -> object
        """

        :type s: State
        """
        next_s = copy.copy(s)
        r = 0
        if a == Actions.stick:
            while not next_s.term:
                next_s.dealer += Card().value
                if next_s.dealer < 1 or next_s.dealer > 21:
                    next_s.term = True
                    r = 1
                elif next_s.dealer >= 17:
                    next_s.term = True
                    if next_s.dealer > next_s.player:
                        r = -1
                    elif next_s.dealer < next_s.player:
                        r = 1
        else:
            next_s.player += Card().value
            if next_s.player < 1 or next_s.player > 21:
                next_s.term = True
                r = -1
        next_s.r = r
        return next_s, r
