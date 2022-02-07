# python3.__version__: 3.x
import os

# pip package translate-toolkit: https://pypi.org/project/translate-toolkit/
from translate.storage.tmx import tmxfile

def read_tmx(filepath: os.path):
	# arg:
	# 	filepath: exists filepath, it is available for '.tmx'.
	# 	check to 'https://github.com/translate/translate' for other available format.

	if not os.path.exists(filepath):
		return f'can not found file: {filepath}'

	try:
		with open(filepath, 'rb') as f:
			file = tmxfile(f)
	except:
		return f'can not read file: {filepath}'

	source = []
	target = []

	for node in file.unit_iter():
		source.append(node.source)
		target.append(node.target)
	return source, target

def write_tmx(
	filepath: os.path, 
	source: list, target: list,
	sourceLanguage: str, targetLanguage: str,
	overwrite = False):
	# args:
	#	filepath: exists filepath or not.
	#	source: source sentences
	# 	target: target sentences
	# 	sourceLanguage: source language
	#	targetLanguage: target language
	#	overwirte: overwriting or not

	if not os.path.exists(filepath):
		XMLskeleton = """<?xml version="1.0" encoding="utf-8"?>
						<!DOCTYPE tmx SYSTEM "tmx14.dtd">
						<tmx version="1.4">
						<header></header>
						<body></body>
						</tmx>""".replace('  ', '')
		with open(filepath, 'w') as f:
			f.write(XMLskeleton)
	with open(filepath, 'rb') as f:
		file = tmxfile(f)

	if not overwrite:
		for unit in file.getunits():
			file.removeunit(unit)

	if not isinstance(source, list):
		source = [source]
	if not isinstance(target, list):
		target = [target]

	for src, tgt in zip(source, target):
		file.addtranslation(src, sourceLanguage, 
							tgt, targetLanguage)
	file.save()