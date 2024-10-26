function calculateTotal() {
    
    const productAmount = parseFloat(document.getElementById('amount').value) || 0;

    document.getElementById("total-amount").textContent = `INR ${productAmount.toFixed(2)}`;
}

function paymentProcess() {
    var totalAmount = document.getElementById("total-amount").textContent;

    var amount = parseFloat(totalAmount.replace("INR ", "")) * 100;

    var options = {
        "key": "rzp_test_RkrD1X74NWT4U5", 
        "amount": amount, 
        "currency": "INR",
        "name": "Vidya.ai",
        "description": "Donation Amount",
        "image": "logo.png",
        "handler": function (response) {
            savetoDB(response);
            $('#myModal').modal(); 
        },
        "prefill": {
            "name": "Mitesh Singh",
            "email": "miteshsingh957@gmail.com",
            "contact": "7420027576"
        },
        "notes": {
            "address": "note value"
        },
        "theme": {
            "color": "#9932CC"
        }
    };

    var propay = new Razorpay(options);
    propay.open();
}


function savetoDB(response) {
    
    console.log('Payment Response:', response);
}
