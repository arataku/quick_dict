import os
import time
import pygame
import keyboard
import pyperclip
import win32gui
import pyautogui
import math


class Search:
    def __init__(self) -> None:
        with open("ejdict-hand-utf8.txt", "r", encoding='UTF-8') as f:
            tmp = f.readlines()
        tmp = [[j.replace("\n", "") for j in i.split("\t")] for i in tmp]
        self.dict = {}
        for i in tmp:
            if len(i) == 2:
                self.dict[i[0].lower()] = i[1]
        print("ready")

    def search(self, word):
        word_tmp = word.replace(" ", "").lower()
        if word_tmp in self.dict:
            return self.dict[word_tmp]
        else:
            return "Not Found"


def split_by_length(txt, length):
    return [txt[i * length:(i + 1) * length] for i in range(math.ceil(len(txt) / length))]


def windowEnumerationHandler(hwnd, windows):
    windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def front(win_name):
    windows = []
    win32gui.EnumWindows(windowEnumerationHandler, windows)
    for i in windows:
        if i[1] == win_name:
            hantei = 0
            while (hantei is not True) and hantei < 100:
                try:
                    win32gui.ShowWindow(i[0], 5)
                    win32gui.SetForegroundWindow(i[0])
                    hantei = True
                except:
                    time.sleep(0.1)
                    hantei += 1
            break


def dict_window(text1_, text2_, position):
    un_focused_count = 0
    pygame.init()
    os.environ["SDL_VIDEO_WINDOW_POS"] = str(position[0] - 5) + ", " + str(position[1] - 5)
    pygame.display.set_caption("quick_dict")
    font = pygame.font.Font("font\SourceHanSansJP-Medium.otf", 20)
    text1 = font.render(text1_, True, (5, 5, 5))
    splitted = split_by_length(text2_, 20)
    text2 = []
    for i in splitted:
        text2.append(font.render(i, True, (5, 5, 5)))
    screen = pygame.display.set_mode((400, 75 + 30 * len(splitted)), pygame.NOFRAME)
    front("quick_dict")
    quited = None
    while quited is None:
        screen.fill((250, 250, 250))
        screen.fill((150, 150, 250), (0, 0, 400, 50))
        screen.blit(text1, (10, 10))
        for i, value in enumerate(text2):
            screen.blit(value, (10, 60 + 30 * i))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                quited = True
        try:
            if not pygame.mouse.get_focused():
                un_focused_count += 1
                time.sleep(0.1)

            else:
                un_focused_count = 0
        except:
            pass
        if un_focused_count >= 2:
            pygame.quit()
            quited = True
        if quited is None:
            pygame.display.update()


searchObj = Search()
while True:
    if keyboard.is_pressed("ctrl+c+shift"):
        clipboard = pyperclip.paste()
        print(clipboard)
        answer = searchObj.search(clipboard)
        dict_window(clipboard, answer, pyautogui.position())
    time.sleep(0.05)
