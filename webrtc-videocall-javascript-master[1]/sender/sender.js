const webSocket = new WebSocket("ws://127.0.0.1:3000");

webSocket.onmessage = (event) => {
    handleSignallingData(JSON.parse(event.data));
};

function handleSignallingData(data) {
    switch (data.type) {
        case "answer":
            peerConn.setRemoteDescription(new RTCSessionDescription(data.answer));
            break;
        case "candidate":
            peerConn.addIceCandidate(new RTCIceCandidate(data.candidate));
            break;
    }
}

let username;

function sendUsername() {
    username = document.getElementById("username-input").value;
    sendData({
        type: "store_user",
    });
}

function sendData(data) {
    data.username = username;
    webSocket.send(JSON.stringify(data));
}

let localStream;
let peerConn;

function startCall() {
    document.getElementById("video-call-div").style.display = "flex";

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

            let configuration = {
                iceServers: [
                    {
                        urls: [
                            "stun:stun.l.google.com:19302",
                            "stun:stun1.l.google.com:19302",
                            "stun:stun2.l.google.com:19302",
                        ],
                    },
                ],
            };

            peerConn = new RTCPeerConnection(configuration);
            localStream.getTracks().forEach((track) => {
                peerConn.addTrack(track, localStream);
            });

            peerConn.ontrack = (e) => {
                document.getElementById("remote-video").srcObject = e.streams[0];
            };

            peerConn.onicecandidate = (e) => {
                if (e.candidate == null) return;
                sendData({
                    type: "store_candidate",
                    candidate: e.candidate,
                });
            };

            createAndSendOffer();
        })
        .catch((error) => {
            console.error("Error accessing camera and microphone:", error);
        });
}

function createAndSendOffer() {
    peerConn.createOffer()
        .then((offer) => {
            return peerConn.setLocalDescription(offer);
        })
        .then(() => {
            sendData({
                type: "store_offer",
                offer: peerConn.localDescription,
            });
        })
        .catch((error) => {
            console.error("Error creating and sending offer:", error);
        });
}

let isAudio = true;
function muteAudio() {
    isAudio = !isAudio;
    localStream.getAudioTracks()[0].enabled = isAudio;
}

let isVideo = true;
function muteVideo() {
    isVideo = !isVideo;
    localStream.getVideoTracks()[0].enabled = isVideo;
}
