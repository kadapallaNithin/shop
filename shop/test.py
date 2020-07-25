import os
import sys
from time import sleep
from selenium import webdriver
import config
from threading import Thread

def start_server():
    os.system("python manage.py runserver")

argv  = sys.argv
if len(argv) > 1 and argv[1] == 'clear' :
    os.chdir('home/migrations')
    for file in os.listdir():
        if file  != "__init__.py" and os.path.isfile(file):
            os.remove(file)
    os.chdir('../..')
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    if len(argv) > 2  and argv[2] ==  'admin':
        os.system(f'python manage.py createsuperuser --username admin --email { config.email }')

t = Thread(target=start_server)
t.start()
sleep(2)
driver = webdriver.Chrome(config.path_for.chromedriver)
driver.get("localhost:8000")
sh  = driver.find_element_by_class_name('site-header')
anchors = sh.find_elements_by_tag_name('a')
sleep(0.2)
anchors[7].click()
p = driver.find_elements_by_name('prod_id')[0]
p.send_keys("-1\t")
add_category = driver.find_element_by_id('new_product').find_element_by_tag_name('a')
add_category.click()
n = driver.find_elements_by_name('name')[0]
n.send_keys("Cement")
sleep(0.3)
n.submit()

p = driver.find_elements_by_name('prod_id')[0]
p.send_keys("-1\t")
n = driver.find_elements_by_name('category')[0]
n.send_keys("1")
n = driver.find_elements_by_name('name')[0]
n.send_keys("ACC Suraksha\t")
q = driver.find_elements_by_name('quantity')[0]
q.send_keys('100')
r = driver.find_elements_by_name('rate')[0]
r.send_keys('400')
sleep(0.3)
r.submit()

e = driver.find_elements_by_name('rate')[0]
e.send_keys('420')
e.submit()

#driver.get("locahost:8000")
sh  = driver.find_element_by_class_name('site-header')
anchors = sh.find_elements_by_tag_name('a')
anchors[6].click()

c = driver.find_elements_by_name('cust_id')[0]
c.send_keys('-1\t')
v = driver.find_element_by_id('data').find_element_by_tag_name('a')
v.click()

driver.find_elements_by_name('village')[0].send_keys("Kurthi")
driver.find_elements_by_name('mandal')[0].send_keys("Pitlam")
driver.find_elements_by_name('district')[0].send_keys("Kamareddy")
sleep(0.3)
driver.find_elements_by_tag_name('form')[0].submit()

c = driver.find_elements_by_name('cust_id')[0]
c.send_keys('-1\t')
driver.find_elements_by_name('address_id')[0].send_keys("1\t")
driver.find_elements_by_name('name')[0].send_keys('Kadapalla Mallappa\t')
sleep(0.3)
driver.find_elements_by_tag_name('form')[0].submit()

driver.find_elements_by_name('particular')[0].send_keys("1\t")
driver.find_elements_by_name('rate')[0].send_keys('450\t')
driver.find_elements_by_name('quantity')[0].send_keys('4\t')
sleep(0.2)
driver.find_elements_by_tag_name('form')[0].submit()
sleep(0.2)
driver.find_elements_by_tag_name('form')[1].submit()

sleep(2)
driver.quit()