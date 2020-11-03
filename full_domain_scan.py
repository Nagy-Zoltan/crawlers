from requests_html import AsyncHTMLSession
from requests_html import HTMLSession
import time
import sys
import re

session = HTMLSession()
asession = AsyncHTMLSession()

start_link = sys.argv[1]
if start_link[-1] != '/':
	start_link += '/'
domain = re.findall('\..*?\/', start_link)[0][1:-1] if 'www' in start_link else re.findall('\//.*?\/', start_link)[0][2:-1]
print(f'domain is: {domain}')

visited = set()
queue = []
print('Starting')

def bfs(link):
	visited.add(link)
	if link not in queue:
		queue.append(link)

	while queue:
	
		tasks = []
		for q in queue:
			async def get_links(link = q):
				try:
					r = await asession.get(link)
					for neighbour in set(r.html.absolute_links) - visited:
						if domain in neighbour:
							visited.add(neighbour)
							queue.append(neighbour)
							print(f'visited: {len(visited)}, in queue: {len(queue)}')
				except:
					print('Fail')

			tasks.append(get_links)

		queue.clear()
		asession.run(*tasks)

				

t1 = time.time()
bfs(start_link)
print(f'Finished crawling in: {time.time() - t1} seconds')

for vis in visited:
	print(vis)





