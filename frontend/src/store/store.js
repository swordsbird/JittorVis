import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        APIBASE: BACKEND_BASE_URL,
        allData: {
            network: {},
            statistic: {
                // eslint-disable-next-line max-len
                'loss': [[0, 1.368281364440918], [1, 0.8863638043403625], [2, 0.6537527441978455], [3, 0.4862731695175171], [4, 0.35306838154792786], [5, 0.313691109418869], [6, 0.15771658718585968], [7, 0.0691552385687828], [8, 0.0762651339173317], [9, 0.04885830357670784], [10, 0.0025434272829443216], [11, 0.0010168652515858412], [12, 0.0007045376696623862], [13, 0.0005360112991183996], [14, 0.00042289754492230713], [15, 0.0003780520928557962], [16, 0.000339549413183704], [17, 0.0003006049373652786], [18, 0.00027838422101922333], [19, 0.0002583468740340322], [20, 0.00021273399761412293], [21, 0.0002297477622050792], [22, 0.00022036675363779068], [23, 0.00022349190840031952], [24, 0.00018359115347266197], [25, 0.00018663618538994342], [26, 0.00019405584316700697], [27, 0.00017161911819130182], [28, 0.00017248239601030946], [29, 0.00016303660231642425], [30, 0.00018204966909252107], [31, 0.00016800033336039633], [32, 0.0001636193337617442], [33, 0.00015419766714330763], [34, 0.00016525608953088522], [35, 0.00015187051030807197], [36, 0.00015311877359636128], [37, 0.00014568018377758563], [38, 0.00015231201541610062], [39, 0.00015871408686507493], [40, 0.00013939558994024992], [41, 0.0001387594238622114], [42, 0.0001429350086254999], [43, 0.00016300816787406802], [44, 0.00013680729898624122], [45, 0.00013435598521027714], [46, 0.00018662236107047647], [47, 0.00014486130385193974], [48, 0.00012893743405584246], [49, 0.00014028225268702954]],
                // eslint-disable-next-line max-len
                'accuracy': [[0, 0.45726755261421204], [1, 0.6428136229515076], [2, 0.7362971901893616], [3, 0.8121193647384644], [4, 0.8686560988426208], [5, 0.8884490728378296], [6, 0.9469143152236938], [7, 0.9762485027313232], [8, 0.9739139080047607], [9, 0.9846731424331665], [10, 0.9996954798698425], [11, 1], [12, 1], [13, 1], [14, 1], [15, 1], [16, 1], [17, 1], [18, 1], [19, 1], [20, 1], [21, 1], [22, 1], [23, 1], [24, 1], [25, 1], [26, 1], [27, 1], [28, 1], [29, 1], [30, 1], [31, 1], [32, 1], [33, 1], [34, 1], [35, 1], [36, 1], [37, 1], [38, 1], [39, 1], [40, 1], [41, 1], [42, 1], [43, 1], [44, 1], [45, 1], [46, 1], [47, 1], [48, 1], [49, 1]],
                // eslint-disable-next-line max-len
                'recall': [[0, 0.45726755261421204], [1, 0.6428136229515076], [2, 0.7362971901893616], [3, 0.8121193647384644], [4, 0.8686560988426208], [5, 0.8884490728378296], [6, 0.9469143152236938], [7, 0.9762485027313232], [8, 0.9739139080047607], [9, 0.9846731424331665], [10, 0.9996954798698425], [11, 1], [12, 1], [13, 1], [14, 1], [15, 1], [16, 1], [17, 1], [18, 1], [19, 1], [20, 1], [21, 1], [22, 1], [23, 1], [24, 1], [25, 1], [26, 1], [27, 1], [28, 1], [29, 1], [30, 1], [31, 1], [32, 1], [33, 1], [34, 1], [35, 1], [36, 1], [37, 1], [38, 1], [39, 1], [40, 1], [41, 1], [42, 1], [43, 1], [44, 1], [45, 1], [46, 1], [47, 1], [48, 1], [49, 1]],
            },
            confusionMatrix: {},
        },
        layoutInfo: {
            layoutNetwork: {}, // very similar to allData.network, with some attributes for layout added
            focusID: '_model/', // default focus node is root node
            t: -1, // a timestamp
        },
        featureMapNodeID: null, // which node to show feature map
        confusionCellID: null, // which cell clicked ({labels, preds})
    },
    mutations: {
        setAllData(state, allData) {
            state.allData.network = allData.network;
        },
        setLayoutInfo(state, layoutInfo) {
            state.layoutInfo = layoutInfo;
        },
        setFeatureMapNodeID(state, featureMapNodeID) {
            state.featureMapNodeID = featureMapNodeID;
        },
        setConfusionMatrix(state, confusionMatrix) {
            state.allData.confusionMatrix = confusionMatrix;
        },
        setConfusionCellID(state, confusionCellID) {
            state.confusionCellID = confusionCellID;
        },
    },
    getters: {
        network: (state) => state.allData.network,
        statistic: (state) => state.allData.statistic,
        featureMapNodeID: (state) => state.featureMapNodeID,
        confusionCellID: (state) => state.confusionCellID,
        layoutInfo: (state) => state.layoutInfo,
        confusionMatrix: (state) => state.allData.confusionMatrix,
        URL_GET_ALL_DATA: (state) => state.APIBASE + '/api/allData',
        URL_GET_CONFUSION_MATRIX: (state) => state.APIBASE + '/api/confusionMatrix',
        URL_GET_FEATURE_INFO: (state) => state.APIBASE + '/api/featureInfo',
        URL_GET_FEATURE: (state) => {
            return (leafID, index) => state.APIBASE + `/api/feature?leafID=${leafID}&index=${index}`;
        },
        URL_GET_IMAGES_IN_MATRIX_CELL: (state) => state.APIBASE+'/api/confusionMatrixCell',
        URL_GET_IMAGE_GRADIENT: (state) => {
            return (imageID, method) => state.APIBASE + `/api/imageGradient?imageID=${imageID}&method=${method}`;
        },
    },
});
