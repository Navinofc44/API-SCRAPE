FROM python:3.10

# FFmpeg install කිරීම (වීඩියෝ/ඕඩියෝ වැඩ වලට අනිවාර්යයි)
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

