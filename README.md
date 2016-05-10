# Easy21
Reinforcement Learning Assignment: Easy21

from: http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching.html

Sections
- [x] #1-Implementation of Easy21
- [ ] #2 Monte-Carlo Control in Easy21
- [ ] #3 TD Learning in Easy21
- [ ] #4 Linear Function Approximation in Easy21
- [ ] #5 Discussion




# #1-Implementation of Easy21
You should write an environment that implements the game Easy21. Specifi- cally, write a function, named step, which takes as input a state s (dealer’s first card 1–10 and the player’s sum 1–21), and an action a (hit or stick), and returns a sample of the next state s′ (which may be terminal if the game is finished) and reward r. We will be using this environment for model-free reinforcement learning, and you should not explicitly represent the transition matrix for the MDP. There is no discounting (γ = 1). You should treat the dealer’s moves as part of the environment, i.e. calling step with a stick action will play out the dealer’s cards and return the final reward and terminal state.

10 marks

see #1-Implementation of Easy21.ipynb

# #2 Monte-Carlo Control in Easy21
Apply Monte-Carlo control to Easy21. Initialise the value function to zero. Use a time-varying scalar step-size of αt = 1/N(st,at) and an ε-greedy exploration strategy with εt = N0/(N0 + N(st)), where N0 = 100 is a constant, N(s) is the number of times that state s has been visited, and N(s,a) is the number of times that action a has been selected from state s. Feel free to choose an alternative value for N0, if it helps producing better results. Plot the optimal value function V ∗ (s) = maxa Q∗ (s, a) using similar axes to the following figure taken from Sutton and Barto’s Blackjack example.

15 marks

# #3 TD Learning in Easy21
Implement Sarsa(λ) in 21s. Initialise the value function to zero. Use the same step-size and exploration schedules as in the previous section. Run the algorithm with parameter values λ ∈ {0, 0.1, 0.2, ..., 1}. Stop each run after 1000 episodes and report the mean-squared error  s,a(Q(s, a) − Q∗(s, a))2 over all states s and actions a, comparing the true values Q∗(s,a) computed in the previous section with the estimated values Q(s, a) computed by Sarsa. Plot the mean- squared error against λ. For λ = 0 and λ = 1 only, plot the learning curve of mean-squared error against episode number.

15 marks

# #4 Linear Function Approximation in Easy21
We now consider a simple value function approximator using coarse coding. Use a binary feature vector φ(s, a) with 3 ∗ 6 ∗ 2 = 36 features. Each binary feature has a value of 1 iff (s, a) lies within the cuboid of state-space corresponding to that feature, and the action corresponding to that feature. The cuboids have the following overlapping intervals:
dealer(s) = {[1, 4], [4, 7], [7, 10]}
player(s) = {[1, 6], [4, 9], [7, 12], [10, 15], [13, 18], [16, 21]}
a = {hit, stick}
where
• dealer(s) is the value of the dealer’s first card (1–10) • sum(s) is the sum of the player’s cards (1–21)
Repeat the Sarsa(λ) experiment from the previous section, but using linear value function approximation Q(s, a) = φ(s, a)⊤θ. Use a constant exploration of ε = 0.05 and a constant step-size of 0.01. Plot the mean-squared error against λ. For λ = 0 and λ = 1 only, plot the learning curve of mean-squared error against episode number.

# #5 Discussion
Discuss the choice of algorithm used in the previous section.
• What are the pros and cons of bootstrapping in Easy21?
• Would you expect bootstrapping to help more in blackjack or Easy21? Why?
• What are the pros and cons of function approximation in Easy21?
• How would you modify the function approximator suggested in this section
to get better results in Easy21?

15 marks
