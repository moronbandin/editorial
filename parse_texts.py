#!/usr/bin/env python3

from pathlib import Path
import re

BASE = Path.home() / "Documents/editorial/new/grego/unidades"

SECTION_MAP = {
    "α": "alpha",
    "β": "beta",
    "γ": "gamma",
}

for unit_dir in BASE.iterdir():

    if not unit_dir.is_dir():
        continue

    source_file = unit_dir / "source" / "original.md"

    if not source_file.exists():
        continue

    content = source_file.read_text(encoding="utf-8")

    # ==================================================
    # EXTRAER SECCIÓNS α β γ
    # ==================================================

    section_pattern = re.compile(
        r"###\s+([αβγ])(?:.*?)\n(.*?)(?=\n###\s+[αβγ]|\Z)",
        re.DOTALL
    )

    sections = section_pattern.findall(content)

    for greek_letter, block in sections:

        name = SECTION_MAP.get(greek_letter)

        if not name:
            continue

        # ==========================================
        # SEPARAR TEXTO DE EXERCICIOS
        # ==========================================

        split = re.split(
            r"\n###\s+Exercicios de INNOVACIÓN",
            block,
            maxsplit=1
        )

        text_part = split[0].strip()

        # gardar texto
        text_file = unit_dir / "texts" / f"{name}.md"
        text_file.write_text(text_part + "\n", encoding="utf-8")

        # se hai exercicios
        if len(split) > 1:

            exercises_block = split[1]

            # innovación
            innov_split = re.split(
                r"\n###\s+(?:Exercicios de )?REPASO",
                exercises_block,
                maxsplit=1
            )

            innovacion = innov_split[0].strip()

            innov_file = unit_dir / "exercises" / "innovacion.md"

            previous = ""
            if innov_file.exists():
                previous = innov_file.read_text(encoding="utf-8").strip()

            with innov_file.open("w", encoding="utf-8") as f:
                if previous:
                    f.write(previous + "\n\n")
                f.write(f"# {name}\n\n")
                f.write(innovacion)
                f.write("\n")

            # repaso
            if len(innov_split) > 1:

                repaso = innov_split[1].strip()

                repaso_file = unit_dir / "exercises" / "repaso.md"

                previous = ""
                if repaso_file.exists():
                    previous = repaso_file.read_text(encoding="utf-8").strip()

                with repaso_file.open("w", encoding="utf-8") as f:
                    if previous:
                        f.write(previous + "\n\n")
                    f.write(f"# {name}\n\n")
                    f.write(repaso)
                    f.write("\n")

    print(f"✓ {unit_dir.name}")

print("\n✅ Textos e exercicios separados.")
