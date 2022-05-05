var fetch = require('node-fetch');
var throttle = require('throttle-wait')["throttle"];

let requiredLetter = 5;
let numbersArray = [];
const testArray = [4,5,1,2];
const successMessage = "Good job!";

// Server is rate limiting me, so restart combinations from
// Where we left off. To start from 0, use [6,6,0,6]
let startI = 0;
let startJ = 0;
let startK = 6;
let startL = 4;



function getAllCombinationsLength4() {
  // NOTE: valid numbers arrays are 1-indexed
  const combinations = [];
  for (let i = startI; i >= 0; i--) {
    numbersArray.push(i+1);
    for (let j = startJ; j >= 0; j--) {
      numbersArray.push(j+1);
      for (let k = startK; k < 7; k++) {
        numbersArray.push(k+1);
        for (let l = startL; l >= 0; l--) {
          numbersArray.push(l+1);
          // we have a valid combination
          if (hasRequiredLetter(numbersArray)) {
            combinations.push(JSON.parse(JSON.stringify(numbersArray)));
          }
          // Reset numbers array for next iteration
          numbersArray.pop();
        }
        // Reset numbers array for next iteration
        numbersArray.pop();
      }
      // Reset numbers array for next iteration
      numbersArray.pop();
    }
    // Reset numbers array for next iteration
    numbersArray.pop();
  }
  console.log(combinations);
  return combinations;
}

function hasRequiredLetter(numbersArray) {
  return numbersArray.includes(requiredLetter);
}

function didFindWord(resData) {
  if (resData["message"] == successMessage) {
    return true;
  }
}

// Only use this message if a result has been found
function foundAllWords(resData) {
  return resData["victory"];
}

async function doFetch(numbersArray) {
  console.log("doing fetch", numbersArray);
  const body = `{\"numeric_word\":\"${numbersArray.join("")}\"}`
  const res = await fetch("https://buzz.pythonanywhere.com/word/", {
    "headers": {
      "accept": "application/json",
      "accept-language": "en-US,en;q=0.9",
      "content-type": "application/json",
      "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "\"macOS\"",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",
      "cookie": "csrftoken=91IoLhjxQk2hAG9KE5T5uTDGJo7Xyk5rav1LPYyT9SoNASAL58jNnpWvWK8sA3Na; sessionid=1qd8acmumrflfdlt3482hk3r84rtdod6",
      "Referer": "https://buzz.pythonanywhere.com/",
      "Referrer-Policy": "same-origin"
    },
    "body": body,
    "method": "POST"
  });
  const stringData = await res.text();
  // const stringData = "{\"message\":\"gofuckyourself\"}";
  console.log(stringData);
  const data = JSON.parse(stringData);
  if (didFindWord(data)) {
    console.log("\n");
    console.log("!!!FOUND A WORD!!!")
    console.log(data);
    console.log(numbersArray.join(""));
    console.log("victory? ", foundAllWords(data));
    console.log("\n");
  }
  
  return data;
}

// EAT YOUR HEART OUT IM USING GLOBALS
// the throttling lib doesn't allow accepting arguments, so use
// globals to keep track of which combination I'm currently trying
let currentComboIdx = 0;
let combinations = getAllCombinationsLength4();

async function doFetchCombinations() {
  console.log(currentComboIdx);
  // console.log(combinations);
  const numbersArray = combinations[currentComboIdx];
  const data = await doFetch(numbersArray);
  currentComboIdx++;
  return data;
}

const doFetchCombinationsThrottled = throttle(1000, doFetchCombinations, {max: 7*7*7*7}); // 5s

async function bruteForceAllCombinationsLength4() {
  for (let i = 0; i < combinations.length; i++) {
    await doFetchCombinationsThrottled();
  }
}

// // I ran this as the main function to get all the combinations of length 4
// bruteForceAllCombinationsLength4()
//   .catch(function (err) {
//       console.log(err);
//   })
//   .then(function (res) {
//     console.log(res);
//   });

const remainingWords = [
  [3, 6, 7, 5, 1, 6, 5, 7],
  [5, 6, 7, 5, 1],
  [4, 1, 3, 6, 7, 5, 1],
  [4, 5, 7, 5, 1],
  [5, 6, 7, 3, 1, 5],
  [4, 1, 3, 2, 5],
  [4, 5, 1, 2, 3, 7],
  [1, 5, 7, 3, 1, 5, 2, 5, 6, 7],
  [2, 5, 7, 5, 1],
  [5, 2, 4, 3, 1, 5],
  [4, 1, 5, 2, 3, 5, 1],
  [3, 6, 6, 5, 1],
  [3, 6, 7, 5, 1],
  [5, 2, 3, 6, 5, 2],
  [3, 6, 7, 5, 6, 7],
  [7, 3, 7, 7, 5, 6],
  [4, 3, 5, 1, 1, 5],
  [4, 5, 4, 4, 5, 1],
  [3, 6, 7, 5, 1, 3, 2],
  [7, 3, 2, 5, 1],
  [4, 1, 5, 2, 3, 5, 1, 5],
  [2, 5, 1, 3, 7],
  [1, 5, 4, 1, 3, 6, 7],
  [4, 5, 7, 3, 7, 5],
  [3, 6, 7, 5, 1, 4, 1, 5, 7],
  [4, 1, 3, 2, 5, 1],
  [7, 5, 1, 1, 3, 5, 1],
  [7, 1, 5, 6, 7],
  [3, 6, 7, 5, 1, 4, 1, 5, 7, 5, 1],
  [3, 6, 7, 5, 1, 6],
  [1, 5, 7, 3, 1, 5],
  [4, 5, 1, 7, 3, 6, 5, 6, 7],
  [4, 3, 4, 5, 1],
  [1, 3, 4, 4, 5, 1],
  [7, 5, 1, 1, 3],
  [4, 1, 5, 7, 5, 5, 6],
  [3, 1, 5, 6, 5],
  [1, 5, 6, 5, 5],
  [4, 5, 1, 3, 2, 5, 7, 5, 1],
  [2, 5, 7, 1, 5],
  [5, 2, 3, 6, 5, 6, 7],
  [5, 1, 6, 3, 5],
  [2, 3, 6, 5, 1],
  [4, 1, 3, 6, 7, 4, 1, 3, 6, 7, 5, 1],
  [5, 6, 7, 1, 5],
  [4, 5, 7, 3, 7],
  [3, 2, 2, 3, 6, 5, 6, 7],
  [3, 6, 7, 5, 1, 2, 3, 7, 7, 5, 6, 7],
  [7, 5, 2, 4, 5],
  [7, 5, 1, 1, 5],
  [7, 5, 2, 4, 5, 1],
  [2, 3, 6, 6, 3, 5],
  [1, 5, 6, 7, 5, 1],
  [2, 5, 1, 1, 3, 7, 7],
  [7, 1, 3, 2, 2, 5, 1],
  [6, 3, 6, 5, 7, 5, 5, 6],
  [5, 7, 3, 5, 6, 6, 5],
  [1, 3, 7, 7, 5, 1],
  [2, 5, 3, 5, 1],
  [4, 5, 4, 4, 5, 1, 2, 3, 6, 7],
  [4, 5, 1, 2, 3, 7, 7, 5, 5],
  [1, 5, 2, 3, 7]
];

let currentWordIdx = 0;
async function doFetchRemainingWords() {
  console.log(currentWordIdx);
  
  const numbersArray = remainingWords[currentWordIdx];
  const data = await doFetch(numbersArray);
  currentWordIdx++;
  return data;
}

const doFetchRemainingWordsThrottled = throttle(2 * 1000, doFetchRemainingWords, {max: 7*7*7*7}); // 5s

async function submitRemainingWords() {
  for (let i = 0; i < remainingWords.length; i++) {
    await doFetchRemainingWordsThrottled();
  }
}

submitRemainingWords()
  .catch(function (err) {
      console.log(err);
  })
  .then(function (res) {
    console.log(res);
  });
