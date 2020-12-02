import asyncio

from aiohttp import ClientSession


# fetch in parallel several urls
class FetchUrl():
    
    def __init__(self, urls):
        self.urls = urls
        self.lenght = len(urls)

    def __enter__(self):
        self.loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(FetchUrl.__run(self.urls, self.lenght))
        return self.loop.run_until_complete(future)

    def __exit__(self, type, value, traceback):
        if(self.loop.is_running()):
            self.loop.close()

    @staticmethod
    async def __fetch(url, session):
        async with session.get(url) as response:
            return {'origin': url, 'content': await response.read()}

    @staticmethod
    async def __bound_fetch(sem, url, session):
        # Getter function with semaphore.
        async with sem:
            return await FetchUrl.__fetch(url, session)


    @staticmethod
    async def __run(urls, lenght):
        tasks = []
        sem = asyncio.Semaphore(lenght)
        async with ClientSession() as session:
            for url in urls:
                task = asyncio.ensure_future(FetchUrl.__bound_fetch(sem, url, session))
                tasks.append(task)
            responses = asyncio.gather(*tasks)
            return await responses
