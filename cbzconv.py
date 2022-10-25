#!/usr/bin/env python

import os
import tempfile
import shutil
import argparse
import re
from PIL import Image

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

parser = argparse.ArgumentParser(description='Converts Comic Book Archives to PDF')
parser.add_argument('input_files', type=str, nargs='+', help='files to be converted')
parser.add_argument('--output-dir', metavar='path', dest="output_dir", default=".", type=str, help='output directory')
parser.add_argument('--no-landscape', dest='no_landscape', action='store_true', help='flip all landscape-oriented pages')
parser.add_argument('--paper-size', metavar='size', dest="paper_size", default="SameAsPage", type=str, help='set a fixed paper size')

args = parser.parse_args()
page_size = (0, 0)

match args.paper_size:
	case 'A4':
		page_size = (2480, 3508)
	case 'A5':
		page_size = (1748, 2480)
	case 'B6':
		page_size = (1476, 2079)
	case 'SameAsPage':
		pass
	case other:
		print("Unsupported paper size. Supported values are: A4, A5, B6, SameAsPage (default)")
		exit()


if not os.path.isdir(args.output_dir):
	print("Output directory doesn't exist")
	exit()
		
for input_file in args.input_files:
	if not os.path.isfile(input_file):
		print(f'File {input_file} not found. Skipping.')
		continue
	
	temp_dir = tempfile.mkdtemp()
	basename, extension = os.path.splitext(os.path.basename(input_file))
	
	match extension.upper():
		case '.CBZ':
			shutil.unpack_archive(input_file, temp_dir, 'zip')
		case '.CBT':
			shutil.unpack_archive(input_file, temp_dir, 'tar')
		case other:
			print(f'File {input_file} not recognized. Skipping.')
			continue
		
	images = []
	for image in os.listdir(temp_dir):
		images.append(os.path.join(temp_dir, image))
		
	images = natural_sort(images)
	pages = []
	
	for image in images:
		page = Image.open(image).convert('RGB')
		width, height = page.size
		if width > height and args.no_landscape:
			page = page.rotate(90, expand = 1)
		if page_size != (0, 0):
			base = Image.new('RGB', page_size, (255, 255, 255))
			page.thumbnail(page_size)
			pos = tuple(map(lambda i, j: int((i - j) / 2), base.size, page.size))
			base.paste(page, pos)
			pages.append(base)
			continue
		pages.append(page)
    	
	first_page = pages.pop(0)
	output_file = os.path.join(args.output_dir, basename + '.pdf')
	first_page.save(output_file, "PDF" , resolution=100.0, save_all=True, append_images=pages)	

