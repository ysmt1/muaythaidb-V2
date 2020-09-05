// Animate values in cost summary table
function animateValue(id, start, end, duration, currency) {
    // assumes integer values for start and end
    const obj = document.getElementById(id);
    const range = end - start;
    // no timer shorter than 50ms (not really visible any way)
    const minTimer = 50;
    // calc step time to show all interediate values
    let stepTime = Math.abs(Math.floor(duration / range));
    // never go below minTimer
    stepTime = Math.max(stepTime, minTimer);
    // get current time and calculate desired end time
    const startTime = new Date().getTime();
    const endTime = startTime + duration;
    let timer;

    function run() {
        const now = new Date().getTime();
        const remaining = Math.max((endTime - now) / duration, 0);
        const value = Math.round(end - (remaining * range));
        obj.innerHTML = formatCurrency(value, currency);
        if (value == end) {
            clearInterval(timer);
        }
    }

    timer = setInterval(run, stepTime);
    run();
}

function formatCurrency(value, currency) {

    value = value.toFixed(2)

    switch (currency) {
        case 'THB':
            return "฿" + parseInt(value);
        case 'USD':
            return "$" + value;
        case 'EUR':
            return "€" + value;
        case 'JPY':
            return '¥' + value;
        case 'AUD':
            return '$' + value;
        case 'CAD':
            return '$' + value;
        case 'GBP':
            return '£' + value;
        default:
            return " " + value;
    }
}

// Clean user input and extract number and duration unit from length of trip
function cleanInput(input) {
    let cleanedStr = input.trim().replace(/ /g, "");
    let splitStr = cleanedStr.split(/(\D+)/);
    tripLenInt = parseInt(splitStr[0]);
    tripLenUnit = splitStr[1].replace("s", "");
}

// Update cell value in summary costs table
function updateCellValue(costType, value) {
    const id = costType + "Cell";
    const cell = document.getElementById(id);
    const currentVal = +cell.innerText.slice(1);
    animateValue(id, currentVal, value, 200, 'THB');
}

function convertCellValue(costType, value, currency) {
    const convertId = costType + "CellConvert";
    const convertCell = document.getElementById(convertId);
    const currentVal = +convertCell.textContent.slice(1);
    const convertedVal = parseInt(value * currencyObj.rates[currency]);
    animateValue(convertId, currentVal, convertedVal, 200, currency);
}

function getCurrencySelection() {
    const select = document.getElementById('currencySelect');
    return select.value;
}