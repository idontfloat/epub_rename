# EPUB Rename
Script *epub-rename.py* will extract EPUB title and author metadata and rename the file as `<title>.epub`, `<title> - <author>.epub` or `<author> - <title>.epub`.

## Usage
All EPUB files in the current working directory will be renamed. This can be changed by listing files or directories with `-p`, `--paths` or without a flag. A mix of files and directories can be listed. If a directory is passed all contained EPUB files will be renamed (subdirectories will be ignored).

By default files will be renamed as `<title>.epub`. The arument `-n` or `--name` can be used to change the naming template with options `t` for `<title>.epub`, `ta` for `<title> - <author>.epub` or `at` for `<author> - <title>.epub`.

Use `-q` or `--quiet` to suppress info messages.

Use `--dry-run` to list changes without renaming.

## Update metadata
Additional script *epub-update-metadata.py* can be used to update metadata for a specified EPUB file. Currently, only title and/or author are supported.

Supply a valid EPUB with `-p`, `--path`. Specifiy title with `-t`, `--title` and/or author with `-a`, `--author`.

Use `-q` or `--quiet` to suppress info messages.