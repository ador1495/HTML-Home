const scriptTag = document.currentScript.dataset.t;
const label = document.querySelector(`.tl${scriptTag}`);
const input = document.querySelector(`.ti${scriptTag}`);
let st = 0, d = 0;
function requestSWTime() {
  return new Promise((resolve) => {
    // temporary listener for the reply
    function handleReply(event) {
      if (event.data.from === "dw") {
        window.removeEventListener("message", handleReply);
        resolve(event.data.value); // return [st, d]
      }
    }

    window.addEventListener("message", handleReply);

    // send request
    parent.postMessage({ from: "SWTime" }, "*");
  });
}
input.addEventListener('dblclick', async () => {
	const [st, d] = await requestSWTime();
	let dr = d, sst = st, mn = Math.floor(sst / 60) % 60, hr = Math.floor(sst / 3600);
	sst = prompt(`Type StartingTime of your study or keep it empty to set ${hr}:${mn}
	hh:mm convert to [ hh , mm ] at the end of the proccess`);
	dr = prompt(`Type Work Duration`, dr)
	let s1 = prompt(`Select Study type:
	0. cq(a & b)
	1. cq(c & d)
	2. mcq
	3. oneshot
	4. reading
	5. note`, "5")
	let s2 = prompt(`Select Subject:
	0. Bangla 
	1. English 
	2. ICT 
	3. Physics 
	4. Chemistry 
	5. Higher Math 
	6. Biology `, "5")
	let s3 = prompt("Type Chapter No. or keep it 0 if it's not spacified", "0")
	let p = prompt("How many items are done?", "1")
	input.value = `[${hr}, ${mn}, ${dr}, ${s1}, ${s2}, ${s3}, ${p}],`;
})
document.addEventListener("keydown", function(e){
	if (e.key == "Enter" && document.activeElement === input){
		navigator.clipboard.writeText(input.value); input.value = "";
	}
})

let topic = [
	["cq(a & b)", "cq(c & d)", "mcq", "oneshot", "reading", "note"],
	["bangla", "english", "ICT", "Physics", "Chemistry", "HigherMath", "Biology"],
	["Random", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
];
let topicColor = [];
let Eval = [];
let List = [];