import whisper

model = whisper.load_model('base')
result = model.transcribe('samples/allow.wav')
print(result)
