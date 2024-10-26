const webSocket = new WebSocket("ws://127.0.0.1:3000");

webSocket.onmessage = (event) => {
    handleSignallingData(JSON.parse(event.data));
};

let localStream;
let peerConn;
let username;

function joinCall() {
    username = document.getElementById("username-input").value;

    document.getElementById("video-call-div").style.display = "flex";

    let configuration = {
        iceServers: [
            {
                urls: ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302", "stun:stun2.l.google.com:19302"],
            },
        ],
    };

    peerConn = new RTCPeerConnection(configuration);

    peerConn.onaddstream = (e) => {
        document.getElementById("remote-video").srcObject = e.stream;
    };

    peerConn.onicecandidate = (e) => {
        if (e.candidate == null) return;

        sendData({
            type: "send_candidate",
            candidate: e.candidate,
        });
    };

    navigator.mediaDevices
        .getUserMedia({
            video: {
                frameRate: 24,
                width: {
                    min: 480,
                    ideal: 720,
                    max: 1280,
                },
                aspectRatio: 1.33333,
            },
            audio: true,
        })
        .then((stream) => {
            localStream = stream;
            document.getElementById("local-video").srcObject = localStream;

            localStream.getTracks().forEach((track) => {
                peerConn.addTrack(track, localStream);
            });

            sendData({
                type: "join_call",
            });
        })
        .catch((error) => {
            console.error("Error accessing camera and microphone:", error);
        });
}

function handleSignallingData(data) {
    switch (data.type) {
        case "offer":
            peerConn.setRemoteDescription(new RTCSessionDescription(data.offer));
            createAndSendAnswer();
            break;
        case "candidate":
            peerConn.addIceCandidate(new RTCIceCandidate(data.candidate));
            break;
    }
}

function createAndSendAnswer() {
    peerConn.createAnswer()
        .then((answer) => {
            return peerConn.setLocalDescription(answer);
        })
        .then(() => {
            sendData({
                type: "send_answer",
                answer: peerConn.localDescription,
            });
        })
        .catch((error) => {
            console.error("Error creating and sending answer:", error);
        });
}

function sendData(data) {
    data.username = username;
    webSocket.send(JSON.stringify(data));
}

let isAudio = true;

function muteAudio() {
    isAudio = !isAudio;
    localStream.getAudioTracks().forEach((track) => {
        track.enabled = isAudio;
    });
}

let isVideo = true;

function muteVideo() {
    isVideo = !isVideo;
    localStream.getVideoTracks().forEach((track) => {
        track.enabled = isVideo;
    });
}
