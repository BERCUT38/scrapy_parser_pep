import datetime as dt
from pathlib import Path

from pep_parse.settings import DATETIME_FORMAT

BASE_DIR = Path(__file__).parents[1]
TABLE_HEADER = 'Статус,Количество\n'


class PepParsePipeline:
    counter = {}

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item['status'] not in PepParsePipeline.counter:
            PepParsePipeline.counter[item['status']] = 0

        PepParsePipeline.counter[item['status']] += 1

        return item

    def close_spider(self, spider):
        formatted_time = str(dt.datetime.now().strftime(DATETIME_FORMAT))
        filename = 'status_summary_' + formatted_time + '.csv'
        total = 0

        with open(
            BASE_DIR / 'results' / filename, mode='w', encoding='utf-8'
        ) as f:

            f.write(TABLE_HEADER)

            for key, value in PepParsePipeline.counter.items():
                f.write(f'{key},{value}\n')
                total += value

            f.write(f'Total,{total}\n')
