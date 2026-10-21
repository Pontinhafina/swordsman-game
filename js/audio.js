// Pure Web Audio API Sound Generator - Zero external dependencies!
class SoundManager {
    constructor() {
        this.ctx = null;
        this.enabled = true;
        this.bgmPlaying = false;
        this.bgmTimer = null;
        this.masterVolume = 0.3;
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    playTone(freq, type, duration, startVol = 0.3, endVol = 0.001, pitchSweep = null) {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = type;
        osc.frequency.setValueAtTime(freq, now);
        if (pitchSweep) {
            osc.frequency.exponentialRampToValueAtTime(Math.max(10, pitchSweep), now + duration);
        }

        gain.gain.setValueAtTime(startVol * this.masterVolume, now);
        gain.gain.exponentialRampToValueAtTime(endVol, now + duration);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + duration);
    }

    playNoise(duration, startVol = 0.3, endVol = 0.001, isLowPass = false, cutoff = 1000) {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const bufferSize = this.ctx.sampleRate * duration;
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }

        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(startVol * this.masterVolume, now);
        gain.gain.exponentialRampToValueAtTime(endVol, now + duration);

        if (isLowPass) {
            const filter = this.ctx.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(cutoff, now);
            filter.frequency.linearRampToValueAtTime(100, now + duration);
            noise.connect(filter);
            filter.connect(gain);
        } else {
            noise.connect(gain);
        }

        gain.connect(this.ctx.destination);
        noise.start(now);
        noise.stop(now + duration);
    }

    playJump() {
        this.playTone(160, 'sine', 0.18, 0.4, 0.01, 480);
    }

    playAttack() {
        // Sword swing whoosh
        this.playNoise(0.12, 0.35, 0.01, true, 2200);
        this.playTone(400, 'triangle', 0.08, 0.2, 0.01, 150);
    }

    playHit() {
        // Impact punch
        this.playTone(280, 'square', 0.12, 0.4, 0.01, 60);
        this.playNoise(0.08, 0.3, 0.01, true, 800);
    }

    playCoin() {
        this.init();
        if (!this.enabled || !this.ctx) return;
        const now = this.ctx.currentTime;
        
        // Crisp dual chime (B5 -> E6)
        const t1 = this.ctx.createOscillator();
        const t2 = this.ctx.createOscillator();
        const g1 = this.ctx.createGain();
        const g2 = this.ctx.createGain();

        t1.type = 'sine';
        t2.type = 'sine';

        t1.frequency.setValueAtTime(987.77, now); // B5
        g1.gain.setValueAtTime(0.3 * this.masterVolume, now);
        g1.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

        t2.frequency.setValueAtTime(1318.51, now + 0.08); // E6
        g2.gain.setValueAtTime(0.001, now);
        g2.gain.setValueAtTime(0.35 * this.masterVolume, now + 0.08);
        g2.gain.exponentialRampToValueAtTime(0.001, now + 0.3);

        t1.connect(g1); g1.connect(this.ctx.destination);
        t2.connect(g2); g2.connect(this.ctx.destination);

        t1.start(now); t1.stop(now + 0.12);
        t2.start(now + 0.08); t2.stop(now + 0.3);
    }

    playChest() {
        this.init();
        if (!this.enabled || !this.ctx) return;
        const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
        notes.forEach((freq, idx) => {
            setTimeout(() => {
                this.playTone(freq, 'triangle', 0.22, 0.3, 0.01);
            }, idx * 70);
        });
    }

    playHurt() {
        this.playTone(180, 'sawtooth', 0.2, 0.4, 0.01, 70);
        this.playNoise(0.15, 0.3, 0.01, true, 600);
    }

    playEnemyDeath() {
        this.playTone(150, 'square', 0.25, 0.35, 0.01, 40);
        this.playNoise(0.2, 0.25, 0.01, true, 500);
    }

    playPlayerDeath() {
        const notes = [392.00, 349.23, 311.13, 261.63]; // G4, F4, Eb4, C4
        notes.forEach((freq, idx) => {
            setTimeout(() => {
                this.playTone(freq, 'sawtooth', 0.35, 0.35, 0.01);
            }, idx * 160);
        });
    }

    playVictory() {
        const notes = [
            { f: 523.25, d: 0.12 }, // C5
            { f: 659.25, d: 0.12 }, // E5
            { f: 783.99, d: 0.12 }, // G5
            { f: 1046.50, d: 0.35 }  // C6
        ];
        let delay = 0;
        notes.forEach(n => {
            setTimeout(() => {
                this.playTone(n.f, 'triangle', n.d, 0.4, 0.01);
            }, delay);
            delay += 140;
        });
    }

    startBgm() {
        if (this.bgmPlaying || !this.enabled) return;
        this.init();
        this.bgmPlaying = true;

        // Retro chiptune melody & bass progression
        const melody = [
            // Note frequencies (Hz), duration (ms)
            { f: 329.63, d: 180 }, // E4
            { f: 392.00, d: 180 }, // G4
            { f: 493.88, d: 180 }, // B4
            { f: 440.00, d: 180 }, // A4
            { f: 392.00, d: 180 }, // G4
            { f: 329.63, d: 180 }, // E4
            { f: 293.66, d: 180 }, // D4
            { f: 329.63, d: 360 }, // E4
            
            { f: 392.00, d: 180 }, // G4
            { f: 440.00, d: 180 }, // A4
            { f: 493.88, d: 180 }, // B4
            { f: 587.33, d: 180 }, // D5
            { f: 493.88, d: 180 }, // B4
            { f: 440.00, d: 180 }, // A4
            { f: 392.00, d: 360 }  // G4
        ];

        let step = 0;
        const tick = () => {
            if (!this.bgmPlaying) return;
            const item = melody[step % melody.length];
            // Play melody note quietly
            this.playTone(item.f, 'square', item.d / 1000 * 0.8, 0.07, 0.005);

            // Play bass note on every other beat
            if (step % 2 === 0) {
                const bassFreq = item.f / 4;
                this.playTone(bassFreq, 'triangle', item.d / 1000 * 1.5, 0.12, 0.01);
            }

            step++;
            this.bgmTimer = setTimeout(tick, item.d);
        };
        tick();
    }

    stopBgm() {
        this.bgmPlaying = false;
        if (this.bgmTimer) {
            clearTimeout(this.bgmTimer);
            this.bgmTimer = null;
        }
    }

    toggleBgm() {
        if (this.bgmPlaying) {
            this.stopBgm();
        } else {
            this.startBgm();
        }
        return this.bgmPlaying;
    }
}

window.sound = new SoundManager();
