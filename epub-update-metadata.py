import argparse
import logging
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

def set_title(ebook, title):
	set_metadata(ebook, "title", title)

def set_author(ebook, author):
	set_metadata(ebook, "creator", author)

def set_metadata(ebook, field, value):
	ebook.set_unique_metadata("DC", field, value)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--title", nargs="?", help="Book title to be updated to.")
	parser.add_argument("-a", "--author", nargs="?", help="Book authors sto be updated to.")
	parser.add_argument("-p", "--path", help=f"Provide *{ebook_suffix} path.")
	parser.add_argument("-q", "--quiet", action="store_true", help=f"If provided, supress info output.")
	args = parser.parse_args()

	if not args.path:
		logger.error("Path must be provided")
		return

	if not args.title and not args.author:
		logger.error("Title and/or author must be provided")
		return

	path = Path(args.path)
	if not path.is_file() or not path.suffix == ebook_suffix:
		logger.error(f"Invalid file: {path}")
		return

	try:
		ebook = epub.read_epub(path)
	except Exception as e:
		logger.error(f"Unable to open {path} as epub", exc_info=True)
		return

	if args.title:
		orig_title = get_ebook_title(ebook)
		set_title(ebook, args.title)
		log_info(f"Original title: {orig_title}\nUpdated title: {args.title}", args.quiet)

	if args.author:
		orig_author = get_ebook_author(ebook)
		set_author(ebook, args.author)
		log_info(f"Original author: {orig_author}\nUpdated author: {args.author}", args.quiet)
	
	try:
		epub.write_epub(path, ebook)
		log_info(f"{path} updated successfully", args.quiet)
	except Exception as e:
		logger.error(f"Unable to write to epub {path}", exc_info=True)

if __name__ == "__main__":
	main()
