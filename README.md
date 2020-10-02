# fastapi-demo
Fastapi demo for fagfredag 

## Sette opp utviklingsmiljø
```conda env create -f win-environment.yml```

## Tren og lagre modell
```python app/model.py```

## Bygg docker-image
```docker build -t fastapi-demo .```

## Kjør

```docker run -p 5000:8080 --env-file .env fastapi-demo```
