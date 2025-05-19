
import os
import sys
import datetime
import multiprocessing



if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")
import numpy as np
import pandas as pd
import ray
import traci
from supersuit import pad_observations_v0
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
from ray.tune.registry import register_env

import sumo_rl

path = os.path.dirname(__file__)

env = sumo_rl.parallel_env(net_file=os.path.join(path, '../sumo_maps/small_two/quickstart.net.xml'),
                  route_file=os.path.join(path, '../sumo_maps/small_two/routes.rou.xml'),
                  out_csv_name= os.path.join(path, "outputs/small3x2/ppo"),
                  use_gui=False,
                  num_seconds=8000)

env = pad_observations_v0(env) # Use supersuit to pad observation space

observations = env.reset()

if __name__ == "__main__":
    
    env_name = "small3x2"
    ray.init()
    register_env(
    env_name,
    lambda _: ParallelPettingZooEnv(env))

    print(f"Num CPU's: {multiprocessing.cpu_count()}")

    config = (
        PPOConfig()
        .environment(env=env_name, disable_env_checking=True)
        .rollouts(num_rollout_workers=multiprocessing.cpu_count()-1, rollout_fragment_length='auto')
        .training(
            train_batch_size=512,
            lr=2e-5,
            gamma=0.95,
            lambda_=0.9,
            use_gae=True,
            clip_param=0.4,
            grad_clip=None,
            entropy_coeff=0.1,
            vf_loss_coeff=0.25,
            sgd_minibatch_size=64,
            num_sgd_iter=10,
        )
        .debugging(log_level="ERROR")
        .framework(framework="torch")
        .resources(num_gpus=int(os.environ.get("RLLIB_NUM_GPUS", "0")))
    )

    tune.run(
        "PPO",
        name="PPO",
        stop={"timesteps_total": 100000},
        checkpoint_freq=10,
        storage_path=os.path.join(path, "ray_results/" + env_name + f"/{datetime.datetime.now()}"),
        config=config.to_dict(),
    )


#while env.agents:
#    actions = {agent: env.action_space(agent).sample() for agent in env.agents}  # this is where you would insert your policy
#    observations, rewards, terminations, truncations, infos = env.step(actions)