from CrawlerModule.WebCrawler import WebCrawler as crawler
from ServerModule.CrawlerServer import application as app
from SongManageModule.song_manage import Song_Mangaer as smang



class Programm:

    def __init__(self) -> None:
        self.server = None
        self.crawl = None
        pass


    def start_server(self):
        server = app()
        server.run()
        pass


    def start_web_crawler(self):
        self.crawl = crawler()
        if self.crawl.music_table == None:
            if not self.crawl.load_data_from_csv():
                self.crawl.search_hundred_songs_page()
                self.crawl.store_data_in_csv()
        print(self.crawl.music_table)
        pass
    

    def run_program(self):
        self.start_web_crawler()
        self.start_server()



if __name__ == '__main__':
    Programm().run_program()