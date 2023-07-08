from flask import Flask, request, Response, render_template_string
import os, requests

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

# allow requests to load cat pictures from local disk and remote servers
class LocalFileAdapter(requests.adapters.BaseAdapter):
    def send(self, req, **kwargs):
        response = requests.Response()
        try:
            response.status_code = 200
            response.raw = open(os.path.normpath(req.path_url), "rb")
        except Exception as e:
            response.status_code = 500
            response.reason = str(e)

        return response

# load a cat picture from local disk (file://) or a remote server (http://)
@app.route("/load")
def load():
    requests_session = requests.session()
    requests_session.mount(
        "file://", LocalFileAdapter()
    )  # enable file:// connection adapter
    try:
        resp = requests_session.get(request.args.get("image", ""))
    except Exception as e:
        resp = str(e)

    return Response(resp, mimetype="image/jpg")

# display my favourite cats in a grid
@app.route("/")
def index():

    cats = ["cat{}.jpg".format(i) for i in range(1, 10)]
    pwd = os.getcwd()
    debug = request.args.get("debug", "")

    template = (
        """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cat Grid</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='bootstrap.min.css') }}">
        <style>
            body, html {
                height: 100%;
                background-color: gray;
            }
            body {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .image-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
            }
            .image-item {
                width: 100%;
                height: 300px;
                border: 1px solid black;
            }
            .image-item img {
                object-fit: cover;
                width: 100%;
                height: 100%;
            }
        </style>
    </head>
    <body>
        <div class="container text-center mt-4">
            <h5>Displaying my favourite cats from {{ pwd }}</h5>
            <div class="image-grid">
                {% for cat in cats %}
                    <div class="image-item">
                        <img src="{{ url_for('load') }}?image=http://localhost:5000/static/images/{{ cat }}" class="img-fluid">
                    </div>
                {% endfor %}
                """ + debug + """
            </div>
        </div>
    </body>
    </html>
    """
    )

    return render_template_string(template, cats=cats, pwd=pwd, debug=debug)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
