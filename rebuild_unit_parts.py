#!/usr/bin/env python3

from pathlib import Path
import re

BASE = Path.home() / "Documents/editorial/new/grego/unidades"

SECTION_MAP = {
    "α": "alpha",
    "β": "beta",
    "γ": "gamma",
}

EXERCISE_START_RE = re.compile(
    r"\n(?=###\s+(?:Exercicios|REPASO|INNOVACIÓN)|####\s+)",
    re.IGNORECASE
)

SECTION_RE = re.compile(
    r"^###\s+([αβγ])(?:[^\n]*)\n(.*?)(?=^###\s+[αβγ](?:[^\n]*)\n|\Z)",
    re.DOTALL | re.MULTILINE
)

def clean(text: str) -> str:
    return text.strip() + "\n"

for unit_dir in sorted(BASE.iterdir()):
    if not unit_dir.is_dir():
        continue

    source = unit_dir / "source" / "original.md"
    if not source.exists():
        print(f"· Saltando {unit_dir.name}: non hai source/original.md")
        continue

    content = source.read_text(encoding="utf-8")

    texts_dir = unit_dir / "texts"
    exercises_dir = unit_dir / "exercises"

    texts_dir.mkdir(exist_ok=True)
    exercises_dir.mkdir(exist_ok=True)

    all_exercises = []

    sections = SECTION_RE.findall(content)

    if not sections:
        print(f"⚠️  {unit_dir.name}: non se detectaron seccións α/β/γ")
        continue

    for greek_letter, block in sections:
        section_id = SECTION_MAP.get(greek_letter)
        if not section_id:
            continue

        # Cortar texto no primeiro bloque claramente exercicio:
        # - ### Exercicios...
        # - ### REPASO
        # - #### a), #### A), etc.
        split = EXERCISE_START_RE.split(block, maxsplit=1)

        text_part = split[0].strip()
        exercise_part = ""

        if len(split) > 1:
            # Recuperar o separador perdido buscando desde o final do texto no bloque orixinal
            idx = block.find(split[1])
            exercise_part = block[idx:].strip() if idx != -1 else split[1].strip()

        # Escribir texto limpo
        (texts_dir / f"{section_id}.md").write_text(
            clean(text_part),
            encoding="utf-8"
        )

        # Acumular exercicios nun único ficheiro
        if exercise_part:
            all_exercises.append(
                f"# {greek_letter}\n\n{exercise_part.strip()}"
            )

    # Escribir único ficheiro de exercicios
    exercises_file = exercises_dir / "exercises.md"
    exercises_file.write_text(
        "\n\n---\n\n".join(all_exercises).strip() + "\n",
        encoding="utf-8"
    )

    # Baleirar antigos ficheiros se existen, para evitar confusión
    for old_name in ["innovacion.md", "repaso.md"]:
        old = exercises_dir / old_name
        if old.exists():
            old.unlink()

    print(f"✓ {unit_dir.name}")

print("\n✅ Textos e exercises.md reconstruídos correctamente.")
