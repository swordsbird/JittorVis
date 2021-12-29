#! /usr/bin/python3
import os
import pickle
import json
import argparse
import numpy as np
from data.jimm import resnet26
from flask import Flask, jsonify, request, send_file, render_template
from data.dataCtrler import dataCtrler
from flask_cors import CORS
import jittor as jt
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/allData', methods=['GET'])
def allData():
    alldata = {
        "network": dataCtrler.getBranchTree(),
        "statistic": dataCtrler.getStatisticData()
    }
    return jsonify(alldata)

@app.route('/api/networkOnImage', methods=["POST"])
def networkOnImage():
    imageID = request.json['imageID']
    return jsonify(dataCtrler.runImageOnModel(imageID))

@app.route('/api/featureInfo', methods=['POST'])
def featureInfo():
    branchID = request.json['branch']
    data = dataCtrler.getBranchNodeOutput(branchID)
    return jsonify(data)

@app.route('/api/feature', methods=["GET"])
def feature():
    leafID = int(request.args['leafID'])
    index = int(request.args['index'])
    return send_file(dataCtrler.getFeature(leafID, index))

@app.route('/api/confusionMatrix', methods=["POST"])
def confusionMatrix():
    return jsonify(dataCtrler.getConfusionMatrix())

@app.route('/api/confusionMatrixCell', methods=["POST"])
def confusionMatrixCell():
    labels = request.json['labels']
    preds = request.json['preds']
    return jsonify(dataCtrler.getImagesInConsuionMatrixCell(labels, preds))

@app.route('/api/imageGradient', methods=["GET"])
def imageGradient():
    imageID = int(request.args['imageID'])
    return jsonify(dataCtrler.getImageGradient(imageID))

@app.route('/api/grid', methods=["POST"])
def grid():
    nodes = request.json['nodes']
    constraints = None
    if 'constraints' in request.json:
        constraints = request.json['constraints']
    depth = request.json['depth']
    return jsonify(dataCtrler.gridZoomIn(nodes, constraints, depth))

@app.route('/api/findParent', methods=["POST"])
def findParent():
    children = request.json['children']
    parents = request.json['parents']
    return jsonify(dataCtrler.findGridParent(children, parents))

def main():
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument("--data_path", type=str, default='/data/zhaowei/jittor-data/')
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5005)
    args = parser.parse_args()
    if not os.path.exists(args.data_path):
        raise Exception("The path does not exist.")
    networkPath = os.path.join(args.data_path, "network.pkl")
    evaluationPath = os.path.join(args.data_path, "evaluation.json")

    predictPath = os.path.join(args.data_path, "predict_info.pkl")
    trainImagePath = os.path.join(args.data_path, "trainImages.npy")
    bufferPath = os.path.join(args.data_path, "buffer")
    modelPath = os.path.join(args.data_path, "resnet26.pkl")
    with open(predictPath, 'rb') as f:
        predictData = pickle.load(f)
    with open(networkPath, 'rb') as f:
        networkData = pickle.load(f)
    with open(evaluationPath, 'r') as f:
        statisticData = json.load(f)
    trainImages = np.load(trainImagePath)

    model = resnet26(pretrained=False, num_classes=100)
    model_dict_path = '/home/zhaowei/JittorModels/trained-models/restnet-14-0.98.pkl'
    model.load_state_dict(jt.load(model_dict_path))
    model.eval()
    sampling_buffer_path = os.path.join(bufferPath, "hierarchy.pkl")
    dataCtrler.process(networkData, statisticData, model = model, predictData = predictData, trainImages = trainImages, sampling_buffer_path = sampling_buffer_path)

    app.run(port=args.port, host=args.host, threaded=True, debug=False)

if __name__ == "__main__":
    main()