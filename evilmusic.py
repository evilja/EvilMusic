import time
import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import evilparser                   # EvilParser by Evil Wicca
import threading                    # MultiThread
import pygame
pygame.mixer.pre_init()
pygame.mixer.init()

runner = evilparser.parser()          # Create a EvilParser Object
config = runner.getconf("db.eparse")  # EvilParser - Parser db.eparse

eventkey = "90060x"

loop = False
killthread = False
def sPlayList(playlist):
    global loop,killthread
    try:
        for music in playlist:
            if eventkey == "90060x":
                print("")
            print("Playing: " + config["musicnames"][config["musiclinks"].index(music)])
            print("Queue: " + str(config["musiclinks"].index(music)+1) + "/" + str(len(playlist)))
            if eventkey == "90060x":
                print("> ",end="")
            pygame.mixer.music.load(music)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                if killthread:
                    break
                else:
                    continue
            if killthread:
                break
        if loop == True and not killthread:
            sPlayList(playlist)
    except pygame.error:
        exit(1)
playlistset = False
threads = []
def controlPanel():
    global loop, playlistset, threads
    while True:
        if not playlistset:
            print("Your Musics:")
            no = 1
            for music in config["musicnames"]:
                print(no,"--",music)
                no += 1
            print("\n")
            sel = input("(A)ll (L)oop (1-2-3-4-5-6-7-8...) (E)xit: ")
            sel = sel.lower()
            a = False
            if "a" in sel:
                playlist = config["musiclinks"]
                a = True
            if "l" in sel:
                loop = True
                sel = sel.replace("l","")
            if "e" in sel:
                print("Bye!")
                time.sleep(1)
                exit()
            if a == False:
                playlist = []
                selplay = sel.split("-")
                for i in selplay:
                    playlist.append(config["musiclinks"][int(i)-1])
            playlistset = True
            if len(threads) == 1:
                pygame.mixer.stop()
                killthread = True
            time.sleep(0.2)
            threads = []
            killthread = False
            threads.append(threading.Thread(target=sPlayList, args=(playlist,)))
            threads[0].start()
            time.sleep(0.2)
            print("Stop playlist and reselect musics = R\n> Turn On/Off Loop = L\n> Exit = E")
        else:
            listenForEvents()



def listenForEvents():
    global playlistset,loop,eventkey
    try:
        event = input("> ").lower()
        eventkey = event
    except KeyboardInterrupt:
        exit(1)
    if event == "l":
        if loop == True:
            loop = False
            print("Loop : False")
        else:
            loop = True
            print("Loop : True")
    if event == "r":
        playlistset = False
    if event == "e":
        exit()
    eventkey = 0
controlPanel()
