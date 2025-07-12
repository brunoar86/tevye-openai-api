from tevye_openai_api.app.main import app


def start():
    app.run(host='127.0.0.1', port='8080', debug=False)


if __name__ == '__main__':
    start()