import random
from textblob import TextBlob
import pretty_midi
import os
import subprocess
import time

class TextToMusicConverter:
    def __init__(self):
        # Enhanced emotion parameters for longer compositions
        self.emotion_params = {
            'happy': {
                'scale': [0, 2, 4, 5, 7, 9, 11],  # Major scale
                'tempo': random.randint(115, 125),
                'rhythm': 'allegro',
                'instrument': 0,  # Acoustic Grand Piano
                'octave': 4,
                'melody_length': 64,  # Double the notes
                'chord_length': 32,
                'progression': [[0,4,5,3], [0,5,3,4]]  # Multiple progression options
            },
            'sad': {
                'scale': [0, 2, 3, 5, 7, 8, 10],  # Minor scale
                'tempo': random.randint(55, 65),
                'rhythm': 'largo',
                'instrument': 48,  # String Ensemble 1
                'octave': 3,
                'melody_length': 48,
                'chord_length': 24,
                'progression': [[0,3,4,6], [0,5,3,6]]
            },
            'angry': {
                'scale': [0, 1, 3, 6, 7, 10],  # Dissonant scale
                'tempo': random.randint(135, 145),
                'rhythm': 'presto',
                'instrument': 30,  # Distortion Guitar
                'octave': 2,
                'melody_length': 72,
                'chord_length': 36,
                'progression': [[0,2,4,6], [0,3,6,2]]
            },
            'neutral': {
                'scale': [0, 2, 4, 5, 7, 9, 11],  # Major scale
                'tempo': random.randint(85, 95),
                'rhythm': 'moderato',
                'instrument': 73,  # Flute
                'octave': 4,
                'melody_length': 56,
                'chord_length': 28,
                'progression': [[0,3,4], [0,4,5]]
            }
        }
        
        # Soundfont (optional)
        self.soundfont = "soundfont.sf2"

    def analyze_text(self, text):
        """Analyze text sentiment and determine emotion"""
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.3:
            return 'happy'
        elif polarity < -0.3:
            return 'sad'
        elif abs(polarity) < 0.1:
            return 'neutral'
        else:
            return 'angry'

    def generate_melody(self, emotion, length=None, section_type="verse"):
        """Generate longer melodies with more variation"""
        params = self.emotion_params[emotion]
        if length is None:
            length = params['melody_length']
        
        midi = pretty_midi.PrettyMIDI(initial_tempo=params['tempo'])
        instrument = pretty_midi.Instrument(program=params['instrument'])
        
        current_time = 0
        phrase_length = 8  # Notes per musical phrase
        
        for i in range(length):
            # Change octave every phrase for variety
            if i % phrase_length == 0:
                current_octave = params['octave'] + random.choice([-1, 0, 0, 1])
                duration_multiplier = random.uniform(0.8, 1.5)
            
            # Create more interesting rhythms
            if section_type == "intro":
                note_duration = random.choice([0.5, 1.0]) * 1.5
            elif section_type == "chorus":
                note_duration = random.choice([0.25, 0.5]) * 0.8
            else:
                note_duration = random.choice([0.25, 0.5, 1.0]) * duration_multiplier
            
            note_pitch = random.choice(params['scale']) + current_octave * 12
            
            # Add occasional rests
            if random.random() < 0.1:  # 10% chance of rest
                current_time += note_duration
                continue
                
            note = pretty_midi.Note(
                velocity=random.randint(90, 110),
                pitch=note_pitch,
                start=current_time,
                end=current_time + note_duration)
            
            instrument.notes.append(note)
            current_time += note_duration
            
            # Occasionally add embellishments
            if random.random() < 0.15:  # 15% chance
                embellishment = pretty_midi.Note(
                    velocity=random.randint(80, 100),
                    pitch=note_pitch + random.choice([-2, -1, 1, 2]),
                    start=current_time - note_duration/2,
                    end=current_time)
                instrument.notes.append(embellishment)
        
        midi.instruments.append(instrument)
        return midi

    def generate_chords(self, emotion, length=None):
        """Generate longer chord progressions with variations"""
        params = self.emotion_params[emotion]
        if length is None:
            length = params['chord_length']
        
        midi = pretty_midi.PrettyMIDI(initial_tempo=params['tempo'])
        instrument = pretty_midi.Instrument(program=params['instrument'])
        
        current_time = 0
        progression = random.choice(params['progression'])
        
        for i in range(length):
            degree = progression[i % len(progression)]
            root = params['scale'][degree % len(params['scale'])] + (params['octave'] + 1) * 12
            third = params['scale'][(degree + 2) % len(params['scale'])] + (params['octave'] + 1) * 12
            fifth = params['scale'][(degree + 4) % len(params['scale'])] + (params['octave'] + 1) * 12
            
            # Vary chord durations
            chord_duration = 2.0 if i % 4 == 0 else 1.5
            
            for pitch in [root, third, fifth]:
                note = pretty_midi.Note(
                    velocity=100,
                    pitch=pitch,
                    start=current_time,
                    end=current_time + chord_duration)
                instrument.notes.append(note)
            
            current_time += chord_duration
            
            # Add occasional arpeggios
            if random.random() < 0.3:  # 30% chance
                for j, pitch in enumerate([root, third, fifth, third]):
                    arp_note = pretty_midi.Note(
                        velocity=90,
                        pitch=pitch,
                        start=current_time + j*0.1,
                        end=current_time + j*0.1 + 0.5)
                    instrument.notes.append(arp_note)
        
        midi.instruments.append(instrument)
        return midi

    def build_composition(self, emotion, text_length):
        """Create a complete musical structure"""
        # Determine length based on text
        if text_length < 10:  # Short text = 30 seconds
            melody_length = 48
            chord_length = 24
            sections = 1
        else:  # Longer text = 60 seconds
            melody_length = 96
            chord_length = 48
            sections = 2
        
        # Intro section
        midi = self.generate_melody(emotion, melody_length//3, "intro")
        intro_chords = self.generate_chords(emotion, chord_length//3)
        
        # Main sections
        for _ in range(sections):
            melody = self.generate_melody(emotion, melody_length)
            chords = self.generate_chords(emotion, chord_length)
            
            for instrument in chords.instruments:
                midi.instruments.append(instrument)
            for instrument in melody.instruments[1:]:  # Skip first instrument
                midi.instruments.append(instrument)
        
        return midi

    def save_midi(self, midi, filename):
        """Save MIDI to file"""
        midi.write(filename)

    def play_midi(self, midi):
        """Play MIDI using system default player"""
        try:
            temp_file = "temp_output.mid"
            self.save_midi(midi, temp_file)
            
            if os.name == 'nt':  # Windows
                os.startfile(temp_file)
            else:  # Mac/Linux
                subprocess.run(['open', temp_file], check=True)
        except Exception as e:
            print(f"Playback error: {e}")

    def text_to_music(self, text, output_file='output.mid', play=False):
        """Convert text to longer musical composition"""
        emotion = self.analyze_text(text)
        text_length = len(text.split())
        
        print(f"Creating {30 if text_length <10 else 60} second composition...")
        midi = self.build_composition(emotion, text_length)
        
        self.save_midi(midi, output_file)
        if play:
            self.play_midi(midi)
        return midi