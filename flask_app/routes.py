from flask_app import app
from flask import render_template, url_for, flash, request, redirect, Markup
from flask_app.forms import UploadForm
from flask_app.funtions import leavesOfPlants, spotsOnLeaves
import os
import pandas as pd

from object_detection import crop_image_detection_multi_images as CP
from object_detection import object_detection_images as Spot

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/upload", methods =['GET','POST'])
def upload():
    form = UploadForm()
    if form.image.data:
        uploaded_files = request.files.getlist("image")
        #image_data = request.files[form.image.name].read()
        for file in uploaded_files:
            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
                if os.path.isdir(os.path.join(app.config['PLANTS_FOLDER'])):
                	file.save(os.path.join(app.config['PLANTS_FOLDER'], file.filename))
                else:
                  os.mkdir(os.path.join(app.config['PLANTS_FOLDER']))
                  file.save(os.path.join(app.config['PLANTS_FOLDER'], file.filename))
            else:
                flash("File extension not allowed","danger")
                return redirect(url_for("upload"))

        total_files = len([name for name in os.listdir(app.config['PLANTS_FOLDER']) if os.path.isfile(os.path.join(app.config['PLANTS_FOLDER'], name))])
        i=1
        for name in os.listdir(app.config['PLANTS_FOLDER']):
            if(name.endswith("jpg")):
                os.rename(app.config['PLANTS_FOLDER']+"/"+name,app.config['PLANTS_FOLDER']+"/"+str(i)+".jpg")
                i+=1
        files = os.listdir(app.config['PLANTS_FOLDER'])
        #return render_template("plants.html",data=total_files,files=files)
        return redirect(url_for("plants"))
    return render_template("upload.html", title="Upload an image file. (*.jpg)", form=form)

@app.route("/plants")
def plants():
    total_files = len(os.listdir(app.config['PLANTS_FOLDER']))
    files = os.listdir(app.config['PLANTS_FOLDER'])
    return render_template("plants.html", data=total_files, files=files)



@app.route("/leaves",methods=['GET','POST'])
def leaves():
    if request.method == 'POST':
        CP.detect_and_crop()
        files = leavesOfPlants()
        plants = len(files)
        #total_files = len([name for name in os.listdir(app.config['LEAVES_FOLDER']) if os.path.isfile(os.path.join(app.config['LEAVES_FOLDER'], name))])
        return render_template("leaves.html", data=Markup(files),plants=plants)
    else:
        files = leavesOfPlants()
        plants = len(files)
        return render_template("leaves.html", data=Markup(files),plants=plants)


@app.route("/spots",methods=['GET','POST'])
def spots():
    if request.method == 'POST':
        Spot.detect_spots()
        files = spotsOnLeaves()
        plants = len(files)
        #total_files = len([name for name in os.listdir(app.config['LEAVES_FOLDER']) if os.path.isfile(os.path.join(app.config['LEAVES_FOLDER'], name))])
        return render_template("spots.html", data=Markup(files),plants=plants)
    else:
        files = spotsOnLeaves()
        plants = len(files)
        return render_template("spots.html", data=Markup(files),plants=plants)

@app.route("/stat")
def stat():
    data_dict = {}
    plant_values =[]
    leaves_values = []
    spots_values = []
    zeroSpot_values = []
    mean_values = []
    for plants in os.listdir(app.config["PLANTS_FOLDER"]):
        plant_values.append(plants)
        plant = plants.split(".",1)[0]
        total_leaves = len([name for name in os.listdir(app.config['LEAVES_FOLDER']) if
                           os.path.isfile(os.path.join(app.config['LEAVES_FOLDER'], name)) and name.startswith(plant)])
        leaves_values.append(total_leaves)

        spotFiles = [filename for filename in os.listdir(app.config['SPOTS_FOLDER']) if filename.startswith(plant)]

        addSpots =0
        zeroSpot =0
        for spots in spotFiles:
            tmp = spots.split(".")[0]
            tmp = tmp.split("_")[2]
            addSpots+=int(tmp)
            if int(tmp)==0:
                zeroSpot+=1
        spots_values.append(addSpots)
        zeroSpot_values.append(zeroSpot)
        mean_values.append(addSpots/(total_leaves-zeroSpot))

    data_dict["plants"] = plant_values
    data_dict["leaves"] = leaves_values
    data_dict["spots"] = spots_values
    data_dict["zeroSpots"] = zeroSpot_values
    data_dict["AVG"] = mean_values

    data = pd.DataFrame(data_dict)

    plants = []

    for i in range(0,len(plant_values)):
        plants.append("Plant "+str(i+1))

    return render_template("stat.html",plants=Markup(plants),spots=spots_values,serverity=mean_values,tables=[data.to_html(classes='table table-striped', header="true",border="0")], titles=data.columns.values)


@app.route("/visualize",methods=['GET'])
def visualize():
    plantImg = request.args["plantid"]
    plant = plantImg.split(".",1)[0]
    spotFiles = [filename for filename in os.listdir(app.config['SPOTS_FOLDER']) if filename.startswith(plant)]
    return render_template("visualize.html", plantImg=plantImg, spotFiles=spotFiles)


