from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True) #reinitialize web after changing the code automatically