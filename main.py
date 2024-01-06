# TODO:
print("DATA IS NOT SAVED AFTER DOWNLOADING")
print("DOS-ATTACK WARNING")
from datafetcher import web_requests
from datafetcher.async_fetcher import get_urls_from_many_hosts
# exit()
from parsers import hse, mipt, spbu, spbstu, itmo
from parsers.vuz import VuzRatingList
from admission import find_all_with_snils, list_to_dict
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

	# vuzes_data = {vuz: dict() for vuz in vuzes_links}

	links_for_all_vuzes_set = set()
	for vuz_name, link_dict in vuzes_links_hash.items():
		links_for_all_vuzes_set.update(link_dict)
	# links_for_all_vuzes_set += list(link_dict.values())

	links_for_all_vuzes = list(links_for_all_vuzes_set)

	# strange code
	for link, data in get_urls_from_many_hosts(links_for_all_vuzes_set, web_requests.get).items():
		if link not in web_requests.cache:
			print("Link was not saved in cache:", link)
		# web_requests.cache[link]=data

elif dblen<10:
	vuzes_links: dict[str, dict[str, str]] = {name: vuz.discover_links(offline=True) for name, vuz in vuzes.items()}
	# for vuz_name in vuzes_links:
	#	print(vuz_name, vuzes_links[vuz_name])
	#all_ratings=[]
	vuz_name="СПбГУ"
	print(f"Parsing {vuz_name}...")
	for prog, link in vuzes_links[vuz_name].items():
		clist = vuzes[vuz_name].parse(link)
		for entry in clist:
			database.append_entry(entry)
		#all_ratings+=clist

	#d = list_to_dict(all_ratings)
	#r = find_all_with_snils(18515614679, d)
	#for abit in r:
	#	print(abit)
# web_requests.save_cache_to_disk()
r = database.find_all_by_snils(18515614679)
for x in r:
	print(x)