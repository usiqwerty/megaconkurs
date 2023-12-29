import asyncio
from typing import Iterable
from urllib.parse import urlparse

# from classes import FakeResponse
from . import web_requests

__all__ = ['get_urls_from_many_hosts']


def group_urls(urls: Iterable[str]):
	servers = dict()
	for url in urls:
		host = urlparse(url).netloc
		if host not in servers:
			servers[host] = [url]
		else:
			servers[host].append(url)
	return list(servers.values())


async def get_urls_from_same_host(urls: list[str], get_func) -> dict[str, str | bytes]:
	pages = dict()
	for url in urls:
		#TODO: async get request
		pages[url] = get_func(url).text
		await asyncio.sleep(web_requests.delay)
	return pages


async def async_get_urls_from_many_hosts(urls: Iterable[str], get_func):
	tasks = []
	for host_group in group_urls(urls):
		tasks.append(asyncio.create_task(get_urls_from_same_host(host_group, get_func)))

	pages_for_many_hosts = []
	for t in tasks:
		pages_for_many_hosts.append(await t)

	pages_many_hosts = dict()
	for pages_for_single_host in pages_for_many_hosts:
		for url, content in pages_for_single_host.items():
			pages_many_hosts[url] = content
	return pages_many_hosts


def get_urls_from_many_hosts(urls: Iterable[str], get_func) -> dict[str, str]:
	"""
	@param urls: Набор ссылок
	@param get_func: Функция, которая будет применяться к каждому URL
	@return: Содержимое страниц по ссылкам
	"""
	return asyncio.run(async_get_urls_from_many_hosts(urls, get_func))
