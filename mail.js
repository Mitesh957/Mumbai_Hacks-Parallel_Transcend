
const firebaseConfig = {
    apiKey: "AIzaSyCqTWhstnYIMAWxFKlFmhqV5kXfDsMwm7Q",
    authDomain: "work-vibe.firebaseapp.com",
    projectId: "work-vibe",
    storageBucket: "work-vibe.appspot.com",
    messagingSenderId: "657553447517",
    appId: "1:657553447517:web:b31d13b5e033c32d7a8bb4",
    measurementId: "G-HEN3V080PD",
    databaseURL: "https://work-vibe-default-rtdb.firebaseio.com/" 
};


firebase.initializeApp(firebaseConfig);


const contactFormDB = firebase.database().ref("contactForm");


function submitForm(e) {
    e.preventDefault();
    console.log("submitted");
    const name = getElementVal("name");
    const emailid = getElementVal("emailid");
    const msgContent = getElementVal("msgContent");

    saveMessages(name, emailid, msgContent);

 
    document.querySelector(".alert").style.display = "block";

    
    setTimeout(() => {
        document.querySelector(".alert").style.display = "none";
    }, 3000);

   
    document.getElementById("contactForm").reset();
}


const saveMessages = (name, emailid, msgContent) => {
    const newContactForm = contactFormDB.push();

    newContactForm.set({
        name: name,
        emailid: emailid,
        msgContent: msgContent,
    });
};


const getElementVal = (id) => {
    return document.getElementById(id).value;
};


document.getElementById("contactForm").addEventListener("submit", submitForm);