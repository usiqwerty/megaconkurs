import json
import os

import requests

ENCODING = 'utf-8'

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
}
delay = 30  # seconds


class FakeResponse:
	"Имитирует response от модуля requests"
	text: str

	def __init__(self, text):
		self.text = text


cache: dict[str, FakeResponse] = dict()
filemap: dict[str, str] = dict()  # url -> filename


def add_last_cache_entry_to_index(url: str) -> str:
	"""
	Связывает url с последним файлом в кэше
	@param url:
	@return:
	"""
	filename = f"{len(cache) + 1}.cache"
	filemap[url] = filename
	return filename


def get(url: str, force=False, do_not_update=False) -> FakeResponse:
	"""
	Выполняет запрос GET с сохранением в кэш
	@return:
	@param url: URL страницы
	@param force: Скачать, даже если страница уже сохранена в кэше
	@param do_not_update: Не скачивать повторно, если уже сохранено
	@return: Данные, лежащие по URL
	"""

	if (not do_not_update) and (url not in cache or force):
		print(f"[WEB] {url}")
		cache[url] = FakeResponse(requests.get(url, headers=headers).text)
		add_last_cache_entry_to_index(url)
	return cache[url]


def load_cache_from_disk():
	global filemap
	with open(os.sep.join(['cache', 'map.json']), encoding=ENCODING) as f:
		print('Loading mapping...')
		filemap = json.load(f)
	count = 0
	for url in filemap:
		fn = filemap[url]
		with open(os.sep.join(['cache', fn]), encoding=ENCODING) as f:
			cache[url] = FakeResponse(f.read())
			count += 1
	print(f"Loaded {count} files of cache")


def save_cache_to_disk():
	with open(os.sep.join(['cache', 'map.json']), 'w', encoding=ENCODING) as f:
		print('Saving mapping...')
		json.dump(filemap, f)

	count = 0
	for url in filemap:
		fn = filemap[url]

		if cache[url]:
			with open(os.sep.join(['cache', fn]), 'w', encoding=ENCODING) as f:
				f.write(cache[url].text)
				count += 1
	print(f'Saved {count} pages')
