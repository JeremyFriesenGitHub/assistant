from bs4 import BeautifulSoup


class WebpageParserService:
    def __init__(self, webpage: BeautifulSoup):
        self.webpage = webpage
        self.__remove_non_content_elements()

    def get_title(self):
        title_tag = self.webpage.find("title")
        return title_tag.string if title_tag else None

    def get_text(self):
        return self.webpage.get_text(separator="\n")

    def __remove_non_content_elements(self):
        for tag in self.webpage(
            ["script", "style", "header", "footer", "nav", "noscript", "svg", "form"]
        ):
            tag.decompose()
