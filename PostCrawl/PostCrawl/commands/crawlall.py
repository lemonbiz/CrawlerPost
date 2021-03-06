from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        spider_list = self.crawler_process.spiders.list()
        print('爬取开始')
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()

def run():
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawlall'])


if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler

    sched = BlockingScheduler()
    sched.add_job(run(), 'interval', days=1)
    sched.start()