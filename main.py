# TODO:
print("DATA IS NOT SAVED AFTER DOWNLOADING")
print("DOS-ATTACK WARNING")
from datafetcher import web_requests
from datafetcher.async_fetcher import get_urls_from_many_hosts
# exit()
from vuzes import hse, mipt, spbu, spbstu, itmo
from vuzes.vuz import VuzRatingList

web_requests.load_cache_from_disk()
vuz_objects: dict[str, VuzRatingList] = {
	"ВШЭ": hse.HSE(),
	"МФТИ": mipt.MIPT(),
	"СПбГУ": spbu.SPbU(),
	"СПбПУ": spbstu.SPbSTU(),
	"ИТМО": itmo.ITMO(),
}
if len(web_requests.cache) < 10:
	print('Discover')
	vuzes_links = {name: vuz.discover_links() for name, vuz in vuz_objects.items()}
	"""		# "ВШЭ": hse.discover_links(),
		# "МФТИ": mipt.discover_links(),
		"СПбГУ": spbu.discover_links(),
		"СПбПУ": spbstu.discover_links(),
		"ИТМО": itmo.discover_links(),
	"""
	print('Ready')
	vuzes_links_hash = {k: set(v) for k, v in vuzes_links.items()}

	vuzes_data = {vuz: dict() for vuz in vuzes_links}

	links_for_all_vuzes = []
	for name, link_dict in vuzes_links.items():
		links_for_all_vuzes += list(link_dict.values())

	# strange code
	for link, data in get_urls_from_many_hosts(links_for_all_vuzes, web_requests.get).items():
		if link not in web_requests.cache:
			print("Link was not saved in cache:", link)
	# web_requests.cache[link]=data

else:
	vuzes_links = {name: vuz.discover_links(offline=True) for name, vuz in vuz_objects.items()}

# web_requests.save_cache_to_disk()
