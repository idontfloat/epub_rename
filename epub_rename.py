import argparse
import logging
import os
import platform
import re
from ebooklib import epub
from pathlib import Path

# Ignore ebooklib warning: 'In the future version we will turn default option ignore_ncx to True.'
import warnings
warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s: %(message)s")
ebook_suffix = ".epub"

def log_info(message, quiet=False):
	logger.info(message)
	if not quiet:
		print(message)

def get_ebook_title(ebook):
	return get_ebook_metadata(ebook, "title")

def get_ebook_author(ebook):
	return get_ebook_metadata(ebook, "creator")

def get_ebook_metadata(ebook, field):
	metadata = ebook.get_metadata("DC", field)
	return metadata[0][0] if metadata else None

def generate_filename(template, title, author):
	if template == "t":
		name = title
	elif template == "ta":
		name = f"{title} - {author}"
	elif template == "at":
		name = f"{author} - {title}"
	else:
		raise ValueError("Invalid template option. Please use 't', 'ta', or 'at'.")
	return clean_filename(name.replace(":", " -")) + ebook_suffix

def clean_filename(name):
	illegal_chars = r"[<>:\"/\\|?*]" if platform.system() == "Windows" else r"[:/]"
	return re.sub(illegal_chars, "", name)

def rename_ebook(template, ebook_file, dry_run=False, quiet=False):
	log_info(f"Opening file '{ebook_file}'...", quiet)
	
	try:
		ebook = epub.read_epub(ebook_file)
	except Exception as e:
		logger.error(f"Unable to open '{ebook_file}' as epub", exc_info=True)
		return
	
	ebook_title = get_ebook_title(ebook)
	ebook_author = get_ebook_author(ebook)

	if not ebook_title:
		log_info(f"Could not find title metadata for '{ebook_file}', skipping", quiet)
	elif not ebook_author:
		log_info(f"Could not find author metadata for '{ebook_file}', skipping", quiet)
	else:
		log_info(f"Title: {ebook_title} | Author: {ebook_author}", quiet)

		ebook_renamed = ebook_file.parent / generate_filename(template, ebook_title, ebook_author)
		log_info(f"File will be renamed '{ebook_renamed.name}'", quiet)

		if ebook_file != ebook_renamed:
			if not dry_run:
				try:
					os.rename(ebook_file, ebook_renamed)
				except Exception as e:
					logger.error(f"Unable to rename '{ebook_file}'", exc_info=True)
					return
				log_info(f"'{ebook_renamed}' renamed successfully", quiet)
			else:
				log_info(f"DRY RUN: '{ebook_file}' would have been renamed '{ebook_renamed}'", False)
		else:
			if not dry_run:
				logger.warning(f"'{ebook_renamed}' already exists, skipping")
			else:
				logger.warning(f"DRY RUN: '{ebook_renamed}' already exists")

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--name", choices=["t", "ta", "at"], default="t", help="Set the naming template with options 't' for '<title>', 'ta' for '<title> - <author>' or 'at' for '<author> - <title>'.")
	parser.add_argument("-p", "--paths", nargs="*", default=None, help=f"List file and/or directory paths. Will rename *{ebook_suffix} files only.")
	parser.add_argument("-q", "--quiet", action="store_true", help=f"If provided, supress output file renaming *{ebook_suffix} files.")
	parser.add_argument("--dry-run", action="store_true", help=f"If provided, perform a dry run without renaming any *{ebook_suffix} files.")
	args, extra_args = parser.parse_known_args()
	
	if not args.paths:
		args.paths = [Path.cwd()] if not extra_args else extra_args
	
	for path in args.paths:
		file_or_dir = Path(path)
		if file_or_dir.is_file() and file_or_dir.suffix == ebook_suffix:
			rename_ebook(args.name, file_or_dir, args.dry_run, args.quiet)
		elif file_or_dir.is_dir():
			ebook_files = [file for file in file_or_dir.iterdir() if file.suffix == ebook_suffix]
			for ebook_file in ebook_files:
				rename_ebook(args.name, ebook_file, args.dry_run, args.quiet)
		else:
			logger.error(f"Invalid path: '{path}', skipping")

if __name__ == "__main__":
	main()
