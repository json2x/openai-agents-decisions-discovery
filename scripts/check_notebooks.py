"""Check shared notebooks without executing code or making API calls."""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for path in sorted(ROOT.glob("*.ipynb")):
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4, f"{path.name}: expected notebook format 4"
    for index, cell in enumerate(notebook["cells"], 1):
        if cell["cell_type"] != "code":
            continue
        label = f"{path.name}:cell {index}"
        assert cell.get("execution_count") is None, f"{label}: clear execution counts"
        assert not cell.get("outputs"), f"{label}: clear saved outputs"
        source = "".join(cell["source"])
        compile(source, label, "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.startswith("RUN_"):
                        assert isinstance(node.value, ast.Constant) and node.value.value is False, (
                            f"{label}: disable {target.id} before sharing"
                        )
    print(f"OK: {path.name}")

assert (ROOT / "outputs/learning-session/assets/jacket-evidence.png").is_file()
print("Notebook syntax, sharing defaults, and image evidence checked; no API calls executed.")
