import numpy as np
import pandas as pd
import gzip
import json
import player
import well_point_converter as point_converter
import interpretation_converter
import plotting_utility
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None) 


projects_file_name = '//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Working Folder/GWC_2021_diffs/GWC_2021_virtual_projects.csv'
entities_file_name = '//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Working Folder/GWC_2021_diffs/GWC_2021_virtual_project_entities.csv'
lateral_wells_file_name = '//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Working Folder/solo_wells_aud_filtered.csv'
interpretations_file_name = '//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Working Folder/solo_interpretations_aud_filtered.csv' 


players_file_name = 'players.csv'
diff_dir = '//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Working Folder/GWC_2021_diffs'
data_dir = '//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Working Folder/GWC'
laterals_dir = 'laterals'
interpretations_dir = 'assembledSegments'
id_stage_1 = 'a1020470-11a2-4eac-906b-f574fd3bda31'
id_stage_2 = 'b4f4a165-8ea0-447a-bf47-6118c330a475'

revision_history_file_name = 'solo_revisions_history.csv'


def get_one_target_line(project_id, revision_id):
    pass


def get_all_lateral_trajectories(laterals_pairs_df, stage_id, player_to_add=None):
    for index, row in laterals_pairs_df.iterrows():
        single_handle = row
        print(single_handle)
        my_dir = data_dir+'/'+stage_id+'/'+laterals_dir+'/'+single_handle['uuid']
        my_file = str(single_handle['trajectory_version'])+'.lateral'
        full_filename = my_dir + '/' + my_file

        with gzip.open(full_filename, 'rb') as file:
            data = file.read()
            data_json = json.loads(data)
            world_points = point_converter.convert_well_points(data_json)
            trajectory = point_converter.LateralWell(well_points=world_points, timestamp=row['revend_tstmp'])
            if player_to_add is not None:
                player_to_add.append_trajectory(traj_ver_id=single_handle['trajectory_version'], trajectory=trajectory)


def get_all_interpretations(interpretation_pairs_df, stage_id, player_to_add=None):
    # to be found in solo_interpretations_aud
    # look for ['rev']
    # this one is less straight-forward
    for index, row in interpretation_pairs_df.iterrows():
        single_handle = row
        # print(single_handle)
        my_dir = data_dir+'/'+stage_id+'/'+interpretations_dir+'/'+single_handle['uuid']
        my_file = str(single_handle['interpretation_version'])+'.assembledSegment'
        full_filename = my_dir + '/' + my_file
        print(single_handle['uuid'])
        with gzip.open(full_filename, 'rb') as file:
            data = file.read()
            data_json = json.loads(data)
            resulting_interpretation = interpretation_converter.convert_interpretation(data_json)
            resulting_interpretation.timestamp = row['revend_tstmp']

            if player_to_add is not None:
                # player_to_add.append_interpretation(resulting_interpretation)
                player_to_add.append_interpretation(interpretation=resulting_interpretation,
                                                    interp_id=single_handle['uuid'],
                                                    interpretation_ver=single_handle['interpretation_version'],
                                                    traj_version_id=single_handle['trajectory_version']
                                                    )
            # print('found', full_filename)


def get_all_lateral_trajectory_versions(lateral_id):
    lateral_well_data = pd.read_csv(lateral_wells_file_name)
    data_for_current_id = lateral_well_data[lateral_well_data['uuid'] == lateral_id]
    revisions = data_for_current_id[['uuid', 'trajectory_version', 'revend_tstmp']]
    return revisions


def get_all_interpetation_versions(interp_id):
    interpretation_data = pd.read_csv(interpretations_file_name)
    data_for_current_id = interpretation_data[interpretation_data['well_id'] == interp_id]
    revisions = data_for_current_id[['uuid', 'interpretation_version', 'well_id', 'trajectory_version', 'revend_tstmp']]
    return revisions


def get_lateral(virtual_project_id):
    entities_data = pd.read_csv(entities_file_name)
    lateral_entites = entities_data[entities_data["object_type"] == 'laterals']
    laterals_for_project = lateral_entites[lateral_entites['virtual_project_uuid'] == virtual_project_id]
    lateral_id = laterals_for_project['object_uuid']
    assert len(lateral_id) == 1
    return lateral_id.values[0]


def get_virtual_project_id(player_number, stage_id):
    vps_data = pd.read_csv(projects_file_name)
    players_vps = vps_data[vps_data['name'] == 'Player #{:03d}'.format(player_number)]
    relevant_vp = players_vps[players_vps['project_uuid'] == stage_id]
    uuid = relevant_vp['uuid'].values[0]
    player_round = player.PlayerRound('Player #{:03d}'.format(player_number), stage_id, uuid)
    return player_round


def get_player_by_number_and_round_id(player_index, round_id):
    players_data = pd.read_csv(players_file_name)
    player_description = players_data.iloc[player_index]
    player_id_num = player_description['id']
    print(player_id_num) 
    revision_data = pd.read_csv(diff_dir+'/'+revision_history_file_name)
    # revision_data['proper_time_stamp'] = pd.to_datetime(revision_data['revstmp'].str.strip()[:-3],
    #                                                     format='%Y-%m-%d %H:%M:%S.%f')
    rev_data_user = revision_data[revision_data['user_id'] == player_id_num]
    rev_data_user_round = rev_data_user[rev_data_user['project_uuid'] == round_id]
    rev_data_correct_interval = rev_data_user_round[rev_data_user_round['revstmp'] >= '2021-09-15 12:00:00.000000']
    rev_data_correct_interval = rev_data_correct_interval[rev_data_correct_interval['revstmp'] <=
                                                          '2021-09-16 00:00:00.000000']
    print(rev_data_correct_interval['revision'].to_numpy())

    for index, row in rev_data_correct_interval.iterrows():
        print(index)


if __name__ == '__main__':
    # here is the main script
    cur_stage_id = id_stage_2
    player_round_6 = get_virtual_project_id(350, stage_id=cur_stage_id)
    print('virtual project id', player_round_6.virtual_proj_id)
    lateral_id = get_lateral(player_round_6.virtual_proj_id)
    print('lateral object', lateral_id)
    revisions_lateral = get_all_lateral_trajectory_versions(lateral_id)
    print('lateral revisions', revisions_lateral)
    all_trajectories = get_all_lateral_trajectories(revisions_lateral, stage_id=cur_stage_id, player_to_add=player_round_6)
    # done with laterals

    revisions_interp = get_all_interpetation_versions(lateral_id)
    print('interpretation revisions', revisions_interp)
    all_interpretations = get_all_interpretations(revisions_interp, stage_id=cur_stage_id, player_to_add=player_round_6)

    print(player_round_6)
    plotting_utility.plot_well(player_round_6, 84710640, True)
    #plotting_utility.plot_well_and_interpretation(player_round_6, 222, True)
    # todo since there is plenty of data before the start of competition note, the starting time
    # for round 1 seems to be around 2021-09-15 16:00
    # for round 2 seems to be around 2021-09-15 18:00
    #plotting_utility.plot_well_and_interpretation_by_time(player_round_6, '2021-09-15 17:08:03.556589', True, max_tvd=5000)
    #plotting_utility.plot_interpretation(player_round_6,('ef6f9322-61e6-447c-a7dc-642dc94e2ce1', 170305337) , show=False, max_tvd=100)
    
    
    
    
    