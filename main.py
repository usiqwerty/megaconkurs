from typing import NamedTuple

import database
from concurs import VUZ_SPBU
from datafetcher import web_requests
from datafetcher.async_fetcher import get_urls_from_many_hosts
from parsers import hse, mipt, spbu, spbstu, itmo
from parsers.vuz import VuzRatingList

web_requests.load_cache_from_disk()
database.start()
dblen = database.count_rows()
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

elif dblen < 10:
	vuzes_links: dict[str, dict[str, str]] = {name: vuz.discover_links(offline=True) for name, vuz in vuzes.items()}
	vuz_name = "СПбГУ"
	print(f"Parsing {vuz_name}...")
	for prog, link in vuzes_links[vuz_name].items():
		clist = vuzes[vuz_name].parse(link)
		for entry in clist:
			database.append_entry(entry)

# r = database.find_all_by_program_extended("38.03.01", VUZ_SPBU)
# for x in r:
#	print(x)

# web_requests.save_cache_to_disk()
Vuz = NamedTuple("vuz", [("name", str), ("code", str), ("full_name", str)])


def find_all_vuzes():
	return [Vuz("СПбГУ", VUZ_SPBU, "Сакнто ываыва")]


def get_vuz_info(vuz: str):
	print(f"looking for {vuz} vuz")
	if vuz == VUZ_SPBU:
		return Vuz("СПбГУ", "spbu", "Санкт-передфыощшфывофы")


def get_rating(vuz, program):
	return database.find_all_by_program_extended(program, vuz)


def get_vuz_programs(vuz):
	return database.get_all_programs_by_vuz(VUZ_SPBU)
