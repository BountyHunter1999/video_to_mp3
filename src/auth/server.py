import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL


server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

print(server.config)
print("We are working...")


@server.route("/")
def hello():
    return "<h1> Hello to my app </h1>"


@server.route("/login", methods=["POST"])
def login():
    # now in this route we need to provide a basic
    # authentication header that contains username and pw
    # request has access to that
    auth = request.authorization
    if not auth:
        return "Missing Credentials", 401

    # Check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email and auth.password !=password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401


def createJWT(username, secret, is_admin):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": is_admin
        },
        secret,
        algorithm="HS256",
    )


@server.route("/validate", methods=["POST"])
def validate():
    # the jwt token will be in Authorization headers
    encoded_jwt = request.headers['Authorization']

    if not encoded_jwt:
        return "Missing Credentials", 401

    # Bearer <token>
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "Not authorized", 403

    return decoded, 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)