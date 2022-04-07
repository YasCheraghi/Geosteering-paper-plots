import numpy as np
import pandas as pd
import gzip
import json
import player
import well_point_converter as point_converter
import interpretation_converter
import plotting_utility
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score



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
    player_round_6 = get_virtual_project_id(5, stage_id=cur_stage_id)
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
    
    
# plotting the well trajectories for all players, conventional    
    
    player_num_list=[]
    
    for i in range(350):
        
        if i==48: continue
        #if i==19: continue
        #if i==18: continue
        #if i==20: continue
        #if i==22: continue
        #if i==233: continue
        #if i==275: continue
    
        player_num_list.append(i+1)
        
    cur_stage_id = id_stage_1
    
    vss_all_r2=[]
    tvds_all_r2=[]
    
    for player_number in player_num_list:
        
        print(player_number)
        
        player_round_6 = get_virtual_project_id(player_number, stage_id=cur_stage_id)
        #print('virtual project id', player_round_6.virtual_proj_id)
        lateral_id = get_lateral(player_round_6.virtual_proj_id)
        #print('lateral object', lateral_id)
        revisions_lateral = get_all_lateral_trajectory_versions(lateral_id)
        #print('lateral revisions', revisions_lateral)
        all_trajectories = get_all_lateral_trajectories(revisions_lateral, stage_id=cur_stage_id, player_to_add=player_round_6)
        # done with laterals

        revisions_interp = get_all_interpetation_versions(lateral_id)
        #print('interpretation revisions', revisions_interp)
        all_interpretations = get_all_interpretations(revisions_interp, stage_id=cur_stage_id, player_to_add=player_round_6)
        
        trajectories=player_round_6.trajectories
        traj_index_list=list(trajectories.keys())
        traj_index_endtime=traj_index_list[len(traj_index_list)-1]
        
        #plotting_utility.plot_well(player_round_6, traj_index_endtime, True)
        
        players_well = player_round_6.trajectories[traj_index_endtime]
        
        points=players_well.well_points
        
        vss = []
        tvds = []
        max_tvd=4000
        for point in points: 
            vss.append(point.vs)
            tvds.append(point.tvd)
        plt.plot(vss, tvds) 
        plt.ylim(max_tvd, 3500)
        
        vss_all_r2.append(vss)
        tvds_all_r2.append(tvds)
        
    plt.xlabel('vss')
    plt.ylabel('xtvds')
    plt.title("Well Trajectories for all players, conventional round")
    plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/well_trajectories_all_r1.png', dpi=500)
    
    
        


# plotting the well trajectories for all players    
    
    player_num_list=[]
    
    for i in range(350):
        
        if i==48: continue
        if i==19: continue
        if i==18: continue
        if i==20: continue
        if i==22: continue
        if i==233: continue
        if i==275: continue
    
        player_num_list.append(i+1)
        
    cur_stage_id = id_stage_2
    
    vss_all_r2=[]
    tvds_all_r2=[]
    
    for player_number in player_num_list:
        
        print(player_number)
        
        player_round_6 = get_virtual_project_id(player_number, stage_id=cur_stage_id)
        #print('virtual project id', player_round_6.virtual_proj_id)
        lateral_id = get_lateral(player_round_6.virtual_proj_id)
        #print('lateral object', lateral_id)
        revisions_lateral = get_all_lateral_trajectory_versions(lateral_id)
        #print('lateral revisions', revisions_lateral)
        all_trajectories = get_all_lateral_trajectories(revisions_lateral, stage_id=cur_stage_id, player_to_add=player_round_6)
        # done with laterals

        revisions_interp = get_all_interpetation_versions(lateral_id)
        #print('interpretation revisions', revisions_interp)
        all_interpretations = get_all_interpretations(revisions_interp, stage_id=cur_stage_id, player_to_add=player_round_6)
        
        trajectories=player_round_6.trajectories
        traj_index_list=list(trajectories.keys())
        traj_index_endtime=traj_index_list[len(traj_index_list)-1]
        
        #plotting_utility.plot_well(player_round_6, traj_index_endtime, True)
        
        players_well = player_round_6.trajectories[traj_index_endtime]
        
        points=players_well.well_points
        
        vss = []
        tvds = []
        max_tvd=1420
        for point in points: 
            vss.append(point.vs)
            tvds.append(point.tvd)
        plt.plot(vss, tvds) 
        plt.ylim(max_tvd, 1300)
        
        vss_all_r2.append(vss)
        tvds_all_r2.append(tvds)
        
    plt.xlabel('vss')
    plt.ylabel('xtvds')
    plt.title("Well Trajectories for all players, unconventional round")
    plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/well_trajectories_all_r2.png', dpi=300)
    
    
    
    
    
# finding Interesting players


player_num_list=[]

for i in range(350):
    
    if i==48: continue
    #if i==19: continue
    #if i==20: continue
    #if i==22: continue
    #if i==233: continue

    player_num_list.append(i+1)    


cur_stage_id = id_stage_1

vss_all=[]
tvds_all=[]

for player_number in player_num_list:
    
    player_round_6 = get_virtual_project_id(player_number, stage_id=cur_stage_id)
    lateral_id = get_lateral(player_round_6.virtual_proj_id)
    revisions_lateral = get_all_lateral_trajectory_versions(lateral_id)
    all_trajectories = get_all_lateral_trajectories(revisions_lateral, stage_id=cur_stage_id, player_to_add=player_round_6)
    revisions_interp = get_all_interpetation_versions(lateral_id)
    all_interpretations = get_all_interpretations(revisions_interp, stage_id=cur_stage_id, player_to_add=player_round_6)
    trajectories=player_round_6.trajectories
    traj_index_list=list(trajectories.keys())
    traj_index_endtime=traj_index_list[len(traj_index_list)-1]   
    players_well = player_round_6.trajectories[traj_index_endtime]
    
    points=players_well.well_points
    
    vss = []
    tvds = []
    max_tvd=4000
    for point in points: 
        vss.append(point.vs)
        tvds.append(point.tvd)

    vss_all.append(vss)
    tvds_all.append(tvds)
    

variance=[] 

for i in tvds_all:
    
    var=np.var(i)
    
    variance.append(var)
    
    
plt.scatter(variance,conv_score, marker='o', c='red', linewidths=0.5, edgecolors='black')
plt.xlabel('Variance in well trajectory')
plt.ylabel('Total Score')

plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/var_vs_score.png', dpi=500)            

# Plotting well trajectories of top 10 players=

top_players=[74, 141, 61, 6, 183, 149, 148, 196, 284, 85]
top_scores=[80.7,82.8, 83.9, 79.5, 79.7, 80.8, 87.5, 82.1, 82.5, 80.3]
cur_stage_id = id_stage_1



for p in range(len(top_players)):
    

        
    player_round_6 = get_virtual_project_id(top_players[p], stage_id=cur_stage_id)
        #print('virtual project id', player_round_6.virtual_proj_id)
    lateral_id = get_lateral(player_round_6.virtual_proj_id)
        #print('lateral object', lateral_id)
    revisions_lateral = get_all_lateral_trajectory_versions(lateral_id)
        #print('lateral revisions', revisions_lateral)
    all_trajectories = get_all_lateral_trajectories(revisions_lateral, stage_id=cur_stage_id, player_to_add=player_round_6)
        # done with laterals

    revisions_interp = get_all_interpetation_versions(lateral_id)
        #print('interpretation revisions', revisions_interp)
    all_interpretations = get_all_interpretations(revisions_interp, stage_id=cur_stage_id, player_to_add=player_round_6)
        
    trajectories=player_round_6.trajectories
    traj_index_list=list(trajectories.keys())
    traj_index_endtime=traj_index_list[len(traj_index_list)-1]
        
        #plotting_utility.plot_well(player_round_6, traj_index_endtime, True)
        
    players_well = player_round_6.trajectories[traj_index_endtime]
        
    points=players_well.well_points
        
    vss = []
    tvds = []
    max_tvd=3750
    for point in points: 
        vss.append(point.vs)
        tvds.append(point.tvd)
    
    plt.style.use('fivethirtyeight')
    plt.plot(vss, tvds) 
    plt.ylim(max_tvd, 3550)
    plt.xlabel('vss')
    plt.ylabel('tvds')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10 )
    plt.title("Well Trajectories for top  players, conventional round")
    plt.legend(['player number:74, score=80.7', 'player number:141, score=82.8','player number:61, score=83.9','player number:6, score=79.5','player number:183, score=79.7', 'player number:149, score=80.8', 'player number:148, score=87.5','player number:196, score=82.1','player number:284, score=82.5', 'player number:85, score=80.3',], fontsize=5, bbox_to_anchor=(0.9, 0.95))
    
    
plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/well_trajectories_top_r1.png',bbox_inches='tight', dpi=250)
    
    
# Plotting well trajectories of worst 10 players=

worst_players=[63, 282, 118, 217, 279, 198, 229, 214, 115, 116]
worst_scores=[27.3, 26.6, 26.1, 22.5, 22.3, 21.3, 27.6, 27.6, 27.6, 27.6]

for p in range(len(worst_players)):
    

        
    player_round_6 = get_virtual_project_id(worst_players[p], stage_id=cur_stage_id)
        #print('virtual project id', player_round_6.virtual_proj_id)
    lateral_id = get_lateral(player_round_6.virtual_proj_id)
        #print('lateral object', lateral_id)
    revisions_lateral = get_all_lateral_trajectory_versions(lateral_id)
        #print('lateral revisions', revisions_lateral)
    all_trajectories = get_all_lateral_trajectories(revisions_lateral, stage_id=cur_stage_id, player_to_add=player_round_6)
        # done with laterals

    revisions_interp = get_all_interpetation_versions(lateral_id)
        #print('interpretation revisions', revisions_interp)
    all_interpretations = get_all_interpretations(revisions_interp, stage_id=cur_stage_id, player_to_add=player_round_6)
        
    trajectories=player_round_6.trajectories
    traj_index_list=list(trajectories.keys())
    traj_index_endtime=traj_index_list[len(traj_index_list)-1]
        
        #plotting_utility.plot_well(player_round_6, traj_index_endtime, True)
        
    players_well = player_round_6.trajectories[traj_index_endtime]
        
    points=players_well.well_points
        
    vss = []
    tvds = []
    max_tvd=3750
    for point in points: 
        vss.append(point.vs)
        tvds.append(point.tvd)
    plt.plot(vss, tvds) 
    plt.ylim(max_tvd, 3500)
    plt.xlabel('vss')
    plt.ylabel('tvds')
    plt.title("Well Trajectories for low ranked players, conventional round")
    plt.legend(['player number:63, score=27.3', 'player number:282, score=26.6','player number:118, score=26.1','player number:217, score=22.5','player number:279, score=22.3', 'player number:198, score=21.3', 'player number:229, score=27.6','player number:214, score=27.6','player number:215, score=27.6', 'player number:216, score=27.6',], fontsize=5, bbox_to_anchor=(0.7, 0.5))
    
    
plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/well_trajectories_low_ranked_r1.png',bbox_inches='tight', dpi=250)



  
    
    
    
    
    
    
#- Correlation between variance in well trajectory and total score 
variance=[] 

for i in tvds_all:
    
    var=np.var(i)
    
    variance.append(var)
    
    
plt.scatter(variance,conv_score, marker='o', c='red', linewidths=0.5, edgecolors='black')
plt.xlabel('Variance in well trajectory')
plt.ylabel('Total Score')

plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/var_vs_score.png', dpi=500) 









# getting the interpretation of all players at the endtime

player_num_list=[]

for i in range(350):
    
    if i==48: continue
    #if i==19: continue
    #if i==20: continue
    #if i==22: continue
    #if i==233: continue

    player_num_list.append(i+1)    


cur_stage_id = id_stage_1

mds_all=[]
tvd_shift_all=[]
max_tvd=200
for player_number in player_num_list:
    print(player_number)
    player_round_6 = get_virtual_project_id(player_number, stage_id=cur_stage_id)
    lateral_id = get_lateral(player_round_6.virtual_proj_id)
    revisions_lateral = get_all_lateral_trajectory_versions(lateral_id)
    all_trajectories = get_all_lateral_trajectories(revisions_lateral, stage_id=cur_stage_id, player_to_add=player_round_6)
    revisions_interp = get_all_interpetation_versions(lateral_id)
    all_interpretations = get_all_interpretations(revisions_interp, stage_id=cur_stage_id, player_to_add=player_round_6)
    
    indexes=player_round_6.interpretation_dict.keys()
    for ind in indexes:
        
        if str(player_round_6.interpretation_dict[ind].timestamp)=='nan':
            
            continue
        
        if '2021-09-15' in player_round_6.interpretation_dict[ind].timestamp:
            
            endtime_index=ind
    
    players_interpretation = player_round_6.interpretation_dict[endtime_index]
    
    b=players_interpretation 
    mds = b.md_points
    tvds = b.tvd_shifts
    plt.plot(mds, tvds)
    plt.xlim(0,7000)
    plt.ylim(max_tvd, -max_tvd)
    plt.xlabel('MD')
    plt.ylabel('TVD shifts')
    mds_all.append(mds)
    tvd_shift_all.append(tvds)

plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/interpretatio_endtime_r1.png', dpi=500) 
    









# well trajectory for top conventional r1

cur_stage_id = id_stage_1
        
    
player_round_6 = get_virtual_project_id(78, stage_id=cur_stage_id)
    #print('virtual project id', player_round_6.virtual_proj_id)
lateral_id = get_lateral(player_round_6.virtual_proj_id)
    #print('lateral object', lateral_id)
revisions_lateral = get_all_lateral_trajectory_versions(lateral_id)
    #print('lateral revisions', revisions_lateral)
all_trajectories = get_all_lateral_trajectories(revisions_lateral, stage_id=cur_stage_id, player_to_add=player_round_6)
    # done with laterals

revisions_interp = get_all_interpetation_versions(lateral_id)
    #print('interpretation revisions', revisions_interp)
all_interpretations = get_all_interpretations(revisions_interp, stage_id=cur_stage_id, player_to_add=player_round_6)
    
trajectories=player_round_6.trajectories
traj_index_list=list(trajectories.keys())
traj_index_endtime=traj_index_list[len(traj_index_list)-1]
    
    #plotting_utility.plot_well(player_round_6, traj_index_endtime, True)
    
players_well = player_round_6.trajectories[traj_index_endtime]
    
points=players_well.well_points
    
vss = []
tvds = []
for point in points: 
    vss.append(point.vs)
    tvds.append(point.tvd)
    
vss_top_r1=vss
tvds_top_r1=tvds
    

# error traj r1    

interpret_error=[]
player_index=[]
strategy=''
error_list_all=[]

for i in range(len(vss_all_r1)):  # iteration over all players
    
    error_list=[]
    
    vss_all_r1[i]=vss_all_r1[i]
    tvds_all_r1[i]=tvds_all_r1[i]
    
    if len(vss_all_r1[i])==0:
    
        max_vss=0
    else:
        max_vss=vss_all_r1[i][-1]

    for j in range(len(vss_top_r1)):
        
        vss_ref=vss_top_r1[j]
        tvds_ref=tvds_top_r1[j]
         
       
        flag='F'
        
        for k in range(len(vss_all_r1[i])):
                  
            if vss_all_r1[i][k]==vss_ref:
                   
                error_val=abs(tvds_ref-tvds_all_r1[i][k])
                error_list.append(error_val)
                flag='T'
        
       
        
        if flag=='F':
            

                if max_vss>= vss_ref:
                
                    strategy='interpolation'
                
                    # finding min & max neighbors
                
                    for k in range(len(vss_all_r1[i])):
                    
                        if vss_all_r1[i][k]<vss_ref:
                        
                            min_neighbor=vss_all_r1[i][k]
                            tvd_min_neighbor=tvds_all_r1[i][k]
                        
                
                    for k in range(len(vss_all_r1[i])):
                    
                        if vss_all_r1[i][k]>vss_ref:
                        
                            max_neighbor=vss_all_r1[i][k]
                            tvd_max_neighbor=tvds_all_r1[i][k]
                            break
                        
                
                
                    m=(tvd_max_neighbor-tvd_min_neighbor)/(max_neighbor-min_neighbor)
                    b=tvd_max_neighbor-(m*max_neighbor)
                
                    tvd_pred=m*vss_ref + b
                
                
                    tvd_diff=abs(tvd_pred-tvds_ref)
                    error_list.append(tvd_diff)
                    print('no')
            
                if max_vss< vss_ref:
            
                    strategy='previous error'
                    if len(error_list)>=1:
                        prev_error=error_list[-1]
                        
                    else:
                        prev_error=100
                    error_list.append(prev_error)
                    print('yes')
                
    print(len(error_list))           
    error_list_all.append(error_list)            
    sum_error=sum(error_list)
    interpret_error.append(sum_error)
    player_index.append(i)
            

                
# ploting

for i in range(len(player_num_list)):
    
    for j in range(len(player_num_excel)):
        
        numm=int(player_num_excel[j][6:])
        
        if numm==player_num_list[i]:
            
            plt.scatter(interpret_error[i],inzoneunconv[j], marker='o', c='red', edgecolors='black')

    

plt.xlabel('trajectory error, R1')
plt.ylabel(' in zone %')
plt.xlim(0,20000)

plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/traj_error_inzone_r1.png',bbox_inches='tight', dpi=500)


   
# interpretation of top unconventional as the true model

cur_stage_id = id_stage_1


max_tvd=150
player_round_6 = get_virtual_project_id(78, stage_id=cur_stage_id)
lateral_id = get_lateral(player_round_6.virtual_proj_id)
revisions_lateral = get_all_lateral_trajectory_versions(lateral_id)
all_trajectories = get_all_lateral_trajectories(revisions_lateral, stage_id=cur_stage_id, player_to_add=player_round_6)
revisions_interp = get_all_interpetation_versions(lateral_id)
all_interpretations = get_all_interpretations(revisions_interp, stage_id=cur_stage_id, player_to_add=player_round_6)
    
indexes=player_round_6.interpretation_dict.keys()

for ind in indexes:
        
    if str(player_round_6.interpretation_dict[ind].timestamp)=='nan':
            
            continue
        
    if '2021-09-15' in player_round_6.interpretation_dict[ind].timestamp:
            
            endtime_index=ind
    
players_interpretation = player_round_6.interpretation_dict[endtime_index]
    
b=players_interpretation 
mds = b.md_points
tvds = b.tvd_shifts
plt.plot(mds, tvds)
plt.xlim(0,3000)
plt.ylim(-max_tvd, max_tvd)
plt.xlabel('MD')
plt.ylabel('TVD shifts')
mds_top_r1= mds
tvd_shift_top_r1=tvds

plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/interpretatio_endtime_top_r2.png', dpi=500) 
 


  # Calculating the interpretation error with regards to the best player- round 1



  interpret_error=[]
  player_index=[]
  strategy=''
  error_list_all=[]

  for i in range(len(mds_all_r1)):  # iteration over all players
      

      

      error_list=[]
      
      max_md=mds_all_r1[i][0]

          
          
      for k in range(len(mds_all_r1[i])):
                 
          if mds_all_r1[i][k]>=max_md:
                  
              max_md=mds_all_r1[i][k]
      
      for j in range(len(mds_top_r1)):
          
          exact_val_index=0
          md_ref=mds_top_r1[j]
          tvd_shift_ref=tvd_shift_top_r1[j]
          
         
          
          for k in range(len(mds_all_r1[i])):
                    
              if mds_all_r1[i][k]==md_ref:
                     
                  error_val=abs(tvd_shift_ref-tvd_shift_all_r1[i][k])
                  error_list.append(error_val)
                  exact_val_index=1
          
         
                  
          if j==0 and exact_val_index==0:
                      
              error_val=abs(tvd_shift_top_r1[0]-tvd_shift_all_r1[i][0])
              error_list.append(error_val)
              
              
          if j==1 and mds_all_r1[i][1]==2900 and exact_val_index==0:
              
              error_val=abs(tvd_shift_top_r1[1]-tvd_shift_all_r1[i][1])
              error_list.append(error_val)
          
          if j>=2 and exact_val_index==0:
              
              
              if max_md>= md_ref:
              
                  strategy='interpolation'
              
                  # finding min & max neighbors
              
                  for k in range(len(mds_all_r1[i])):
                  
                      if mds_all_r1[i][k]<md_ref:
                      
                          min_neighbor=mds_all_r1[i][k]
                          tvd_min_neighbor=tvd_shift_all_r1[i][k]
                      
              
                  for k in range(len(mds_all_r1[i])):
                  
                      if mds_all_r1[i][k]>md_ref:
                      
                          max_neighbor=mds_all_r1[i][k]
                          tvd_max_neighbor=tvd_shift_all_r1[i][k]
                          break
                      
              
              
                  m=(tvd_max_neighbor-tvd_min_neighbor)/(max_neighbor-min_neighbor)
                  b=tvd_max_neighbor-(m*max_neighbor)
              
                  tvd_pred=m*md_ref + b
              
              
                  tvd_diff=abs(tvd_pred-tvd_shift_ref)
                  error_list.append(tvd_diff)
                  print('no')
              
              if max_md< md_ref:
              
                  strategy='previous error'
                  prev_error=error_list[-1]
                  error_list.append(prev_error)
                  print('yes')
                  
      print(len(error_list))           
      error_list_all.append(error_list)            
      sum_error=sum(error_list)
      interpret_error.append(sum_error)
      player_index.append(i)
              


  data=pd.read_excel('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Working Folder/results_ALL_meg.xlsx', sheet_name='all_scores(RU)', header=1)

  conv_score=data.convscore
  unconv_score=data.unconvscore
  player_num_excel=data.Player
  inzoneconv=data.InZoneconv
  inzoneunconv=data.inZoneunconv           
             
  player_list=data.Player
  player_number=[]
  sorted_score=[0]*349
  sorted_inzone=[0]*349 
  sorted_unconv_score=[0]*349
  sorted_unconv_inzone=[0]*349       
              
  for i in range(len(player_list)):
      
      player_num=int(player_list[i][6:])
      player_number.append(player_num)
      

#storing scores      
              
  for i in range(len(player_num_list)):
      
      
      for j in range(len(player_number)):
          
          
          if player_num_list[i]==player_number[j]:
              
              sorted_score[i]=conv_score[j]
              sorted_inzone[i]=inzoneconv[j]
              sorted_unconv_score[i]=unconv_score[j]
              sorted_unconv_inzone[i]=inzoneunconv[j] 
              

# plotting

  for i in range(len(player_num_list)):
      
      for j in range(len(player_num_excel)):
          
          numm=int(player_num_excel[j][6:])
          
          if numm==player_num_list[i]:
              
              plt.scatter(interpret_error[i],unconv_score[j], marker='o', c='red', edgecolors='black')

     
  plt.xlabel('interpret error, R1')
  plt.ylabel(' Total Scores')
  plt.xlim(0,2000)

  plt.savefig('//fil031.uis.no/emp05/2925376/Desktop/Geosteering Paper/Plots-paper/interpret_error_r1.png',bbox_inches='tight', dpi=500)
  
  
