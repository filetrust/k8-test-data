from src import create_app,db,app

if __name__ == "__main__":
    db=db
    print(db)
    app.run(debug=True, host="0.0.0.0", port="5000")  # nosec
