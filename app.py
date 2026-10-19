"""Flask application for uploading an image and displaying its prediction."""

from flask import Flask, render_template, request

from model import predict_result, preprocess_img


app = Flask(__name__)


@app.route("/")
def main():
    """Display the image-upload home page."""
    return render_template("index.html")


@app.route("/prediction", methods=["POST"])
def predict_image_file():
    """Process an uploaded image and display its predicted digit."""
    try:
        image = preprocess_img(request.files["file"].stream)
        prediction = predict_result(image)
        return render_template(
            "result.html",
            predictions=str(prediction),
        )
    except (KeyError, TypeError, ValueError, OSError):
        error = "File cannot be processed."
        return render_template("result.html", err=error)


if __name__ == "__main__":
    app.run(port=9000, debug=True)
