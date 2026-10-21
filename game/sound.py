import pygame
import numpy as np

class SoundManager:
    def __init__(self):
        self.enabled = True
        self.music_enabled = True
        self.sounds = {}
        self.bgm_tracks = {}
        self.current_bgm = None
        self.music_channel = None

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(22050, -16, 2, 512)
            pygame.mixer.set_num_channels(16)
            self.music_channel = pygame.mixer.Channel(0)
            self._generate_sounds()
            self._generate_bgm()
        except Exception as e:
            print("Audio init warning:", e)
            self.enabled = False

    def _generate_tone(self, freq, duration, wave_type='sine', sweep_to=None, volume=0.3):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        if n_samples <= 0:
            return None
        t = np.linspace(0, duration, n_samples, False)

        if sweep_to:
            freqs = np.linspace(freq, sweep_to, n_samples)
            phase = 2 * np.pi * np.cumsum(freqs) / sample_rate
        else:
            phase = 2 * np.pi * freq * t

        if wave_type == 'square':
            wave = np.sign(np.sin(phase))
        elif wave_type == 'sawtooth':
            wave = 2 * (t * freq - np.floor(0.5 + t * freq))
        elif wave_type == 'triangle':
            wave = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
        else:
            wave = np.sin(phase)

        envelope = np.exp(-3.2 * t / duration)
        audio = (wave * envelope * volume * 32767).astype(np.int16)
        stereo = np.column_stack((audio, audio))
        return pygame.sndarray.make_sound(stereo)

    def _generate_noise(self, duration, volume=0.25):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        noise = np.random.uniform(-1, 1, n_samples)
        envelope = np.exp(-4.5 * t / duration)
        audio = (noise * envelope * volume * 32767).astype(np.int16)
        stereo = np.column_stack((audio, audio))
        return pygame.sndarray.make_sound(stereo)

    def _generate_sounds(self):
        sample_rate = 22050
        self.sounds['jump'] = self._generate_tone(180, 0.16, 'sine', sweep_to=460, volume=0.28)
        self.sounds['pogo'] = self._generate_tone(320, 0.18, 'triangle', sweep_to=680, volume=0.35)
        self.sounds['attack'] = self._generate_noise(0.09, volume=0.28)
        self.sounds['hit'] = self._generate_tone(260, 0.12, 'square', sweep_to=70, volume=0.38)
        self.sounds['coin'] = self._generate_tone(987, 0.15, 'sine', sweep_to=1318, volume=0.28)
        self.sounds['chest'] = self._generate_tone(523, 0.25, 'triangle', sweep_to=1046, volume=0.35)
        self.sounds['hurt'] = self._generate_tone(160, 0.2, 'sawtooth', sweep_to=60, volume=0.38)
        self.sounds['death'] = self._generate_tone(320, 0.4, 'sawtooth', sweep_to=80, volume=0.42)
        self.sounds['victory'] = self._generate_tone(523, 0.35, 'triangle', sweep_to=784, volume=0.38)
        self.sounds['dash'] = self._generate_noise(0.14, volume=0.32)
        self.sounds['wall_slide'] = self._generate_noise(0.06, volume=0.14)
        self.sounds['potion'] = self._generate_tone(440, 0.22, 'sine', sweep_to=880, volume=0.35)
        self.sounds['break'] = self._generate_noise(0.18, volume=0.42)
        self.sounds['checkpoint'] = self._generate_tone(440, 0.3, 'sine', sweep_to=1174, volume=0.35)

        # Owl Hoot (warm natural double-hoot)
        t1 = np.linspace(0, 0.12, int(sample_rate * 0.12), False)
        h1 = 0.28 * np.sin(2 * np.pi * 440 * t1) * np.exp(-3 * t1 / 0.12)
        pause = np.zeros(int(sample_rate * 0.08))
        t2 = np.linspace(0, 0.22, int(sample_rate * 0.22), False)
        h2 = 0.32 * np.sin(2 * np.pi * 370 * t2) * np.exp(-3 * t2 / 0.22)
        hoot = np.concatenate([h1, pause, h2])
        audio_hoot = (hoot * 32767).astype(np.int16)
        stereo_hoot = np.column_stack((audio_hoot, audio_hoot))
        self.sounds['owl_hoot'] = pygame.sndarray.make_sound(stereo_hoot)

        # Boss Ground Slam Shockwave
        t_slam = np.linspace(0, 0.35, int(sample_rate * 0.35), False)
        freqs_slam = np.linspace(120, 35, len(t_slam))
        phase_slam = 2 * np.pi * np.cumsum(freqs_slam) / sample_rate
        slam = 0.45 * np.sign(np.sin(phase_slam)) * np.exp(-3.2 * t_slam / 0.35)
        audio_slam = (slam * 32767).astype(np.int16)
        self.sounds['boss_slam'] = pygame.sndarray.make_sound(np.column_stack((audio_slam, audio_slam)))

        # Boss Roar
        t_roar = np.linspace(0, 0.45, int(sample_rate * 0.45), False)
        noise_roar = np.random.uniform(-1, 1, len(t_roar))
        freqs_roar = np.linspace(80, 45, len(t_roar))
        sub_roar = np.sin(2 * np.pi * np.cumsum(freqs_roar) / sample_rate)
        roar = (0.35 * sub_roar + 0.25 * noise_roar) * np.exp(-2.2 * t_roar / 0.45)
        audio_roar = (roar * 32767).astype(np.int16)
        self.sounds['boss_roar'] = pygame.sndarray.make_sound(np.column_stack((audio_roar, audio_roar)))

    def _generate_bgm(self):
        sample_rate = 22050

        def make_bgm_track(melody_notes, bass_notes, bpm=130):
            beat_dur = 60 / bpm / 2
            n_notes = len(melody_notes)
            total_dur = n_notes * beat_dur
            total_samples = int(sample_rate * total_dur)
            audio = np.zeros(total_samples, dtype=np.float32)

            for i in range(n_notes):
                m_f = melody_notes[i]
                b_f = bass_notes[i % len(bass_notes)]
                st = int(i * beat_dur * sample_rate)
                en = int((i + 1) * beat_dur * sample_rate)
                t = np.linspace(0, beat_dur, en - st, False)

                # Melody
                if m_f > 0:
                    m_wave = 2 * np.abs(2 * (t * m_f - np.floor(t * m_f + 0.5))) - 1
                    m_env = np.exp(-2.6 * t / beat_dur)
                    audio[st:en] += m_wave * m_env * 0.12

                # Bass
                if b_f > 0:
                    b_wave = np.sign(np.sin(2 * np.pi * b_f * t))
                    b_env = np.exp(-3.0 * t / beat_dur)
                    audio[st:en] += b_wave * b_env * 0.08

                # Rhythm Snare/Hat
                if i % 2 == 1:
                    noise = np.random.uniform(-1, 1, en - st)
                    n_env = np.exp(-22 * t / beat_dur)
                    audio[st:en] += noise * n_env * 0.04

            max_val = np.max(np.abs(audio))
            if max_val > 0:
                audio = (audio / max_val) * 0.20

            audio_int16 = (audio * 32767).astype(np.int16)
            stereo = np.column_stack((audio_int16, audio_int16))
            return pygame.sndarray.make_sound(stereo)

        # 16-step Stage Theme (A Minor / C Major adventure)
        m_stage = [440, 523.2, 659.2, 523.2, 587.3, 440, 392, 440,
                   523.2, 659.2, 784, 659.2, 587.3, 523.2, 440, 440]
        b_stage = [110, 110, 130.8, 130.8, 146.8, 146.8, 110, 110]
        self.bgm_tracks['stage'] = make_bgm_track(m_stage, b_stage, bpm=130)

        # 16-step Boss Battle Theme (D Minor fast battle)
        m_boss = [293.7, 349.2, 293.7, 440, 415.3, 293.7, 349.2, 392,
                  440, 523.2, 440, 587.3, 523.2, 440, 349.2, 293.7]
        b_boss = [73.4, 73.4, 87.3, 87.3, 98.0, 98.0, 73.4, 73.4]
        self.bgm_tracks['boss'] = make_bgm_track(m_boss, b_boss, bpm=155)

    def play(self, name):
        if not self.enabled:
            return
        snd = self.sounds.get(name)
        if snd:
            snd.play()

    def play_bgm(self, track_name):
        if not self.enabled or not self.music_enabled or not self.music_channel:
            return
        if self.current_bgm == track_name and self.music_channel.get_busy():
            return
        track = self.bgm_tracks.get(track_name)
        if track:
            self.current_bgm = track_name
            self.music_channel.play(track, loops=-1)

    def stop_bgm(self):
        if self.music_channel:
            self.music_channel.stop()
        self.current_bgm = None

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_bgm()
        else:
            if self.current_bgm:
                track = self.bgm_tracks.get(self.current_bgm)
                if track and self.music_channel:
                    self.music_channel.play(track, loops=-1)

sound = SoundManager()
