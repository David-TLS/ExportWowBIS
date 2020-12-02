from fetch_urls import FetchUrls

# download an decode to utf8 a collection of url
class FetchHtml(FetchUrls):
    def __enter__(self):
        responses = []
        for response in super().__enter__():
            response['content'] = response['content'].decode('utf8')
            responses.append(response)
        return responses
