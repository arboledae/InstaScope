from flask import Flask, render_template, request
import json
import zipfile
import tempfile
import os

app = Flask(__name__)

def procesar_datos(followers_data, following_data):

    followers = set()
    following = set()


    for usuario in followers_data:

        try:
            username = usuario["string_list_data"][0]["value"]
            followers.add(username.strip().lower())

        except:
            pass

    try:
        following_list = following_data["relationships_following"]

    except:
        following_list = following_data

    for usuario in following_list:

        try:

       
            if "title" in usuario:

                username = usuario["title"]

      
            else:

                username = usuario["string_list_data"][0]["value"]

            following.add(username.strip().lower())

        except:
            pass


    no_te_siguen = sorted(following - followers)

    return followers, following, no_te_siguen


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        instagram_zip = request.files["instagram_zip"]

        with tempfile.TemporaryDirectory() as temp_dir:

            # guardar zip
            zip_path = os.path.join(temp_dir, "instagram.zip")

            instagram_zip.save(zip_path)

            # extraer zip
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            followers_path = None
            following_path = None

            # buscar archivos
            for root, dirs, files in os.walk(temp_dir):

                for file in files:

                    if file == "followers_1.json":
                        followers_path = os.path.join(root, file)

                    if file == "following.json":
                        following_path = os.path.join(root, file)

            # verificar
            if not followers_path or not following_path:

                return """
                <h1 style='color:white;background:black;padding:40px;font-family:Arial'>
                followers_1.json or following.json not found inside ZIP
                </h1>
                """

            # abrir jsons
            with open(followers_path, encoding="utf-8") as f:
                followers_data = json.load(f)

            with open(following_path, encoding="utf-8") as f:
                following_data = json.load(f)

            # procesar
            followers, following, no_te_siguen = procesar_datos(
                followers_data,
                following_data
            )

            # renderizar
            return render_template(
                "result.html",
                followers=len(followers),
                following=len(following),
                no_te_siguen=no_te_siguen
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)