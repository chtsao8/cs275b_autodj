

from pydub import AudioSegment
import sys
import os
import librosa
import random

class Setlist():

    def __init__(self, playlist_dir):
        self.playlist_dir = playlist_dir
        self.song_play_length = 30  #  num sec
        self.crossfade_len = 3000 # milsec
    
    def create_setlist(self, output_filename, bpm_sort=False, key_sort=False):
        setlist_song_files = os.listdir(self.playlist_dir)
        
        if bpm_sort:
            setlist_song_files = sort_by_bpm(setlist_song_files)
        elif key_sort:
            setlist_song_files = sort_by_key(setlist_song_files)
        elif bpm_sort and key_sort:
            setlist_song_files = sort_by_bpm_key(setlist_song_files)
        else:
            random.shuffle(setlist_song_files)

        setlist_build = None
        print(setlist_song_files)
        for filename in setlist_song_files:
            song_audio = AudioSegment.from_mp3(os.path.join(self.playlist_dir, filename))
            
            # clip song length if long enough
            song_len = song_audio.duration_seconds
            if song_len > self.song_play_length:
                song_start = (song_len / 2- self.song_play_length / 2) * 1000 / 2
                song_end = (song_len / 2 + self.song_play_length / 2) * 1000 / 2
                print(song_len , song_start / 1000, song_end / 1000)
                # n / 2 +30 - 30
                song_audio_clip = song_audio[song_start: song_end] # grab clip from middle using self.song_play_length
            else:
                song_audio_clip = song_audio

            if setlist_build == None:
                setlist_build = song_audio_clip
            else:
                setlist_build = setlist_build.append(song_audio_clip, crossfade=self.crossfade_len)
        
        print(setlist_build.duration_seconds)
           
        setlist_build.export(output_filename + ".mp3", format="mp3")

    def sort_by_bpm(self, setlist_song_files, acending=True):
        song_bpms = {}
        for filename in setlist_song_files:
            f = os.path.join(self.playlist_dir, filename)
            y, sr = librosa.load(f)
            onset_env = librosa.onset.onset_strength(y, sr=sr)
            tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
            song_bpms[filename] = tempo
        return sorted(song_bpms.items(), key=lambda item: item[1])

    def sort_by_key(self, setlist_song_files, acending=True):
        
        song_keys = {}
        for filename in setlist_song_files:
            f = os.path.join(self.playlist_dir, filename)
            y, sr = librosa.load(f)
            onset_env = librosa.onset.onset_strength(y, sr=sr)
            tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
            song_bpms[filename] = tempo
        return sorted(song_bpms.items(), key=lambda item: item[1])

    def sort_by_bpm_key(self, setlist_song_files, acending=True):
        pass


if __name__ == "__main__":
    setlist = Setlist(sys.argv[1])
    setlist.create_setlist(sys.argv[2])

    