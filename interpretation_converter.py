EPS = 1e-7


class Interpretation:
    def __init__(self, md_points, tvd_shifts, horizon_depths, variable_thicknesses=False, timestamp=None):
        self.md_points = md_points
        self.tvd_shifts = tvd_shifts 
        self.horizon_depths = horizon_depths 
        self.variable_thicknesses = variable_thicknesses
        self.timestamp = timestamp


def get_tvd_shifts(horizon_shifts):
    old_start = None
    old_end = None
    for horizon_id in horizon_shifts:
        horizon = horizon_shifts[horizon_id]
        if old_start is None or old_end is None:
            old_start = horizon['start']['val']
            old_end = horizon['end']['val']
        else:
            start = horizon['start']['val']
            end = horizon['end']['val']
            if abs(start - old_start) > EPS or \
                    abs(end - old_end) > EPS:
                return old_start, old_end, False
    return old_start, old_end, True


def convert_interpretation(interpretation_data):
    # horizons
    # {'37e4e0fc-b65d-4bc4-a4f1-7eb4297f4728': {'tvd': {'val': 1369.8411137989049}, 'uuid': '37e4e0fc-b65d-4bc4-a4f1-7eb4297f4728'}
    # segments
    # {'boundary_type': 0,
    # 'md': {'val': 510.00986681776635},
    # 'start': {'val': 15.532732663662046}
    # 'end': {'val': 15.552119408874205},
    # 'horizon_shifts': {'37e4e0fc-b65d-4bc4-a4f1-7eb4297f4728': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': '37e4e0fc-b65d-4bc4-a4f1-7eb4297f4728'}, '42e64ae6-33f8-4746-a229-b4220539d8da': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': '42e64ae6-33f8-4746-a229-b4220539d8da'}, '5fb9eaa1-92cf-4021-b1f0-315ab6c35a83': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': '5fb9eaa1-92cf-4021-b1f0-315ab6c35a83'}, '623c60f1-344b-42ef-a50e-d8e1bd50d6ba': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': '623c60f1-344b-42ef-a50e-d8e1bd50d6ba'}, '69460429-ceb2-48b5-aa8b-5e8ac5f10c34': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': '69460429-ceb2-48b5-aa8b-5e8ac5f10c34'}, '8427d43e-790a-4e0e-9eb3-d649b0497d78': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': '8427d43e-790a-4e0e-9eb3-d649b0497d78'}, '9b957167-5175-4bcd-9c82-b7cf8e4bc6ae': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': '9b957167-5175-4bcd-9c82-b7cf8e4bc6ae'}, 'd793d350-9925-4338-9648-3b65f6cc7314': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': 'd793d350-9925-4338-9648-3b65f6cc7314'}, 'd9a8ddb3-83e3-46d6-b0ff-1ce2ff05e2e7': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': 'd9a8ddb3-83e3-46d6-b0ff-1ce2ff05e2e7'}, 'dc9f2168-aa15-47cb-aedf-2844026347dc': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': 'dc9f2168-aa15-47cb-aedf-2844026347dc'}, 'f91ffa21-7007-4627-9731-d9cfc3dd4977': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': 'f91ffa21-7007-4627-9731-d9cfc3dd4977'}, 'fe877253-eb46-4f37-869e-ffbe06176144': {'end': {'val': 16.666667544375287}, 'start': {'val': 21.69943924548079}, 'uuid': 'fe877253-eb46-4f37-869e-ffbe06176144'}}
    horizons = interpretation_data['horizons']
    segments = interpretation_data['segments']

    # horizons
    horizon_depths = []
    for horizon_id in horizons:
        horizon = horizons[horizon_id]
        horizon_depths.append(horizon['tvd']['val'])

    # segments
    segment_mds = []
    segment_tvd_shifts = []
    md_prev = 0
    prev_end = -100500
    variable_thickness = False
    for segment in segments:
        md = segment['md']['val']
        start, end, equal = get_tvd_shifts(segment['horizon_shifts'])
        if start != prev_end:
            # print('boundary type', segment['boundary_type'])
            segment_mds.append(md_prev + EPS)
            segment_tvd_shifts.append(start)
        segment_mds.append(md)
        segment_tvd_shifts.append(end)
        if not equal:
            print('Warning variable thickness of layers')
            variable_thickness = True
        md_prev = md
        prev_end = end

    return Interpretation(md_points=segment_mds,
                          tvd_shifts=segment_tvd_shifts,
                          horizon_depths=horizon_depths,
                          variable_thicknesses=variable_thickness)

