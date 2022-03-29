import matplotlib.pyplot as plt
import numpy as np


def plot_well(player, index, show=False, max_tvd=4000):
    players_well = player.trajectories[index]
    # editing YASAMAN Test
    points=players_well.well_points
    
    vss = []
    tvds = []
    for point in points: 
        vss.append(point.vs)
        tvds.append(point.tvd)
    plt.plot(vss, tvds) 
    plt.ylim(max_tvd, 0)
    # plt.plot()
    #if show:
        #plt.show()
    
    
def plot_interpretation(player, index, show=False, max_tvd=100):
    players_interpretation = player.interpretation_dict[index]
    # Editing YASAMAN
    b=players_interpretation 
    mds = b.md_points
    tvds = b.tvd_shifts
    plt.plot(mds, tvds)
    plt.xlim(0,5000)
    plt.ylim(max_tvd, -max_tvd) 
    # plt.plot()
    #if show:
        #plt.show()   


def convert_mds_to_vss(mds, well_mds, well_vss):
    mds_np = np.array(mds)
    well_mds_np = np.array(well_mds)
    well_vss_np = np.array(well_vss)
    interp_vss = np.interp(x=mds_np, xp=well_mds_np, fp=well_vss_np)
    return interp_vss


def plot_well_and_interpretation_by_time(player, time_str, show=False, max_tvd=2000):
    print('looking for {}'.format(time_str))
    interp_index = None
    for i, interp_id in enumerate(player.interpretation_id_list):
        # interp = player.interpretation_id_list[i[1]]
        interp = player.interpretation_dict[interp_id]
        print(interp.timestamp)
        if isinstance(interp.timestamp, str) and (interp.timestamp >= time_str):
            interp_index = i
            traj_time_stamp = interp.timestamp
            print(traj_time_stamp) 
            break
    plot_well_and_interpretation(player, interp_index, show=show, max_tvd=max_tvd)


def plot_well_and_interpretation(player, interp_index, show=False, max_tvd=5000, use_md=False):
    my_index = player.interpretation_id_list[interp_index]
    players_interpretation = player.interpretation_dict[my_index]
    traj_ids = player.trajectories.keys()
    time_stamp = players_interpretation.timestamp
    for i in traj_ids:
        traj = player.trajectories[i]
        if isinstance(traj.timestamp, str) and (traj.timestamp > time_stamp or traj.timestamp == time_stamp):
            traj_time_stamp = traj.timestamp
            print(traj_time_stamp)
            break
    players_well = traj
    mds = []
    vss = []
    tvds = []
    for point in players_well.well_points:
        mds.append(point.md)
        vss.append(point.vs)
        tvds.append(point.tvd)

    # plotting the well
    if use_md:
        plt.plot(mds, tvds)
    else:
        plt.plot(vss, tvds)

    interp_vss = convert_mds_to_vss(players_interpretation.md_points, mds, vss)
    interp_tvd_sshifts = np.array(players_interpretation.tvd_shifts)
    for depth in players_interpretation.horizon_depths:
        interp_tvds = depth + interp_tvd_sshifts
        if use_md:
            plt.plot(np.array(players_interpretation.md_points), interp_tvds)
        else:
            plt.plot(interp_vss, interp_tvds)

    plt.ylim(max_tvd, 0)
    # plt.plot()
    if show:
        plt.show()

