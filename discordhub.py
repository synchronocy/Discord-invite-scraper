#!usr/bin/env python3

# Date: 02-08-18, Feb ~ 8th 2018 | Synchronocy
# Project: Discordhub.com Scraper
# Lul I bombed their discord
import requests
from threading import Thread
from queue import Queue

discordhub = 'https://discordhub.com/'
pool = []
class Worker(Thread):
    """
    Pooling
    """

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as ex:
                pass
            finally:
                self.tasks.task_done()

class ThreadPool:
    """
    Pooling
    """

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """
        Add a task to be completed by the thread pool
        """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """
        Map an array to the thread pool
        """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """
        Await completions
        """
        self.tasks.join()
def scrape(counter):
    src = requests.get('https://discordhub.com/servers/list?page='+str(counter)).text
    links = src.split('<a href="')
    for link in links:
        if 'invite' in link:
            discord = requests.get(discordhub+link[:34])
            url = discord.url
            url = 'https://discord.gg/'+url[30:]
            print(url)
            with open('links.txt','a') as handle:
                handle.write(url+'\n')
def main():
    pool = ThreadPool(800)# be careful with this as it can actually rape your pc
    counter = 0
    for x in range(50): # in pages
        counter += 1
        pool.add_task(scrape,counter)
    pool.wait_completion()
    
main()
