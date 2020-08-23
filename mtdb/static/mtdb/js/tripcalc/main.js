const tripLength = document.getElementById("trainingLength");
const formInputs = document.querySelectorAll("#tripCalcForm input, #currencySelect");
const currencySelect = document.getElementById("currencySelect");
let validTrip = false;
let costDict = {};
let tripLenInt = 1;
let tripLenUnit;
const costMultiplier = {
    "day": 1,
    "week": 7,
    "month": 30,
    "year": 365
};

// Read in training prices from trip-costs.json file
function getCostsJSON(callback) {
    let request = new XMLHttpRequest();
    request.open("GET", "/static/mtdb/js/tripcalc/trip-costs.json", true);
    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            var data = JSON.parse(this.response);
            callback(data);
        } else {
            console.log("Unable to get json");
        }
    };
    request.onerror = function() {
        console.log("connection error");
    }
    request.send();
}

// callback function to return
function returnCosts(data) {
    costDict = data;
}

function calcTotal() {
    if (!validTrip) { 
        console.log("invalid length, cannot calc");
        return;
    }
    let allCostObj = {
        trainingCost: getTrainingCost(),
        livingCost: getLivingCost(),
        foodCost: getFoodCost(),
        transportCost: getTransportCost() + getMotoCost(),
        partyCost: getPartyCost(),
        miscCost: getMiscCost(),
        flightCost: getFlightCost(),
        totalCost: getTrainingCost() + getLivingCost() + getFoodCost() + getTransportCost()
            + getPartyCost() + getMotoCost() + getFlightCost() + getMiscCost()
    }
    const currency = getCurrencySelection();
    const chartData = Object.values(allCostObj);
    chartData.pop();

    // Iterate over object props and call function for each cost category
    for (const costType in allCostObj) {
        updateCellValue(costType, allCostObj[costType]);
        convertCellValue(costType, allCostObj[costType], currency);
    }
    
    updateChart(chartData);
}

formInputs.forEach(function(input) {
    input.addEventListener("change", function(e) {
        // Calculate total cost
        calcTotal();
    })
})

// Validate trip length field - will be used to calculate values
tripLength.addEventListener("input", function(e) {
    const durations = ["days", "day", "week", "weeks", "months", "month", "years", "year"];
    const re = /\d+\s*[A-Za-z]+/;
    let userInput = e.target.value;

    // Remove validation class if it already exists
    if (tripLength.classList.contains("is-valid")) { 
        tripLength.classList.remove("is-valid"); 
    } else if (tripLength.classList.contains("is-invalid")) {
        tripLength.classList.remove("is-invalid"); 
    }

    // Validate input of trip length
    validTrip = re.test(userInput) && durations.some(duration => userInput.includes(duration));
    if (validTrip) { 
        tripLength.classList.add("is-valid");
        cleanInput(userInput);
    } 
})

// Add invalid class if user types in invalid trip length
tripLength.addEventListener("change", function (e) {
    if (!tripLength.classList.contains("is-valid")) { tripLength.classList.add("is-invalid"); }
})

currencySelect.addEventListener("change", function(e) {
    const currencyDisplay = document.getElementById("selectedCurrency");
    if (currencyDisplay.textContent !== this.value) {
        currencyDisplay.textContent = this.value;
    }
})

getCostsJSON(returnCosts);
getCurrencyRates();
