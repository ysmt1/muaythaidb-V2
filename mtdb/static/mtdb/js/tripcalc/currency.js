// set endpoint and your access key
// const baseCur = 'USD';
const app_id = 'c5dd7943f6cf4c3f8b06d171079f63a0';
const endpoint = 'https://openexchangerates.org/api/latest.json?app_id=' + app_id

let currencyObj;
let thaiBase;
const emptyObj = {
    rates: {
        "USD": 0,
        "THB": 1
    }
};
const curRequest = new XMLHttpRequest();

function getCurrencyRates() {
    curRequest.open('GET', endpoint, true);

    curRequest.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            // Success!
            var resp = this.response;

            try {
                currencyObj = JSON.parse(resp);
                thaiBase = currencyObj.rates["THB"];
                convertUsdToBaht(currencyObj.rates)
            } catch {
                console.log("An error has occured when parsing response from the exhange rates API");
                currencyObj = emptyObj;
            }
            populateCurrencyOptions(currencyObj);
        } else {
            console.log("An error has occured when calling the exhange rates API (unsuccessful status code)");
            currencyObj = emptyObj;
            populateCurrencyOptions(currencyObj);
        }
    };

    curRequest.onerror = function () {
        console.log("An error has occured when calling the exhange rates API");
        currencyObj = emptyObj;
        populateCurrencyOptions(currencyObj);
    };

    curRequest.send();
}

function populateCurrencyOptions(obj) {
    const select = document.getElementById('currencySelect');
    const sortedKeys = Object.keys(obj.rates).sort();

    sortedKeys.forEach(function(currency) {
        if (currency !== 'USD') {
            const option = document.createElement('option');
            option.value = currency;
            option.innerHTML = currency;
            select.add(option);
        }        
    })
}

function convertUsdToBaht(obj) {
    Object.keys(obj).forEach(function(key) {
        obj[key] = obj[key] / thaiBase;
    })
}