"""Names stay neutral and the skill stays in English (decisions recorded in the README)."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "fdm-minimal-design"
BRAND = re.compile(r"braun|\brams\b", re.IGNORECASE)
CJK = re.compile(r"[　-ヿ㐀-鿿＀-￯]")


def tracked_files():
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [ROOT / p for p in out.splitlines() if (ROOT / p).is_file()]


def test_no_file_or_directory_name_contains_braun_or_rams():
    assert [str(p.relative_to(ROOT)) for p in tracked_files() if BRAND.search(str(p.relative_to(ROOT)))] == []


def test_no_python_code_or_comment_contains_braun_or_rams():
    hits = [str(p.relative_to(ROOT)) for p in tracked_files()
            if p.suffix == ".py" and p.name != "test_naming.py" and BRAND.search(p.read_text(encoding="utf-8"))]
    assert hits == []


def test_no_model_document_names_braun_or_rams():
    # The look-alike check in each rationale.md describes products by kind, not by brand.
    hits = [str(p.relative_to(ROOT)) for p in (ROOT / "models").rglob("*.md")
            if BRAND.search(p.read_text(encoding="utf-8"))]
    assert hits == []


def test_the_skill_name_in_skill_md_is_neutral_and_matches_its_folder():
    front = SKILL.joinpath("SKILL.md").read_text(encoding="utf-8").split("---")[1]
    name = re.search(r"^name:\s*(\S+)", front, re.M).group(1)
    assert name == SKILL.name and not BRAND.search(name)


def test_the_skill_description_fits_the_1024_character_limit():
    front = SKILL.joinpath("SKILL.md").read_text(encoding="utf-8").split("---")[1]
    description = re.search(r"^description:\s*(.+)$", front, re.M).group(1)
    assert len(description) <= 1024


def test_the_skill_documents_figures_and_scripts_contain_no_japanese_text():
    hits = [str(p.relative_to(ROOT)) for p in SKILL.rglob("*")
            if p.suffix in {".md", ".py", ".svg", ".txt"} and CJK.search(p.read_text(encoding="utf-8"))]
    assert hits == []
