from flask import Flask


app = Flask(__name__)


@app.route('/hello')
def hello():
    return "Hello, world!"


@app.route('/info')
def info():
    return "This is an informational page."


@app.route('/calc/<number_one>/<number_two>') # тут можно подставить /<int:number_one>/<int:number_two> и проверка будет не нужна
def calc(number_one, number_two):
    try:
        num1 = int(number_one)
        num2 = int(number_two)
        return f"The sum of {num1} and {num2} is {num1 + num2}."
    except ValueError:
        return "Invalid input: please provide numbers.", 400

@app.route("/reverse/<line>")
def reverse(line):
    if line:
        return f"{line[::-1]}"
    else:
        return "The text must have at least 1 character."


@app.route("/user/<name>/<float:age>")
def user(name, age):
    if age >= 0:
        return f"Hello, {name}. You are {age} years old."
    else:
        return "The age must be greater than 0."


if __name__ == "__main__":
    app.run(debug=True)
