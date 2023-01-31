import gym
import numpy as np
from sac_torch import Agent
import matplotlib.pyplot as plt


if __name__ == "__main__":
    env = gym.make('MountainCarContinuous-v0')
    agent = Agent(agent_name="actor", input_dims=env.observation_space.shape, env=env, n_actions=env.action_space.shape[0])
    n_games = 250
    filename = 'MountainCar.png'

    figure_file = 'plots/' + filename

    best_score = env.reward_range[0]
    score_history = []
    load_checkpoint = True

    if load_checkpoint:
        agent.load_models()
        env.render(mode='human')

    for i in range(n_games):
        observation = env.reset()
        done = False
        score = 0
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.remember(observation, action, reward, observation_, done)
            if not load_checkpoint:
                agent.learn()
            observation = observation_
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score
            if not load_checkpoint:
                agent.save_models()
        
        print('episode', i, 'score %.1f' % score, 'avg_score %.1f' % avg_score)
    
    if not load_checkpoint:
        x = [i+1 for i in range(n_games)]
        plt.plot(x, score_history)
        plt.savefig(figure_file)