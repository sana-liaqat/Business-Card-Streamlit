# ---------- Base Image ----------
    FROM python:3.10-slim

    # ---------- Environment ----------
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    ENV STREAMLIT_SERVER_PORT=8501
    ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
    
    # ---------- System Dependencies ----------
    RUN apt-get update && apt-get install -y \
        build-essential \
        curl \
        && rm -rf /var/lib/apt/lists/*
    
    # ---------- Working Directory ----------
    WORKDIR /app
    
    # ---------- Python Dependencies ----------
    COPY requirements.txt .
    
    RUN pip install --upgrade pip \
        && pip install --no-cache-dir -r requirements.txt
    
    # ---------- App Code ----------
    COPY . .
    
    # ---------- Expose Port ----------
    EXPOSE 8501
    
    # ---------- Run Streamlit ----------
    CMD ["streamlit", "run", "streamlit_app.py"]
    