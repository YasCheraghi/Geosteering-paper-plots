import numpy as np


class PlayerRound:
    def __init__(self, player_name, round_id, virt_proj_id):
        self.player_name = player_name
        self.round_id = round_id
        self.virtual_proj_id = virt_proj_id
        self.interpretation_id_list = [] 
        self.trajectories = {}
        self.interpretation_dict = {}
        self.target_lines = {}

    def append_trajectory(self, traj_ver_id, trajectory):
        if traj_ver_id in self.trajectories:
            print('Trajectory already added warning')
            # exit(1)
        self.trajectories[traj_ver_id] = trajectory

    def append_interpretation(self, interp_id, interpretation_ver, traj_version_id, interpretation):
        if (interp_id, interpretation_ver) in self.interpretation_dict:
            print('Interpretation already added warning')
            # exit(1)
        self.interpretation_dict[(interp_id, interpretation_ver)] = interpretation
        self.interpretation_id_list.append((interp_id, interpretation_ver))






