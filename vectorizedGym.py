import gym
import torch as torch
import numpy as np

class VectorizedGym():

    def __init__(self):
        self.envs = gym.vector.SyncVectorEnv([
            lambda: gym.make("Pendulum-v1", g=9.9),
            lambda: gym.make("Pendulum-v1", g=9.7),
            lambda: gym.make("Pendulum-v1", g=9.81)
        ])
        self.obs_i = self.envs.reset()
        self.num_ensemble = 3
        self.num_sim = 2
        self.num_real = 1
    
    def take_actions(self,actions):
        a_sim = [[float(actions[0])]]
        a_real = [[float(actions[1])]]
        a = np.asarray(a_sim*self.num_sim+a_real*self.num_real)
        print(a)
        obs,reward,done,info = self.envs.step(a)
        return obs,reward,done,info





            
    
