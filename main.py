#TODO:
print("DATA IS NOT SAVED AFTER DOWNLOADING")
print("DOS-ATTACK WARNING")
#exit()
from vuzes import hse, mipt, spbu, spbstu, itmo
from analyse import get_programs_by_snils_in_vuz
from datafetcher import web_requests
from datafetcher.async_fetcher import get_urls_from_many_hosts

web_requests.load_cache_from_disk()

if len(web_requests.cache)<10:
    print('Discover')
    vuzes_links = {
        #"ВШЭ": hse.discover_links(),
        #"МФТИ": mipt.discover_links(),
        "СПбГУ":spbu.discover_links(),
        "СПбПУ":spbstu.discover_links(),
        "ИТМО":itmo.discover_links("01.03.02 09.03.01 09.03.02 09.03.03 09.03.04 10.05.01 38.03.05 02.03.01 02.03.02".split()),
    }
    print('Ready')
    vuzes_links_hash = { k: set(v) for k,v in vuzes_links.items()}

    vuzes_data= {vuz: dict() for vuz in vuzes_links}

    def precache_everything():
        links=[]
        for name, link_dict in vuzes_links.items():
            links+=list(link_dict.values())

        for link, data in get_urls_from_many_hosts(links, web_requests.get).items():
            if link not in web_requests.cache:
                print("Link was not saved in cache:", link)
                #web_requests.cache[link]=data



    precache_everything()
else:
    vuzes_links = {
        "ВШЭ": hse.discover_links(),
        "МФТИ": mipt.discover_links(),
        "СПбГУ": spbu.discover_links(),
        "СПбПУ": spbstu.discover_links(offline=True),
        "ИТМО": itmo.discover_links("01.03.02 09.03.01 09.03.02 09.03.03 09.03.04 10.05.01 38.03.05 02.03.01 02.03.02".split(), offline=True),
    }


#web_requests.save_cache_to_disk()