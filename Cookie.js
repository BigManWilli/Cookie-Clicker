let cookieCount = 0;
let clickValue = 1;
let img1;

function setup() {
  createCanvas(800, 600);
}

function preload() {
  img1 = loadImage("Billeder/cookie.jpg");
}

function draw() {
  background(255);
  
  // Draw cookie
  image(img1, width/2 - 100, height/2 - 200, 200, 400); // Adjusted image position
  
  // Display cookie count
  fill(0);
  textSize(24);
  text("Cookies: " + cookieCount, 90, 30);
}

function mouseClicked() {
  // Check if click is on cookie
  let cookieX = width/2 - 100;
  let cookieY = height/2 - 200;
  
  if (mouseX >= cookieX && mouseX <= cookieX + 200 && mouseY >= cookieY && mouseY <= cookieY + 400) {
    cookieCount += clickValue;
  }
}
