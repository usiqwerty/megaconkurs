# TODO:
print("DATA IS NOT SAVED AFTER DOWNLOADING")
print("DOS-ATTACK WARNING")
from datafetcher import web_requests
from datafetcher.async_fetcher import get_urls_from_many_hosts

from parsers import hse, mipt, spbu, spbstu, itmo
from parsers.vuz import VuzRatingList

import database

web_requests.load_cache_from_disk()
database.start()
dblen=database.count_rows()
print(f"DB contains {dblen} rows")
vuzes: dict[str, VuzRatingList] = {
	"ВШЭ": hse.HSE(),
	"МФТИ": mipt.MIPT(),
	"СПбГУ": spbu.SPbU(),
	"СПбПУ": spbstu.SPbSTU(),
	"ИТМО": itmo.ITMO(),
}
if len(web_requests.cache) < 10:
	print('Discover')
	vuzes_links = {name: vuz.discover_links() for name, vuz in vuzes.items()}
	print('Ready')
	vuzes_links_hash: dict[str, set[str]] = {k: set(v) for k, v in vuzes_links.items()}

	links_for_all_vuzes_set = set()
	for vuz_name, link_dict in vuzes_links_hash.items():
		links_for_all_vuzes_set.update(link_dict)

	links_for_all_vuzes = list(links_for_all_vuzes_set)

	# strange code
	for link, data in get_urls_from_many_hosts(links_for_all_vuzes_set, web_requests.get).items():
		if link not in web_requests.cache:
			print("Link was not saved in cache:", link)
		# web_requests.cache[link]=data

elif dblen<10:
	vuzes_links: dict[str, dict[str, str]] = {name: vuz.discover_links(offline=True) for name, vuz in vuzes.items()}
	vuz_name="СПбГУ"
	print(f"Parsing {vuz_name}...")
	for prog, link in vuzes_links[vuz_name].items():
		clist = vuzes[vuz_name].parse(link)
		for entry in clist:
			database.append_entry(entry)

r = database.find_all_by_snils(18515614679)
for x in r:
	print(x)
# web_requests.save_cache_to_disk()
