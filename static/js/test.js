let a;
a = window.prompt("what is ur name");
document.getElementById("p1").textContent= a;
// secend way

let b;
document.getElementById("submit").onclick = function() {
    b = document.getElementById("put").value;
    document.getElementById("p1").textContent= b;
    console.log(b);
}
let x ="1a";
let y ="1a";
let z ="1a";

x=Number(x);
y=String(y);
z=Boolean(z);

console.log(x, typeof x)
console.log(y, typeof y)
console.log(z, typeof z)

let c= 1.5;
let d= 2;
let w;

w= Math.round(c); //w=1
w= Math.pow(c, d); //w=1.5^2 1.5 os 2
w= Math.sqrt(2); //w= jidr 2
w= Math.sin(2);
w= Math.cos(2);
w= Math.tan(2);
w= Math.log(2);
w= Math.abs(-2); //w=|-2|=2
w= Math.max(c, d);
w= Math.min(c, d);

let k = Math.random() // y3tik 3dd 3chwa2i bin 0 w 1
k= Math.floor(Math.random() * 10) + 1; // y3tik nimiro bin 1 w 10 bla fasila
const max = 50;
const min = 25;
k = Math.floor(Math.random() * (max - min)) + min; // y3tik nimiro bin max w min

if(k > 30){
    console.log("hi");
}
else{
    console.log("by");
}


let age=21;
let n= age > 28 ? 5 : 7; // if age>28  n=5 if not n=7
console.log('hhhh'+ n + 'go');

let r = "what's up";
r.charAt(0) // ywrilk 7rf lwl ta3 klma charAt(x) ywrilk 7rf li f mrtba hadk ex: r.charAt(5)= '
r.indexOf("'") // ywrlk nimiro ta3 chercher f klma ex: r.indexOf("t")= 4
r.length // ywrilk tol klma
w = r.startsWith("j") // ila r ybda bi j w = true ila mybdach w = false
w = r.endsWith("j")  // kima li 9blha bs77 ykhlas bhad 7rf
w = r.includes("j") // ila kan fiha j yrj3 true ila mkanch yrj3 false
r = r.replaceALL("li 7abt tbdlo" , "bwach rak 7ab tbdlo") 


const da = "hi bro"
let ro = da.slice(nimiro ta3 7rf li 7ab tbda bih , nimiro ta3 7rf li 7ab tkhlas bih bi)