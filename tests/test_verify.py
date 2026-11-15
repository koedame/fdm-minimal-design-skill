import sys

from conftest import ROOT

sys.path.insert(0, str(ROOT / "skills" / "fdm-minimal-design" / "scripts"))
import fdm_samples as fs   # noqa: E402
import verify              # noqa: E402

BASE = fs.box(-20, 20, -20, 20, 0, 10)


def slider_parts():
    """A block on a base plate, with a wall at x 20..24 that stops it after 10 mm of travel to +X."""
    base = BASE.union(fs.box(20, 24, -20, 20, 10, 20))
    block = fs.box(-10, 10, -10, 10, 10, 20)
    return {"base": fs.Part(base, base, fs.OFF), "block": fs.Part(block, block, fs.OFF)}


def results(parts, motion):
    return {pos: (want, ok) for pos, _, want, ok in verify.motion_check(parts, motion)}


def test_when_a_slide_reaches_the_wall_the_stop_is_proven_and_before_it_the_part_is_free():
    motion = {"part": "block", "against": "base", "slide": [1, 0, 0], "free": [0, 9.9], "stop": [10.5]}
    assert results(slider_parts(), motion) == {0: ("free", True), 9.9: ("free", True), 10.5: ("stop", True)}


def test_when_a_stop_is_expected_where_the_part_is_still_free_the_position_fails():
    motion = {"part": "block", "against": "base", "slide": [2, 0, 0], "stop": [5]}   # the direction is normalised
    assert results(slider_parts(), motion) == {5: ("stop", False)}


def test_when_a_snap_overlaps_within_its_limit_it_passes_and_beyond_it_fails():
    parts = slider_parts()
    # at 10.1 the block enters the wall by 0.1 x 20 x 10 = 20 mm3
    assert results(parts, {"part": "block", "against": "base", "slide": [1, 0, 0],
                           "snap": {"at": [10.1], "max_mm3": 25}}) == {10.1: ("snap", True)}
    assert results(parts, {"part": "block", "against": "base", "slide": [1, 0, 0],
                           "snap": {"at": [10.1], "max_mm3": 15}}) == {10.1: ("snap", False)}


def test_when_a_hinge_turns_a_flap_into_the_base_the_overlap_is_found():
    flap = fs.box(-20, 20, 10, 12, 10, 40)            # stands on the back edge of the base, axis along X at y 12, z 10
    parts = {"base": fs.Part(BASE, BASE, fs.OFF), "flap": fs.Part(flap, flap, fs.OFF)}
    motion = {"part": "flap", "against": "base", "hinge": [[0, 12, 10], [1, 12, 10]], "free": [-90], "stop": [90]}
    assert results(parts, motion) == {-90: ("free", True), 90: ("stop", True)}


class _Vol:
    """A shape that knows only its volume and what intersect and cut return."""
    def __init__(self, vol, inter=None, rest=None):
        self.vol, self.inter, self.rest = vol, inter, rest

    def Volume(self):
        return self.vol

    def intersect(self, other):
        return self.inter

    def cut(self, other):
        return self.rest


def test_when_intersect_returns_nothing_for_shapes_that_overlap_the_cut_still_finds_the_overlap():
    # what OCCT did on a lid turned 1 deg into its base: intersect empty, but the cut took 519 mm3 off the base
    base = _Vol(1000.0, rest=_Vol(481.0))
    lid = _Vol(800.0, inter=_Vol(0.0))
    assert verify.overlap(lid, base) == 519.0


def test_when_intersect_finds_an_overlap_it_is_taken_as_it_is():
    base = _Vol(1000.0, rest=_Vol(0.0))           # a cut that failed would claim everything
    lid = _Vol(800.0, inter=_Vol(20.0))
    assert verify.overlap(lid, base) == 20.0


def test_when_copies_of_a_part_touch_and_are_unioned_verify_reports_them_fused(capsys):
    one = fs.box(0, 10, 0, 10, 0, 5)
    fused = one.union(one.translate((0, 0, 5)))
    fs.SAMPLES["_test_fused"] = lambda: {"disc": fs.Part(fused, one, fs.OFF, qty=2)}
    fs.SAMPLES["_test_copies"] = lambda: {"disc": fs.Part(fs.copies([one, one.translate((0, 0, 5))]), one, fs.OFF, qty=2)}
    try:
        assert verify.check("_test_fused", 256) is False
        assert "copies fused in a union" in capsys.readouterr().out
        assert verify.check("_test_copies", 256) is True
    finally:
        del fs.SAMPLES["_test_fused"], fs.SAMPLES["_test_copies"]


def test_when_a_feature_of_a_part_does_not_touch_it_verify_reports_a_loose_piece(capsys):
    block = fs.box(0, 10, 0, 10, 0, 5)
    loose = block.union(fs.box(10.5, 14, 0, 10, 0, 5))    # a ledge 0.5 short of the block
    fs.SAMPLES["_test_loose"] = lambda: {"rail": fs.Part(loose, loose, fs.OFF)}
    fs.SAMPLES["_test_joined"] = lambda: {"rail": fs.Part(block.union(fs.box(9.5, 14, 0, 10, 0, 5)), block, fs.OFF)}
    try:
        assert verify.check("_test_loose", 256) is False
        assert "2 separate solids" in capsys.readouterr().out
        assert verify.check("_test_joined", 256) is True
    finally:
        del fs.SAMPLES["_test_loose"], fs.SAMPLES["_test_joined"]


def test_when_a_part_is_bought_it_is_checked_for_interference_but_not_as_a_print(capsys):
    pin = fs.cyl(1.5, 5, 10)                           # half inside the base
    fs.SAMPLES["_test_ref"] = lambda: {"base": fs.Part(BASE, BASE, fs.OFF), "pin": fs.Part(pin, None, fs.DARK, ref=True)}
    try:
        assert verify.check("_test_ref", 256) is False
        out = capsys.readouterr().out
        assert "pin                    valid=True bought part, not printed" in out
        assert "base x pin:" in out
    finally:
        del fs.SAMPLES["_test_ref"]


def test_when_a_shape_is_put_on_a_vertical_slope_its_local_z_points_to_the_front_and_y_up():
    plate = fs.box(-5, 5, 0, 20, 0, 1)                 # local: 20 up the face, 1 out of it
    bb = fs.on_slope(plate, 90, (0, -30, 10)).val().BoundingBox()
    assert (round(bb.ymin, 6), round(bb.ymax, 6), round(bb.zmin, 6), round(bb.zmax, 6)) == (-31, -30, 10, 30)
