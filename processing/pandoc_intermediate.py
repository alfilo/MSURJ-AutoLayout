from pathlib import Path
import subprocess


def create_tex_ir(input_docx, *, ir_tex_dir=None):
    project_root = Path.cwd()
    if ir_tex_dir is None:
        ir_tex_dir = project_root / "data" / "ir_tex"
    else:
        ir_tex_dir = Path(ir_tex_dir)
    paper_num = input_docx.stem

    output_dir = ir_tex_dir / paper_num
    output_dir.mkdir(parents=True, exist_ok=True)

    output_tex = output_dir / f"{paper_num}.tex"

    subprocess.run([
        "pandoc",
        str(input_docx),
        "--from=docx",
        "--to=latex",
        "--output", str(output_tex),
        "--standalone",
        f"--extract-media={output_dir}",
        "--wrap=none"
    ])

    media_dir = output_dir / "media"
    figures_dir = output_dir / "Figures"
    if media_dir.exists():
        if figures_dir.exists():
            shutil.rmtree(figures_dir)
        media_dir.rename(figures_dir)
    else:
        figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"Files created in:\n{output_dir.resolve()}")
    return output_dir
