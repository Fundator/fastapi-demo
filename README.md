# fastapi-demo
Fastapi demo for fagfredag 


```conda env create -f win-environment.yml```

```docker build -t fastapi-demo .```

```python app/model.py```

```docker run -p 5000:8080 --env-file .env fastapi-demo```