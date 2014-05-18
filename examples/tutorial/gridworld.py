#!/usr/bin/env python
"""
Getting Started Tutorial for RLPy
=================================

This file contains a very basic example of a RL experiment:
A simple Grid-World.
"""
__author__ = "Robert H. Klein"
from rlpy.Domains import GridWorld
from rlpy.Agents import Q_Learning
from rlpy.Representations import Tabular
from rlpy.Policies import eGreedy
from rlpy.Experiments import Experiment
import os


def make_experiment(id=1, path="./Results/Tutorial/gridworld-qlearning"):
    """
    Each file specifying an experimental setup should contain a
    make_experiment function which returns an instance of the Experiment
    class with everything set up.

    @param id: number used to seed the random number generators
    @param path: output directory where logs and results are stored
    """

    # Domain:
    maze = os.path.join(GridWorld.default_map_dir, '4x5.txt')
    domain = GridWorld(maze, noise=0.3)

    # Representation
    representation = Tabular(domain, discretization=20)

    # Policy
    policy = eGreedy(representation, epsilon=0.2)

    # Agent
    agent = Q_Learning(representation=representation, policy=policy,
                       domain=domain,
                       initial_learn_rate=0.1,
                       learn_rate_decay_mode="boyan", boyan_N0=100,
                       lambda_=0.)
    checks_per_policy = 100
    max_steps = 2000
    num_policy_checks = 10
    experiment = Experiment(**locals())
    return experiment

if __name__ == '__main__':
    experiment = make_experiment(1)
    experiment.run(visualize_steps=False,  # should each learning step be shown?
                   visualize_learning=True,  # show policy / value function?
                   visualize_performance=1)  # show performance runs?
    experiment.plot()
    experiment.save()
