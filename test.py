import win32com.client

speaker = win32com.client.Dispatch('SAPI.SpVoice')

if __name__ == '__main__':
    while 1:
        print('enter word')
        s = input()
        speaker.Speak(s)