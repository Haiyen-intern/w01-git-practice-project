from fastapi import FastAPI
app = FastAPI(title = "Books API")

@app.get("/")
def read_root():
    return {"message": "Hello World"}
