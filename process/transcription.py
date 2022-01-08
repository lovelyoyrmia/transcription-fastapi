import speech_recognition, librosa, os
from pydub import AudioSegment

def divide(divider, audio=None):
	list_durations = []
	audio = librosa.get_duration(filename=audio)

	if audio_duration > 240:
		while audio_duration > 0:
			list_durations.append(audio_duration)
			audio_duration -= divider
		list_durations.append(0)
		list_durations.reverse()
	else:
		list_durations = [0, audio_duration]

	return list_durations

def remove_file(filename):
	if os.path.exists(filename):
		os.remove(filename)

def recognition(offset, duration, audio=None, language='en-US'):
	try:
		if '.mp3' in audio:
			sound = AudioSegement.from_mp3(audio)
			sound.export('audio.wav', format='wav')
		r = speech_recognition.Recognizer()
		if audio != None:
			audio_file = speech_recognition.AudioFile(audio)
			with audio_file as source:
				r.adjust_for_ambient_noise(source)
				audio = r.record(source, offset=offset, duration=duration)
				try:
					text = r.recognize_google(audio, language=language)
					return {'text': text, 'processed': True}
				except:
					return {'text': '...', 'processed': True}
	except Exception as e:
		return f'Error {e}'
