# -*- coding: utf-8 -*-

import os
import zipfile

from pathlib import Path

import LO_extension.Scripts.python.maylibre as v


def create_missing_dir(p: Path) -> None:
    if not p.exists():
        p.mkdir(parents=True)


def build_templates(indir: str, outdir: str, exclude_dir: str = None) -> None:
    for dir_path, dirnames, filenames in os.walk(indir):
        if exclude_dir is not None and exclude_dir in dir_path:
            continue
        for name in filenames:

            if name == 'TemplateWindowState.xcu':
                infile_path = dir_path + '/' + name
                with open(infile_path, encoding='utf-8') as f:
                    instr = f.read()
                    for program in ['Writer', 'Calc', 'Impress', 'Draw']:
                        outfile_path = Path(dir_path.replace(indir, outdir, 1) + '/' + name.replace('Template', program))
                        create_missing_dir(outfile_path.parent)
                        with outfile_path.open('w', encoding='utf-8') as of:
                            of.write(instr.replace('%PROGRAM%', program))


if __name__ == "__main__":
    plugin_version = v.__version__

    print('LibreOffice plugin version: %s' % plugin_version)

    # Populate extension with files from the template dir
    EXTENSION_NAME = 'maylibre'
    EXTENSION_SOURCE_DIRS = 'LO_extension'
    EXTENSION_TEMPLATE_DIRS = 'templates'
    EXCLUDE_DIR = "pycache"

    build_templates(EXTENSION_TEMPLATE_DIRS, EXTENSION_SOURCE_DIRS, EXCLUDE_DIR)

    outdir = Path("./out/")
    create_missing_dir(outdir)
    create_missing_dir(Path("./Office/UI"))
    extension_archive = zipfile.ZipFile(outdir / f"{EXTENSION_NAME}.oxt", 'w')
    for dir_path, dirnames, filenames in os.walk(EXTENSION_SOURCE_DIRS):
        if EXCLUDE_DIR in dir_path:
            continue
        for name in filenames:
            file_path = dir_path + '/' + name
            print(file_path)
            if name == 'description.xml':
                description_content = open(file_path).read().replace('%PLUGIN_VERSION%', plugin_version)
                extension_archive.writestr(name, description_content)
            else:
                extension_archive.write(file_path, os.path.relpath(file_path, EXTENSION_SOURCE_DIRS))

    extension_archive.close()
    print('Successfully built LibreOffice plugin version %s' % plugin_version)
