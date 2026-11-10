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
