from flask_app import app
import os

def leavesOfPlants():
    total_plants = len(os.listdir(app.config['PLANTS_FOLDER']))
    files = []
    for k in range(0,total_plants):
        f = str(k+1)+'_'
        leavesFiles = [i for i in os.listdir(app.config['LEAVES_FOLDER']) if os.path.isfile(os.path.join(app.config['LEAVES_FOLDER'],i)) and f in i]
        files.append(leavesFiles)
    return files

def spotsOnLeaves():
    total_plants = len(os.listdir(app.config['PLANTS_FOLDER']))
    files = []
    for k in range(0,total_plants):
        f = str(k+1)+'_'
        leavesFiles = [i for i in os.listdir(app.config['SPOTS_FOLDER']) if os.path.isfile(os.path.join(app.config['SPOTS_FOLDER'],i)) and i.startswith(f)]
        files.append(leavesFiles)
    return files