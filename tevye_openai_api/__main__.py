import uvicorn
from tevye_openai_api.app.main import app


def start():
    uvicorn.run(app, host='127.0.0.1', port='8080', reload=True, debug=False)


if __name__ == '__main__':
    start()
