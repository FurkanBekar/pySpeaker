import pyaudio
import wave
from pydub import AudioSegment
from pynput.keyboard import Listener
import optparse

log = 0
def banner():
    print("\n                      /$$$$$$                                /$$                                ")
    print("                     /$$__  $$                              | $$                                ")
    print("  /$$$$$$  /$$   /$$| $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$ | $$   /$$  /$$$$$$   /$$$$$$       ")
    print(" /$$__  $$| $$  | $$|  $$$$$$  /$$__  $$ /$$__  $$ |____  $$| $$  /$$/ /$$__  $$ /$$__  $$      ")
    print("| $$  \ $$| $$  | $$ \____  $$| $$  \ $$| $$$$$$$$  /$$$$$$$| $$$$$$/ | $$$$$$$$| $$  \__/      ")
    print("| $$  | $$| $$  | $$ /$$  \ $$| $$  | $$| $$_____/ /$$__  $$| $$_  $$ | $$_____/| $$            ")
    print("| $$$$$$$/|  $$$$$$$|  $$$$$$/| $$$$$$$/|  $$$$$$$|  $$$$$$$| $$ \  $$|  $$$$$$$| $$            ")
    print("| $$____/  \____  $$ \______/ | $$____/  \_______/ \_______/|__/  \__/ \_______/|__/            ")
    print("| $$       /$$  | $$          | $$                                                              ")
    print("| $$      |  $$$$$$/          | $$                                                              ")
    print("|__/       \______/           |__/")

    print("\n" + "*" * 92)
    print("\t\t  Author  : Furkan BEKAR\n\t\t  Version : 1.0\n\t\t  GitHub  : https://github.com/FurkanBekar")
    print("*" * 92)


def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-n","--name",dest="name",help="Enter the name of the voice to record.",nargs=1)
    parse_object.add_option("-c","--channel",dest="channel",help="Mono or stereo (1 or 2). Example: -c 1 and default value is 2",nargs=1)
    parse_object.add_option("-t","--time",dest="time",help="Enter the recording time. Default 0 and limitless record",nargs=1)
    parse_object.add_option("-i","--increase",dest="increase",help="Enter how many db the recording sound will be increased",nargs=1)
    parse_object.add_option("-d","--decrease",dest="decrease",help="Enter how many db the recording sound will be decreased",nargs=1)
    parse_object.add_option("-s","--sample",dest="sample",help="Samples per second. Default value is 44100",nargs=1)

    return parse_object.parse_args()

def volume_up_down(user_input):
    if user_input.increase != None:
        volume_up(user_input.name + ".wav", increase)
        print("[!] Volume " + increase +" db increased")
    elif user_input.decrease != None:
        volume_up(user_input.name + ".wav", decrease)
        print("[!] Volume " + decrease + " db decreased")
    else:
        exit()

def save_record(filename,stream,channels,FORMAT,p,sample_rate,frames):
    print("[!] Finished recording.")
    # the file name output you want to record into
    filename = filename + ".wav"
    # stop and close stream
    stream.stop_stream()
    stream.close()
    # terminate pyaudio object
    p.terminate()
    # save audio file
    # open the file in 'write bytes' mode
    wf = wave.open(filename, "wb")
    # set the channels
    wf.setnchannels(channels)
    # set the sample format
    wf.setsampwidth(p.get_sample_size(FORMAT))
    # set the sample rate
    wf.setframerate(sample_rate)
    # write the frames as bytes
    wf.writeframes(b"".join(frames))
    # close the file
    wf.close()

    volume_up_down(user_input)

def voice_record(filename,channels,record_seconds,sample_rate):

    # set the chunk size of 1024 samples
    chunk = 1024
    # sample format
    FORMAT = pyaudio.paInt16
    # initialize PyAudio object
    p = pyaudio.PyAudio()
    # open stream object as input & output
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []
    print("[!] Recording started")
    print("[!] Recording...")
    if record_seconds == 0:

        def on_press(key):
            global log
            log = int(key.char)
            print("[!] Recording stopped")
            if log == 1:
                exit(code=save_record(filename, stream, channels, FORMAT, p, sample_rate,frames))

        with Listener(on_press=on_press) as listener:
            while log != 1:
                data = stream.read(chunk)
                # stream.write(data)
                frames.append(data)
            listener.join()

    else:
        for i in range(int(sample_rate / chunk * record_seconds)):
            data = stream.read(chunk)
            # stream.write(data)
            frames.append(data)

        save_record(filename,stream,channels,FORMAT,p,sample_rate)


def volume_up(filename,db):
    audio_file = filename + ".wav"
    song = AudioSegment.from_wav(audio_file)
    # increae volume dB
    song_db_quieter = song + int(db)
    # save the output
    song_db_quieter.export(filename + "_higher.wav", "wav")

def volume_down(filename,db):
    audio_file = filename + ".wav"
    song = AudioSegment.from_wav(audio_file)
    # increae volume dB
    song_db_quieter = song - int(db)
    # save the output
    song_db_quieter.export(filename + "_lower.wav", "wav")

banner()

(user_input,arguments) = get_user_input()

if user_input.channel == None:
    channel = 2
else:
    channel = int(user_input.channel)

if user_input.sample == None:
    sample = 44100
else:
    sample = int(user_input.sample)

if user_input.increase != None:
    increase = int(user_input.increase)

if user_input.decrease != None:
    decrease = int(user_input.decrease)

if user_input.time == None:
    time = 0
else:
    time = int(user_input.time)

voice_record(user_input.name,channel,time,sample)









