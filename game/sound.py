import pygame
import numpy as np

class SoundManager:
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(22050, -16, 2, 512)
            self._generate_sounds()
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

        # Decay envelope
        envelope = np.exp(-3 * t / duration)
        audio = (wave * envelope * volume * 32767).astype(np.int16)
        stereo = np.column_stack((audio, audio))
        return pygame.sndarray.make_sound(stereo)

    def _generate_noise(self, duration, volume=0.25):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        noise = np.random.uniform(-1, 1, n_samples)
        envelope = np.exp(-4 * t / duration)
        audio = (noise * envelope * volume * 32767).astype(np.int16)
        stereo = np.column_stack((audio, audio))
        return pygame.sndarray.make_sound(stereo)

    def _generate_sounds(self):
        self.sounds['jump'] = self._generate_tone(180, 0.16, 'sine', sweep_to=460, volume=0.3)
        self.sounds['pogo'] = self._generate_tone(320, 0.18, 'triangle', sweep_to=680, volume=0.35)
        self.sounds['attack'] = self._generate_noise(0.09, volume=0.3)
        self.sounds['hit'] = self._generate_tone(260, 0.12, 'square', sweep_to=70, volume=0.4)
        self.sounds['coin'] = self._generate_tone(987, 0.15, 'sine', sweep_to=1318, volume=0.3)
        self.sounds['chest'] = self._generate_tone(523, 0.25, 'triangle', sweep_to=1046, volume=0.35)
        self.sounds['hurt'] = self._generate_tone(160, 0.2, 'sawtooth', sweep_to=60, volume=0.4)
        self.sounds['death'] = self._generate_tone(320, 0.4, 'sawtooth', sweep_to=80, volume=0.45)
        self.sounds['victory'] = self._generate_tone(523, 0.35, 'triangle', sweep_to=784, volume=0.4)
        self.sounds['dash'] = self._generate_noise(0.14, volume=0.35)
        self.sounds['wall_slide'] = self._generate_noise(0.06, volume=0.15)
        self.sounds['potion'] = self._generate_tone(440, 0.22, 'sine', sweep_to=880, volume=0.35)
        self.sounds['break'] = self._generate_noise(0.18, volume=0.45)
        self.sounds['checkpoint'] = self._generate_tone(440, 0.3, 'sine', sweep_to=1174, volume=0.35)

    def play(self, name):
        if not self.enabled:
            return
        snd = self.sounds.get(name)
        if snd:
            snd.play()

sound = SoundManager()
