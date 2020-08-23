// set endpoint and your access key
const endpoint = 'latest';
const baseCur = 'THB';
// const access_key = '661fe961cbcc8966f16ba4fb46c67922';
// let symbols = 'USD,THB,JPY,GBP,AUD,CAD';
let currencyObj;
const emptyObj = {
    rates: {
        "USD": 0,
        "THB": 1
    }
};
const curRequest = new XMLHttpRequest();

//Fixer.io
//curRequest.open('GET', 'http://data.fixer.io/api/' + endpoint + '?access_key=' + access_key + '&symbols=' + symbols, true);
//exchangeratesapi.io

function getCurrencyRates() {
    curRequest.open('GET', 'https://api.exchangeratesapi.io/' + endpoint + '?base=' + baseCur, true);

    curRequest.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            // Success!
            var resp = this.response;

            try {
                currencyObj = JSON.parse(resp);
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

