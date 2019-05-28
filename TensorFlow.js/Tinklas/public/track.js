const video = document.getElementById("myvideo");
const canvas_small = document.getElementById("canvas_small");
const canvas_rez = document.getElementById("canvas_rez");

const context_small = canvas_small.getContext("2d");
const context_rez = canvas_rez.getContext("2d");


let trackButton = document.getElementById("trackbutton");
let updateNote = document.getElementById("updatenote");

let isVideo = false;
let model = null;

const modelParams = {
    flipHorizontal: true,
    maxNumBoxes: 20,
    iouThreshold: 0.5,
    scoreThreshold: 0.6, 
}

function startVideo() {
    handTrack.startVideo(video).then(function (status) {
        console.log("video started", status);
        if (status) {
            updateNote.innerText = "Video started. Now tracking"
            isVideo = true
            runDetection()
        } else {
            updateNote.innerText = "Please enable video"
        }
    });
}

// Stop/Start video
function toggleVideo() {
    if (!isVideo) {
        updateNote.innerText = "Starting video"
        startVideo();
    } else {
        updateNote.innerText = "Stopping video"
        handTrack.stopVideo(video)
        isVideo = false;
        updateNote.innerText = "Video stopped"
    }
}

function runDetection() {
    model.detect(video).then(predictions => {
        console.log("Predictions: ", predictions);
		model.renderPredictions_test(predictions, canvas_small, context_small, video, canvas_rez, context_rez);
        if (isVideo) {
            requestAnimationFrame(runDetection);
        }
    });
}

// Modelio įkelimas
handTrack.load(modelParams).then(lmodel => {
    model = lmodel
    updateNote.innerText = "Loaded Model!"
    trackButton.disabled = false
});
