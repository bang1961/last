import os
import requests
import datetime
import time

class valid_api:
    def __init__(self, count=10):
        self.host = 'http://127.0.0.1:9007/'
        self.urls = [
            '', 
            'history/',
            ]
        self.result = dict()
        self.count = count

    def validation(self):
        for url in self.urls:
            full_url = self.host + url
            results = []
            for i in range(self.count):
                start = datetime.datetime.now()
                res = requests.get(full_url)
                assert res.status_code == 200
                passed_t = datetime.datetime.now() - start
                results.append(passed_t.total_seconds())
                time.sleep(0.1)
                print(f'\rturn: {i + 1}', end='')
            print()
            print(url)
            print(sum(results) / self.count)
            self.result[url] = results

    def save_results(self):
        BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(BASE_DIR, f'{self.count}_api_validation.txt'), 'w') as f:
            for k,v in self.result.items():
                doc = f"api: {k}\n"
                doc += f'mean: {sum(v) / len(v):.2f}\n'
                doc += f'max: {max(v):.2f}\n'
                doc += f'min: {min(v):.2f}\n\n'
                f.write(doc)

    

if __name__ == '__main__':
    tester = valid_api(100)
    tester.validation()
    tester.save_results()