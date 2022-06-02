import schedule
import subprocess
from tqdm import tqdm
import datetime
import os
from loguru import logger
from scrapy import spiderloader
from scrapy.utils import project


BASE_DIR = os.path.abspath(".")
file_name = os.path.join(BASE_DIR, f'log/{datetime.date.today()}.log')

# log_level = "DEBUG"
# # feature 字符串格式化
# logger.add(
#     file_name,
#     enqueue=True,
#     level=log_level,
#     format="【{level}】 | {time:YY年MM月DD日 HH时mm分} | {file}——{line} | {message}",
#     encoding="utf-8",
#     rotation="10 MB",
# )
# logger.opt(depth=1)


def crawl_work():
    settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    for index,spider in enumerate(tqdm(spiders)):
        logger.debug(f"目前即将开始运行第{index}个，文件为{spider}")
        subprocess.Popen(f'scrapy crawl {spider}').wait()


if __name__=='__main__':
    schedule.every(1).days.do(crawl_work)

    logger.info('当前时间为{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    while True:
        schedule.run_pending()