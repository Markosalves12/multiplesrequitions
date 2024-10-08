import asyncio
import aiohttp


class MultipleRequisition:
    def __init__(self, urls, batch_size = 31):
        # lista de urls para serem solcitadas
        self.urls = urls
        # tamanho do lote de url
        self.batch_size = batch_size

    async def make_requisition(self, session, url):
        async with session.get(url) as response:
            # Lê o conteúdo da resposta e faz o parsing para JSON
            return await response.json()

    async def make_batch_requisition(self, session, batch_urls):
        tasks = [self.make_requisition(session, url) for url in batch_urls]
        return await asyncio.gather(*tasks)

    async def make_assincronous_requisition(self):
        async with aiohttp.ClientSession() as session:
            # Dividir as URLs em lotes
            batches = [self.urls[i:i + self.batch_size] for i in range(0, len(self.urls), self.batch_size)]

            # Fazer requisições em lotes
            results = []
            for batch in batches:
                results.extend(await self.make_batch_requisition(session, batch))

            # retorna uma lista de JSONS com as respostas disponiveis
            return results
            
    # função que é chamada no corpo do código
    def make_requisitions(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.make_assincronous_requisition())
