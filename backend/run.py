from app import create_app

app = create_app()

if __name__ == '__main__':
    # El host 0.0.0.0 es necesario para que sea accesible desde Docker
    app.run(host='0.0.0.0', port=5001, debug=True)
