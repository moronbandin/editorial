from pathlib import Path
import shutil

BASE = Path("~/Documents/editorial/new/grego/unidades").expanduser()

for unit_dir in BASE.iterdir():
    if not unit_dir.is_dir():
        continue

    exercises = unit_dir / "exercises" / "exercises.md"
    source_dir = unit_dir / "source"

    if not exercises.exists():
        continue

    source_dir.mkdir(exist_ok=True)

    destination = source_dir / "exercises_original.md"

    shutil.copy2(exercises, destination)

    print(f"✓ {unit_dir.name}")

print("\n✅ Copias creadas en source/exercises_original.md")
