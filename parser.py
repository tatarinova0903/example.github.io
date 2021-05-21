import re
import sys
import requests
import time

URL = 'https://git.iu7.bmstu.ru'
LOGIN_URL = 'https://git.iu7.bmstu.ru/users/sign_in'

login = input('Login: ')
password = input('Password: ')

session = requests.Session()

sign_in_page = session.get(LOGIN_URL).content
for line in sign_in_page.decode().split('\n'):
    m = re.search('name="authenticity_token" value="([^"]+)"', line)
    if m:
        break

token = None
if m:
    token = m.group(1)

if not token:
    print('Unable to find the authenticity token')
    sys.exit(1)

data = {'user[login]': login,
        'user[password]': password,
        'authenticity_token': token}

r = session.post(LOGIN_URL, data=data)
if r.status_code != 200 or session.get(URL).text.find("Remember me") != -1:
    print('Failed to log in')
    sys.exit(1)

for line in session.get(URL).text.split('\n'):
    if re.search('iu7-cprog-labs-2021', line):
        pr_url = line.split('href="')[1]
        pr_url = pr_url[:pr_url.find('"')]
        break

all_jobs_url = 'https://git.iu7.bmstu.ru' + pr_url + '/-/jobs'

job_number = 1
for line in session.get(all_jobs_url).text.split('\n'):
    if re.search('ci-status ci-', line):

        '''раскомментить, если нужно протетстить НЕ последний job, и указать его порядковый номер после !='''
        # if job_number != 8:
        #     job_number += 1
        #     continue

        target_job_url = line.split('href="')[1]
        target_job_url = target_job_url[:target_job_url.find('"')]
        break

target_job_num = target_job_url.split('/')[-1]
# target_job_num = '174608'
# target_job_url = 'https://git.iu7.bmstu.ru' + '/'.join(target_job_url.split('/')[:-1]) + f'/{target_job_num}/raw'
target_job_url = 'https://git.iu7.bmstu.ru' + target_job_url + '/raw'
# print(target_job_url)

count = 0
print(f'\nJob #{target_job_num}', end='')
job_data = session.get(target_job_url).text
if 'Job ' in job_data:
    print(':' + job_data.split("Job")[1][:job_data.split("Job")[1].find("\n")])
else:
    print(': running')
if 'Uploading artifacts' in job_data:
    for line in job_data.split('\n'):
        if (line.find('lab') == 0 or 'of' in line) and 'SKIPPED' not in line and 'ANOTHER TASK' not in line:
            if line.find('lab') == 0 and line.split('_')[1][0] != str(count):
                count += 1
                print(f'Task {count}:')
            print(line)
else:
    printed_lines = 0
    while 'Uploading artifacts' not in job_data:
        line_number = 0
        job_data = session.get(target_job_url).text
        for line in job_data.split('\n'):
            if (line.find('lab') == 0 or 'of' in line) and 'SKIPPED' not in line and 'ANOTHER TASK' not in line:
                line_number += 1
                if line_number > printed_lines:
                    if line.find('lab') == 0 and line.split('_')[1][0] != str(count):
                        count += 1
                        print(f'Task {count}:')
                    print(line)
                    printed_lines += 1
        time.sleep(3)
    time.sleep(5)
    job_data = session.get(target_job_url).text
    print('Job' + job_data.split("Job")[1][:job_data.split("Job")[1].find("\n")])

URL = 'https://tatarinova0903.github.io'
session2 = requests.Session()
data = {'name': 'Dasha'}
r = session2.post(LOGIN_URL, data=data)
print("RETURNED CODE:", r)
print(requests.post(URL , data).text)

