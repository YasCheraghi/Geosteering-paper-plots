
import math


DELTA = 0.000001


class LateralWell:
    def __init__(self, timestamp=None, well_points=None):
        if well_points is None:
            self.well_points = []
        else:
            self.well_points = well_points
        self.timestamp = timestamp


class WellPoint:
    def __init__(self, lateral_point, prev=None):
        self.md = lateral_point['md']['val']
        self.incl = lateral_point['incl']['val']
        self.azim = lateral_point['azim']['val']
        if prev is None:
            # todo fix the starting point's tvd
            self.vs = 0
            self.tvd = 0
        else:
            self._compute_vs_tvd_from_prev_solo(prev=prev)

    def _compute_vs_tvd_from_prev_naive(self, prev):
        # stupid version angle from current point
        d_md = self.md - prev.md
        d_vs = math.sin(self.incl) * d_md
        d_tvd = math.cos(self.incl) * d_md
        self.vs = prev.vs + d_vs
        self.tvd = prev.tvd + d_tvd

    def _calc_shape_factor(self, dog_leg):
        if dog_leg is None:
            return

        if (
                math.fabs(dog_leg) > DELTA and
                math.fabs(dog_leg - math.pi) > DELTA
        ):
            return 2.0 * math.tan(0.5 * dog_leg) / dog_leg

        return 1.0


    def compute_dog_leg(self, prev_point):
        curr_point = self
        prev_incl_sin, curr_incl_sin = math.sin(prev_point.incl), math.sin(curr_point.incl)
        prev_incl_cos, curr_incl_cos = math.cos(prev_point.incl), math.cos(curr_point.incl)
        curr_azim = self.azim
        dog_leg = math.acos(
            math.cos(prev_point.incl - curr_point.incl)
            - curr_incl_sin * prev_incl_sin
            * (1.0 - math.cos(curr_azim - prev_point.azim))
        )
        course_length = self.md - prev_point.md
        shape = 0.5 * self.calc_shape_factor(dog_leg) * course_length
        tvd = prev_point.tvd + shape * (curr_incl_cos + prev_incl_cos)
        vs = prev_point.vs + shape * (curr_incl_sin + prev_incl_sin)
        self.tvd = tvd
        self.vs = vs

    def _compute_vs_tvd_from_prev_solo(self, prev):
        # todo finish and test
        # stupid version angle from current point
        # tvd = prev_point.tvd + shape * (curr_incl_cos + prev_incl_cos)

        d_md = self.md - prev.md
        d_vs = math.sin(self.incl) * d_md
        d_tvd = math.cos(self.incl) * d_md
        self.vs = prev.vs + d_vs
        self.tvd = prev.tvd + d_tvd

    def __str__(self):
        return '{:6.1f} m VS: {:6.1f} TVD: {:6.1f} \n'.format(self.md, self.vs, self.tvd)

    def __repr__(self):
        return self.__str__()


def convert_well_points(points_lateral):
    # {'azim': {'val': 0}, 'incl': {'val': 0}, 'md': {'val': 0}}
    prev_point = None
    resulting_points = []
    for point in points_lateral:
        converted_point = WellPoint(point, prev_point)
        resulting_points.append(converted_point)
        prev_point = converted_point
    return resulting_points
