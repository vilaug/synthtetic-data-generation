from pathlib import Path
from io import BytesIO
import sys
from flask import Flask, request, render_template, send_file
import zipfile
import os

src_dir = "/workdir"
sys.path.insert(1, src_dir)
sys.path.append(os.getcwd())

from src.server.generate import check_generate  # noqa: E402
from src.util.parser import Parser  # noqa: E402

app = Flask(__name__, template_folder='../../templates', static_folder='../../static')
app.secret_key = "don't tell anyone!!!"

configuration = Parser().parse_long_term_configuration(Path("configuration.yaml"))['flask']


@app.route("/")
def index():
    """
    Renders the index page.
    """
    return render_template('index.html')


@app.route('/download_images')
def download():
    """
    Downloads the contents of the output folder
    :return: sends a zip file to the user.
    """
    base_path = Path('./images/')
    data = BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='images.zip', cache_timeout=0)


@app.route("/generate", methods=['GET', 'POST'])
def generate():
    """
    Checks the generate behaviour

        if the request method is post
        checks the generation of the input form

        if the request method is get
        renders the generate template with the materials.
    """
    if request.method == 'POST':
        return check_generate(request.form, configuration)
    else:
        return render_template('generate.html', configuration=configuration)


if __name__ == "__main__":
    app.run(port=5000)
