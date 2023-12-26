import asyncio
from urllib.parse import urlparse
#from classes import FakeResponse
from . import web_requests
__all__=['get_urls_from_many_hosts']
def group_urls(urls: list[str]):
    servers=dict()
    for url in urls:
        host=urlparse(url).netloc
        if host not in servers:
            servers[host]=[url]
        else:
            servers[host].append(url)
    return list(servers.values())

async def get_urls_from_same_host(url_list: list[str], get_func) -> dict[str, str|bytes]:
    results=dict()
    for url in url_list:
        resp = get_func(url)
        results[url]=resp.text
        await asyncio.sleep(web_requests.delay)
    return results


async def async_get_urls_from_many_hosts(urls: list[str], get_func):
    tasks = []
    for host_group in group_urls(urls):
        tasks.append( asyncio.create_task( get_urls_from_same_host(host_group, get_func)) )

    dicts=[]
    for t in tasks:
        dicts.append (await t)

    result=dict()
    for group in dicts:
        for k,v in group.items():
            result[k]=v
    return result

def get_urls_from_many_hosts(url_list: list[str], get_func) -> dict[str,str]:
    return asyncio.run(async_get_urls_from_many_hosts(url_list, get_func))
"""
async def a(x):
    return 1+x
async def run():
    t1=asyncio.create_task(a(4))
    r=await t1
    print(r)
asyncio.run(run())
"""