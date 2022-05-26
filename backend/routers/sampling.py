from fastapi import APIRouter, Form, UploadFile

router = APIRouter()

@router.get('/sampling')
async def sampling():
    return {"status": 200}

@router.post('/sampling/waveform')
async def waveform(file: UploadFile = Form('')):
    print(file.filename)
    return {"status": 200}