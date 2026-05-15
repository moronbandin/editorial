#!/usr/bin/env python3

from pathlib import Path
import shutil

BASE = Path.home() / "Documents/editorial/new/grego/unidades"

UNIT_YAML_TEMPLATE = """unit: {unit}
mathema: ""
title: ""
slug: "{slug}"
difficulty: medium
source: "{source}"

tags: []

focus: []
"""

README_TEMPLATE = """# Unidade {unit}

Estrutura editorial da unidade.
"""

for unit_dir in BASE.iterdir():

    if not unit_dir.is_dir():
        continue

    # Buscar markdown principal
    md_files = [
        f for f in unit_dir.glob("*.md")
        if not f.name.startswith("vocabulario")
        and "tagged" not in f.name
    ]

    if not md_files:
        continue

    main_md = md_files[0]

    unit_slug = unit_dir.name
    unit_number = unit_slug.split("-")[0]

    # =========================
    # CREAR CARPETAS
    # =========================

    folders = [
        "texts",
        "exercises",
        "vocabulary",
        "summaries",
        "assets",
        "source"
    ]

    for folder in folders:
        (unit_dir / folder).mkdir(exist_ok=True)

    # =========================
    # MOVER ORIXINAL
    # =========================

    source_original = unit_dir / "source" / "original.md"

    if not source_original.exists():
        shutil.copy(main_md, source_original)

    # =========================
    # MOVER TAGGED SE EXISTE
    # =========================

    tagged_files = list(unit_dir.glob("*tagged*.md"))

    for tagged in tagged_files:
        target = unit_dir / "source" / tagged.name
        if not target.exists():
            shutil.move(str(tagged), str(target))

    # =========================
    # VOCABULARIO
    # =========================

    vocab_files = list(unit_dir.glob("vocabulario*.md"))

    for vocab in vocab_files:
        target = unit_dir / "vocabulary" / "vocabulary.md"
        if not target.exists():
            shutil.move(str(vocab), str(target))

    # =========================
    # UNIT YAML
    # =========================

    unit_yaml = unit_dir / "unit.yaml"

    if not unit_yaml.exists():
        unit_yaml.write_text(
            UNIT_YAML_TEMPLATE.format(
                unit=unit_number,
                slug=unit_slug,
                source=f"source/original.md"
            ),
            encoding="utf-8"
        )

    # =========================
    # TEXTS PLACEHOLDERS
    # =========================

    for text_name in ["alpha.md", "beta.md", "gamma.md"]:
        path = unit_dir / "texts" / text_name
        if not path.exists():
            path.write_text("", encoding="utf-8")

    # =========================
    # EXERCISES PLACEHOLDERS
    # =========================

    for ex_name in ["innovacion.md", "repaso.md"]:
        path = unit_dir / "exercises" / ex_name
        if not path.exists():
            path.write_text("", encoding="utf-8")

    # =========================
    # SUMMARIES PLACEHOLDERS
    # =========================

    summary_files = [
        "language.md",
        "greek-world.md",
        "reading.md",
        "summary.md"
    ]

    for summary in summary_files:
        path = unit_dir / "summaries" / summary
        if not path.exists():
            path.write_text("", encoding="utf-8")

    # =========================
    # README
    # =========================

    readme = unit_dir / "README.md"

    if not readme.exists():
        readme.write_text(
            README_TEMPLATE.format(unit=unit_number),
            encoding="utf-8"
        )

print("✅ Estrutura creada correctamente.")
