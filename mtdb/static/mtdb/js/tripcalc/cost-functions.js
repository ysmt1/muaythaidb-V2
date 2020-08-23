// calculate training cost based on user input
function getTrainingCost() {
    let trainingCost = 0;
    const selectedVal = document.querySelector("input[name='trainingFreq']:checked");
    if (selectedVal) {
        const trainingVal = selectedVal.value;
        trainingCost = costDict.trainingCosts[trainingVal][tripLenUnit] * tripLenInt;
    }
    return trainingCost;
}

// calculate living cost based on user input
function getLivingCost() {
    let livingCost = 0;
    let accomLevel;
    const selectedVal = document.querySelector("input[id='livingRange']");
    if (selectedVal) {
        const livingVal = selectedVal.value;
        switch (livingVal) {
            case "0":
                accomLevel = "basic";
                break;
            case "1":
                accomLevel = "medium";
                break;
            case "2":
                accomLevel = "high"
                break;
        }
        livingCost = costDict.livingCosts[accomLevel][tripLenUnit] * tripLenInt;
    }
    return livingCost;
}

function getFoodCost() {
    let foodCost = 0;
    let foodPref;
    const selectedVal = document.querySelector("input[id='foodRange']");
    if (selectedVal) {
        const foodVal = selectedVal.value;
        switch (foodVal) {
            case "0":
                foodPref = "thai";
                break;
            case "1":
                foodPref = "mixed";
                break;
            case "2":
                foodPref = "western"
                break;
        }
        foodCost = costDict.foodCosts[foodPref] * tripLenInt * costMultiplier[tripLenUnit];
    }
    return foodCost;
}

function getTransportCost() {
    let transportCost = 0;
    let pubTransportUse;
    const selectedVal = document.querySelector("input[id='transportRange']");
    if (selectedVal) {
        const transportVal = selectedVal.value;
        switch (transportVal) {
            case "0":
                pubTransportUse = "seldom";
                break;
            case "1":
                pubTransportUse = "sometimes";
                break;
            case "2":
                pubTransportUse = "often"
                break;
        }
        transportCost = costDict.transportCosts.taxi[pubTransportUse] * tripLenInt * costMultiplier[tripLenUnit];
    }
    return transportCost;
}

function getPartyCost() {
    let partyCost = 0;
    let partyFreq;
    const selectedVal = document.querySelector("input[id='partyRange']");
    if (selectedVal) {
        const partyVal = selectedVal.value;
        switch (partyVal) {
            case "0":
                partyFreq = "no";
                break;
            case "1":
                partyFreq = "little";
                break;
            case "2":
                partyFreq = "yes"
                break;
        }
        partyCost = costDict.partyCosts[partyFreq] * tripLenInt * costMultiplier[tripLenUnit];
    }
    return partyCost;
}

function getMotoCost() {
    let motoCost = 0;
    const selectedVal = document.querySelector("input[name='motoRent']:checked");
    if (selectedVal) {
        const motoVal = selectedVal.value;
        if (motoVal === "yes") {
            motoCost = costDict.transportCosts.motorbike[tripLenUnit] * tripLenInt;
        }
    }
    return motoCost;
}

function getFlightCost() {
    let flightCost = 0;
    const selectedVal = document.querySelector("input[name='flightCost']:checked");
    if (selectedVal) {
        const flightVal = selectedVal.value;
        flightCost = costDict.flightCosts[flightVal];
    }
    return flightCost;
}

function getMiscCost() {
    let miscCost = 50 * tripLenInt * costMultiplier[tripLenUnit];
    return miscCost;
}