#!usr/bin/env python3

# Date: 02-08-18, Feb ~ 8th 2018 | Synchronocy
# Project: Discordhub.com Scraper
# Lul I bombed their discord

import requests
import string
import sys
#from pasteee import *
from threading import Thread
from queue import Queue

discord = 'http://discordhub.com'
discordservers = 'https://discordhub.com/servers/list?page='
httptag = 'https'
filename = 'discordlinks.txt'

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

def removedupes(inputfile, outputfile):
        lines=open(inputfile, 'r').readlines()
        lines_set = set(lines)
        out=open(outputfile, 'w')
        for line in lines_set:
                out.write(line)
        print('\nScan completed.\nRemoved any/all dupes.')
page = 1

def resolver(flink):
    r = requests.get(flink)
    resa = r.url
    resb = resa.replace("discordapp.com/invite","discord.gg")
    resb = resb + '\n'
    if 'https://discord.gg/' in resb:
        #print(resb)
        with open("discordlinks.txt","a") as handle:
            handle.write(resb)
            handle.close()
    else:
        pass
        
def backend(page):
    pool = ThreadPool(500)
    src = requests.get(discordservers + page).text
    links = src.split('<a href="')
    for link in links:
        link = link.split('"')[0].replace("/show","\n")
        flink = discord+link
        flink.replace("javascript:void(0);","").replace("https://discordhub.com/servers/list","")
        if 'http://discordhub.com/servers/' and '/invite/' in flink:
            pool.add_task(resolver,flink)

def main():
    pool = ThreadPool(500)
    amt = input("Page count: ")
    for x in range(1,int(amt)):
        backend(str(x))
    removedupes(filename,filename)
    pool.wait_completion()
    print("[+] Your list of discord links are located at: \nnote discord links may still be saving to the document.")
    print(filename)
    
if __name__ == '__main__':
    main()
    sys.exit()
