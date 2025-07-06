from fastapi import FastAPI, UploadFile, File, HTTPException, Request
import aiofiles
import openai
import uuid
import os
from pathlib import Path

app = FastAPI()

# Audio file validation
ALLOWED_AUDIO_TYPES = ['audio/mp3', 'audio/wav', 'audio/m4a', 'audio/ogg', 'audio/webm']
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB (Whisper limit)

@app.post("/api/upload-audio")
async def upload_audio(request: Request, file: UploadFile = File(...)):
    # Get user ID from cookie
    user_id = request.cookies.get("user_id", str(uuid.uuid4()))
    
    # Validate file size
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large. Maximum size is 25MB")
    
    # Save file temporarily
    file_id = str(uuid.uuid4())
    temp_path = f"temp/{file_id}_{file.filename}"
    
    os.makedirs("temp", exist_ok=True)
    
    async with aiofiles.open(temp_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Transcribe with OpenAI Whisper
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        with open(temp_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )
        
        # Clean up temp file
        os.remove(temp_path)
        
        return {
            "user_id": user_id,
            "file_id": file_id,
            "transcription": transcript.text,
            "language": transcript.language,
            "duration": transcript.duration
        }
    except Exception as e:
        # Clean up on error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(500, f"Transcription failed: {str(e)}")