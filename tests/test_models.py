import json

import models


def edit_json(path, **changes):
    meta = json.loads(path.read_text())
    meta.update(changes)
    path.write_text(json.dumps(meta))


def problems_of(models_dir, name="001_pen_cup"):
    return models.check_model(models_dir / name)


def test_when_a_model_directory_is_complete_and_consistent_check_reports_no_problems(models_dir):
    assert problems_of(models_dir) == []


def test_when_check_passes_for_every_model_the_command_exits_with_0(models_dir, capsys):
    assert models.main(["--models-dir", str(models_dir), "check"]) == 0
    assert "1 of 1 models passed" in capsys.readouterr().out


def test_when_a_model_has_a_problem_the_command_exits_with_1_and_prints_it(models_dir, capsys):
    (models_dir / "001_pen_cup" / "rationale.md").unlink()
    assert models.main(["--models-dir", str(models_dir), "check"]) == 1
    assert "missing file: rationale.md" in capsys.readouterr().out


def test_when_the_directory_name_is_not_nnn_slug_check_rejects_it(models_dir):
    (models_dir / "001_pen_cup").rename(models_dir / "PenCup")
    assert problems_of(models_dir, "PenCup") == [
        "directory name 'PenCup' is not NNN_slug (three digits, lowercase snake_case)"]


def test_when_the_id_in_model_json_differs_from_the_directory_name_check_reports_it(models_dir):
    edit_json(models_dir / "001_pen_cup" / "model.json", id="002_pen_cup")
    assert any("does not match the directory name" in p for p in problems_of(models_dir))


def test_when_a_required_field_is_missing_check_names_the_field(models_dir):
    path = models_dir / "001_pen_cup" / "model.json"
    meta = json.loads(path.read_text())
    del meta["summary"]
    path.write_text(json.dumps(meta))
    assert "model.json: missing field 'summary'" in problems_of(models_dir)


def test_when_the_licence_is_not_cc_by_4_0_check_reports_it(models_dir):
    edit_json(models_dir / "001_pen_cup" / "model.json", license="MIT")
    assert any("'license' has an invalid value" in p for p in problems_of(models_dir))


def test_when_based_on_names_something_that_is_not_a_sample_check_reports_it(models_dir):
    edit_json(models_dir / "001_pen_cup" / "model.json", based_on=["99_toaster"])
    assert "model.json: based_on '99_toaster' is not one of the skill's samples" in problems_of(models_dir)


def test_when_a_part_in_model_json_is_not_built_by_design_py_check_names_the_part(models_dir):
    edit_json(models_dir / "001_pen_cup" / "model.json", parts=[
        {"name": "cup", "qty": 1, "orientation": "Bottom down", "material": "PLA"},
        {"name": "lid", "qty": 1, "orientation": "Top face down", "material": "PLA"}])
    assert "model.json: part 'lid' is in parts but not in design.py" in problems_of(models_dir)


def test_when_a_part_quantity_differs_from_design_py_check_reports_both_numbers(models_dir):
    edit_json(models_dir / "001_pen_cup" / "model.json", parts=[
        {"name": "cup", "qty": 2, "orientation": "Bottom down", "material": "PLA"}])
    assert "model.json: part 'cup' qty 2 but design.py makes 1" in problems_of(models_dir)


def test_when_size_mm_differs_from_the_assembled_bounding_box_check_reports_the_measured_size(models_dir):
    edit_json(models_dir / "001_pen_cup" / "model.json", size_mm=[72, 72, 100])
    assert any("measures 72.0 x 72.0 x 108.0" in p for p in problems_of(models_dir))


def test_when_rationale_md_lacks_the_review_section_check_reports_it(models_dir):
    path = models_dir / "001_pen_cup" / "rationale.md"
    path.write_text(path.read_text().replace("## Review", "## Notes"))
    assert any(p.startswith("rationale.md: needs the sections") for p in problems_of(models_dir))


def test_when_preview_png_is_not_a_png_check_reports_it(models_dir):
    (models_dir / "001_pen_cup" / "preview.png").write_bytes(b"not an image")
    assert "preview.png: not a PNG file" in problems_of(models_dir)


def test_when_design_py_registers_a_different_id_check_reports_it(models_dir):
    path = models_dir / "001_pen_cup" / "design.py"
    path.write_text(path.read_text().replace('SAMPLES["001_pen_cup"]', 'SAMPLES["001_pen_mug"]'))
    models.fdm_samples.SAMPLES.pop("001_pen_cup", None)
    assert "design.py: does not register SAMPLES['001_pen_cup']" in problems_of(models_dir)


def test_when_exported_each_part_gets_a_print_stl_and_the_model_a_step(models_dir, tmp_path):
    out = tmp_path / "build"
    assert models.main(["--models-dir", str(models_dir), "export", "--out", str(out)]) == 0
    files = sorted(p.name for p in (out / "001_pen_cup").iterdir())
    assert files == ["001_pen_cup_assembly.step", "_asm_cup.stl", "print_cup.stl"]
    assert "001_pen_cup" in json.loads((out / "_colors.json").read_text())


LID_AND_PEN = '''

def pen_cup_with_lid():
    from fdm_samples import cyl
    parts = pen_cup()
    lid = rrect(72, 72, 12, 110, 4)                     # 2 above the rim; 3 down it sits on the walls
    parts["lid"] = Part(lid, lid, OFF)
    parts["pen_ref"] = Part(cyl(4, 2.4, 100), None, OFF, ref=True)
    return parts


SAMPLES["001_pen_cup"] = pen_cup_with_lid
'''
LID_MOTION = {"part": "lid", "against": "cup", "slide": [0, 0, -1], "free": [0, 1], "stop": [3]}


def with_lid_and_pen(models_dir, **changes):
    """The pen cup with a lid floating above it and a bought pen standing in it."""
    d = models_dir / "001_pen_cup"
    (d / "design.py").write_text((d / "design.py").read_text() + LID_AND_PEN)
    meta = json.loads((d / "model.json").read_text())
    meta["parts"] += [{"name": "lid", "qty": 1, "orientation": "Bottom down", "material": "PLA"},
                      {"name": "pen_ref", "qty": 1, "ref": True, "orientation": "Bought", "material": "A pen"}]
    meta["size_mm"] = [72, 72, 114]
    meta.update(changes)
    (d / "model.json").write_text(json.dumps(meta))


def test_when_the_motions_in_model_json_give_what_they_expect_check_reports_no_problems(models_dir, capsys):
    with_lid_and_pen(models_dir, motions=[LID_MOTION])
    assert problems_of(models_dir) == []
    out = capsys.readouterr().out
    assert "slide along (0, 0, -1) lid against cup +3 mm" in out and "expected stop" in out


def test_when_a_stop_in_model_json_does_not_catch_the_part_check_fails_on_verify(models_dir, capsys):
    with_lid_and_pen(models_dir, motions=[dict(LID_MOTION, stop=[1.5])])     # still 0.5 above the rim
    assert problems_of(models_dir) == ["verify.py: needs attention (see its output above)"]
    assert "+1.5 mm: overlap 0.000 mm3, expected stop  <-- CHECK" in capsys.readouterr().out


def test_when_a_snap_overlaps_more_than_its_limit_check_fails_on_verify(models_dir):
    with_lid_and_pen(models_dir, motions=[dict(LID_MOTION, stop=[], snap={"at": [3], "max_mm3": 0.5})])
    assert problems_of(models_dir) == ["verify.py: needs attention (see its output above)"]


def test_when_a_motion_names_a_part_that_design_py_does_not_build_check_names_it(models_dir):
    with_lid_and_pen(models_dir, motions=[dict(LID_MOTION, part="cap")])
    assert "model.json: motions[0].part 'cap' is not a part in design.py" in problems_of(models_dir)


def test_when_a_motion_is_neither_a_hinge_nor_a_slide_check_reports_it(models_dir):
    motion = {k: v for k, v in LID_MOTION.items() if k != "slide"}
    with_lid_and_pen(models_dir, motions=[motion])
    assert ("model.json: motions[0] needs either 'hinge' (two points on the axis) or 'slide' (a direction)"
            in problems_of(models_dir))


def test_when_view_has_no_direction_check_reports_it(models_dir):
    edit_json(models_dir / "001_pen_cup" / "model.json", view={"zoom": 1.2})
    assert any(p.startswith("model.json: 'view' must be") for p in problems_of(models_dir))


def test_when_a_bought_part_is_not_marked_ref_in_model_json_check_reports_it(models_dir):
    with_lid_and_pen(models_dir)
    meta_path = models_dir / "001_pen_cup" / "model.json"
    meta = json.loads(meta_path.read_text())
    del meta["parts"][-1]["ref"]
    meta_path.write_text(json.dumps(meta))
    assert ("model.json: part 'pen_ref' is a bought part in design.py (ref=True) but has no \"ref\": true"
            in problems_of(models_dir))


def test_when_a_model_with_a_bought_part_is_exported_the_bought_part_gets_no_print_stl(models_dir, tmp_path):
    with_lid_and_pen(models_dir)
    out = tmp_path / "build"
    assert models.main(["--models-dir", str(models_dir), "export", "--out", str(out)]) == 0
    files = sorted(p.name for p in (out / "001_pen_cup").iterdir())
    assert files == ["001_pen_cup_assembly.step", "_asm_cup.stl", "_asm_lid.stl", "_asm_pen_ref.stl",
                     "print_cup.stl", "print_lid.stl"]
