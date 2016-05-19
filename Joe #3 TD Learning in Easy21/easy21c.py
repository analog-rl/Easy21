from enum import Enum
import copy
import random
import numpy as np
from matplotlib import cm
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

    def dealer_idx(self):
        return self.dealer - 1

    def player_idx(self):
        return self.player - 1


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
        return next_s, r


class MC_Agent:
    def __init__(self, environment, n0):
        self.n0 = float(n0)
        self.env = environment

        # N(s) is the number of times that state s has been visited
        # N(s,a) is the number of times that action a has been selected from state s.
        self.N = np.zeros((self.env.dealer_values_count,
                           self.env.player_values_count,
                           self.env.actions_count))

        self.Q = np.zeros((self.env.dealer_values_count,
                           self.env.player_values_count,
                           self.env.actions_count))
        # self.E = np.zeros((self.env.dealer_values_count,
        #                    self.env.player_values_count,
        #                    self.env.actions_count))

        # Initialise the value function to zero.
        self.V = np.zeros((self.env.dealer_values_count, self.env.player_values_count))

        self.count_wins = 0
        self.iterations = 0

    #     def get_action(self, s):
    #         a = Actions.hit
    #         return a

    # get optimal action, with epsilon exploration (epsilon dependent on number of visits to the state)
    def train_get_action(self, state):
        dealer_idx = state.dealer - 1
        player_idx = state.player - 1
        n_visits = sum(self.N[dealer_idx, player_idx, :])

        # epsilon = N0/(N0 + N(st)
        curr_epsilon = self.n0 / (self.n0 + n_visits)

        # epsilon greedy policy
        if random.random() < curr_epsilon:
            r_action = Actions.hit if random.random() < 0.5 else Actions.stick
            #             if (dealer_idx == 0 and player_idx == 0):
            #                 print ("epsilon:%s, random:%s " % (curr_epsilon, r_action))
            return r_action
        else:
            action = Actions.to_action(np.argmax(self.Q[dealer_idx, player_idx, :]))
            #             if (dealer_idx == 0 and player_idx == 0):
            #                 print ("epsilon:%s Qvals:%s Q:%s" % (curr_epsilon, self.Q[dealer_idx, player_idx, :], action))
            return action

    def train(self, iterations):

        # Loop episodes
        for episode in xrange(iterations):
            episode_pairs = []

            # get initial state for current episode
            s = self.env.get_start_state()

            # Execute until game ends
            while not s.term:
                # get action with epsilon greedy policy
                a = self.train_get_action(s)

                # store action state pairs
                episode_pairs.append((s, a))

                # update visits
                # N(s) is the number of times that state s has been visited
                # N(s,a) is the number of times that action a has been selected from state s.
                self.N[s.dealer - 1, s.player - 1, Actions.as_int(a)] += 1

                # execute action
                s, r = self.env.step(s, a)

            # if episode%10000==0: print "Episode: %d, Reward: %d" %(episode, my_state.rew)
            self.count_wins = self.count_wins + 1 if r == 1 else self.count_wins

            # Update Action value function accordingly
            for curr_s, curr_a in episode_pairs:
                # print s.dealer, s.player, s.r, a
                dealer_idx = curr_s.dealer - 1
                player_idx = curr_s.player - 1
                action_idx = Actions.as_int(curr_a)

                # Use a time-varying scalar step-size of at = 1/N(st,at)
                #                 step = 1.0 / sum(self.N[dealer_idx, player_idx, :])
                step = 1.0 / self.N[dealer_idx, player_idx, action_idx]
                error = r - self.Q[dealer_idx, player_idx, action_idx]
                self.Q[dealer_idx, player_idx, action_idx] += step * error

        self.iterations += iterations
        print float(self.count_wins) / self.iterations * 100

        # Derive value function
        for d in xrange(self.env.dealer_values_count):
            for p in xrange(self.env.player_values_count):
                self.V[d, p] = max(self.Q[d, p, :])

    def plot_frame(self, ax):
        def get_stat_val(x, y):
            return self.V[x, y]

        X = np.arange(0, self.env.dealer_values_count, 1)
        Y = np.arange(0, self.env.player_values_count, 1)
        X, Y = np.meshgrid(X, Y)
        Z = get_stat_val(X, Y)
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        return surf

