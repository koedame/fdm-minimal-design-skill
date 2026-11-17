import zipfile

import build_skill


def names(path):
    with zipfile.ZipFile(path) as zf:
        return zf.namelist()


def test_when_built_every_file_sits_under_one_folder_named_after_the_skill(tmp_path):
    entries = names(build_skill.build(tmp_path, with_step=False))
    assert entries and all(n.startswith("fdm-minimal-design/") for n in entries)


def test_when_built_the_bundle_holds_skill_md_references_scripts_and_licence(tmp_path):
    entries = set(names(build_skill.build(tmp_path, with_step=False)))
    for n in ("SKILL.md", "LICENSE.txt", "references/05_catalog.md", "scripts/fdm_samples.py",
              "scripts/verify.py", "scripts/render.py", "scripts/viewer.py", "scripts/viewer/page.html",
              "scripts/viewer/fdm-viewer.js", "scripts/viewer/part-menu.js", "scripts/viewer/dimensions.js",
              "scripts/viewer/page.js", "scripts/viewer/three.min.js", "scripts/viewer/three-LICENSE.txt",
              "assets/samples/overview.png"):
        assert f"fdm-minimal-design/{n}" in entries


def test_when_python_caches_exist_in_the_skill_folder_they_stay_out_of_the_bundle(tmp_path):
    cache = build_skill.SKILL_DIR / "scripts" / "__pycache__"
    cache.mkdir(exist_ok=True)
    (cache / "stray.cpython-311.pyc").write_bytes(b"")
    try:
        entries = names(build_skill.build(tmp_path, with_step=False))
    finally:
        (cache / "stray.cpython-311.pyc").unlink()
    assert not [n for n in entries if "__pycache__" in n or n.endswith(".pyc")]


def test_when_built_twice_from_the_same_files_the_entries_are_identical(tmp_path):
    a = build_skill.build(tmp_path / "a", with_step=False).read_bytes()
    b = build_skill.build(tmp_path / "b", with_step=False).read_bytes()
    assert a == b
