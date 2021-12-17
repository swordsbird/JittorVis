from data.network import JittorNetworkProcessor
import copy
import os
import numpy as np
from PIL import Image
import math
from tempfile import NamedTemporaryFile
from data.feature_vis import FeatureVis

class DataCtrler(object):

    def __init__(self):
        super().__init__()
        self.networkRawdata = {}
        self.network = {}
        self.statistic = {}
        self.labels = None
        self.preds = None
        self.features = None
        self.trainImages = None
        self.featureVis = None

    def processNetworkData(self, network: dict) -> dict:
        processor = JittorNetworkProcessor()
        return processor.process(network)

    def processStatisticData(self, data):     
        return data

    def process(self, networkRawdata, statisticData, model, predictData = None, trainImages = None, modeltype='jittor', attrs = {}):
        """process raw data
        """        
        self.networkRawdata = networkRawdata
        self.network = self.processNetworkData(self.networkRawdata["node_data"])
        self.statistic = self.processStatisticData(statisticData)
        self.featureVis = FeatureVis(model)

        if predictData is not None:
            self.labels = predictData["labels"].tolist()
            self.preds = predictData["preds"].tolist()
            self.features = predictData["features"]
        self.trainImages = trainImages

    def getBranchTree(self) -> dict:
        """get tree of network
        """        
        branch = self.network["branch"]
        newBranch = copy.deepcopy(branch)
        for branchID, branchNode in newBranch.items():
            if type(branchNode["children"][0])==int:
                branchNode["children"]=[]
        return newBranch

    def getBranchNodeOutput(self, branchID: str) -> np.ndarray:
        """unserializae leaf data from str to numpy.ndarray

        Args:
            branchID (str): branch node id

        Returns:
            np.ndarray: branch node output
        """        
        # first, get output opr node
        def visitTree(root):
            outputnode = None
            for childID in root["children"]:
                if type(childID)==int:
                    if "data" in self.network["leaf"][childID]["attrs"]:
                        outputnode = self.network["leaf"][childID]
                else:
                    childOutput = visitTree(self.network["branch"][childID])
                    if childOutput:
                        outputnode = childOutput
            return outputnode
        outputnode = visitTree(self.network["branch"][branchID])
        if outputnode is None:
            return {
                "leafID": -1
            }
        # second, compute the data
        if type(outputnode["attrs"]["data"]) == str:
            shape = [int(num) for num in outputnode['attrs']['shape'][1:len(outputnode['attrs']['shape'])-2].split(',')]
            data = np.array([float(num) for num in outputnode['attrs']['data'].split(',')])
            data = data.reshape(tuple(shape))
            if int(outputnode["attrs"]["ndim"])>1:
                data = data[0]
                shape = shape[1:]
            outputnode["attrs"]["data"] = data
            outputnode["attrs"]["shape"] = shape

        # third, get all 
        if len(outputnode["attrs"]["shape"])==1:
            features = [self.getFeature(outputnode["id"], -1)]
            maxActivations = []
            minActivations = []
        else:
            features = [self.getFeature(outputnode["id"], featureIndex) for featureIndex in range(outputnode["attrs"]["shape"][0])]
            maxActivations = [float(np.max(feature)) for feature in features]
            minActivations = [float(np.min(feature)) for feature in features]

        return {
            "leafID": outputnode["id"],
            "shape": outputnode["attrs"]["shape"],
            "features": features,
            "maxActivations": maxActivations,
            "minActivations": minActivations
        }

    def getFeature(self, leafID, featureIndex: int) -> str:
        """get feature map of a opr node

        Args:
            leafID (int or str): opr node id
            featureIndex (int): feature map index, if -1, return whole feature

        Returns:
            list: feature map image path
        """
        # compute the data
        leafNode = self.network["leaf"][leafID]
        if type(leafNode["attrs"]["data"]) == str:
            shape = [int(num) for num in leafNode['attrs']['shape'][1:len(leafNode['attrs']['shape'])-2].split(',')]
            data = np.array([float(num) for num in leafNode['attrs']['data'].split(',')])
            data = data.reshape(tuple(shape))
            if int(leafNode["attrs"]["ndim"])>1:
                data = data[0]
                shape = shape[1:]
            leafNode["attrs"]["data"] = data
            leafNode["attrs"]["shape"] = shape

        # get feature
        feature = None
        if featureIndex==-1:
            feature = self.network["leaf"][leafID]["attrs"]["data"]
        else:
            feature = self.network["leaf"][leafID]["attrs"]["data"][featureIndex]
        if len(feature.shape)==1:
            width = math.ceil(np.sqrt(feature.shape[0]))
            if feature.shape[0] < width*width:
                zeroPad = np.zeros((width*width-feature.shape[0]))
                feature = np.concatenate((feature, zeroPad))
            feature = feature.reshape((width, width))
        
        return feature.tolist()

    def getStatisticData(self):
        """get statistic data
        """
        return self.statistic        

    def getConfusionMatrix(self):
        """ confusion matrix
        """        
        return self.statistic["confusion"]

    def getImagesInConsuionMatrixCell(self, labels: list, preds: list) -> list:
        """return images in a cell of confusionmatrix

        Args:
            labels (list): true labels of corresponding cell
            preds (list): predicted labels of corresponding cell

        Returns:
            list: images' id
        """ 
        # convert list of label names to dict
        labelNames = self.statistic['confusion']['names']
        name2idx = {}
        for i in range(len(labelNames)):
            name2idx[labelNames[i]]=i
        
        # find images
        labelSet = set()
        for label in labels:
            labelSet.add(name2idx[label])
        predSet = set()
        for label in preds:
            predSet.add(name2idx[label])
        imageids = []
        if self.labels is not None and self.preds is not None:
            n = len(self.labels)
            for i in range(n):
                if self.labels[i] in labelSet and self.preds[i] in predSet:
                    imageids.append(i)
                    
        # limit length of images
        return imageids[:50]
    
    def getImageGradient(self, imageID: int, method: str) -> list:
        """ get gradient of image

        Args:
            imageID (int): image id
            method (str): method for feature visualization

        Returns:
            list: gradient
        """        
        if self.trainImages is not None:
            image = self.trainImages[imageID]
            if method=='origin': return image.tolist()
            label = int(self.labels[imageID])
            grad = self.getFeatureVis(image, label, method)
            return grad.tolist()
        else:
            return []

    def getFeatureVis(self, inputImage, label, method="vanilla_bp"):
        """get feature visualization of an image

        Args:
            inputImage (numpy, (w,h,3)): RGB image
            label (int): true class label
            method (str): vanilla_bp, guided_bp, grad_cam, layer_cam, integrated_gradients, grad_times_image ...

        Returns:
            numpy (w, h, 3)
        """
        return self.featureVis.get_feature_vis(inputImage, label, method)


dataCtrler = DataCtrler()