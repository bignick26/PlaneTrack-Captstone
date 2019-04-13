
//Nicholas Restivo
//https://learn.sparkfun.com/tutorials/easy-driver-hook-up-guide/all

//Stepper: Black,Green,Red,Blue?? -> A+,A-,B+,B-
#define stpX 12
#define dirX 13
#define MS1X 9
#define MS2X 11
#define ENX  10
#define SLPX 8
#define stpY 2
#define dirY 5
#define MS1Y 3
#define MS2Y 7
#define ENY  6
#define SLPY 4


//Declare variables for functions
char user_input;
int x = 0;

//Step Speed
unsigned long prevMillisX = 0;
unsigned long prevMillisY = 0;
unsigned long curMillisX;
unsigned long curMillisY;
int xStepDelay, yStepDelay;
int xState = LOW;
int yState = LOW;
int y = 0;
int inY = 0;

//Position
int currentPosX = 400; // ~800 is full circle on full step
int currentPosY = 0; //0 - 4500 = full circle on 1/8 step
float desPosX = 400;
float desPosY = 0;

int n;

String readStr;

void setup() {
  pinMode(stpX, OUTPUT);
  pinMode(dirX, OUTPUT);
  pinMode(MS1X, OUTPUT);
  pinMode(MS2X, OUTPUT);
  pinMode(ENX, OUTPUT);
  pinMode(SLPX, OUTPUT);
  digitalWrite(SLPX,LOW);
  pinMode(stpY, OUTPUT);
  pinMode(dirY, OUTPUT);
  pinMode(MS1Y, OUTPUT);
  pinMode(MS2Y, OUTPUT);
  pinMode(ENY, OUTPUT);
  pinMode(SLPY, OUTPUT);
  digitalWrite(SLPY,LOW);
  
  resetEDPins(); //Set step, direction, microstep and enable pins to default states
  Serial.begin(19200); //Open Serial connection for debugging
  Serial.println("Begin motor control");
  Serial.println();
  //Print function list for user selection
  Serial.println("Enter Yaw and Pitch coordinates bewteen 1-700 and 0-4500 respectively.");
  Serial.println("Format: 'Yaw,Pitch' - Example: 350,2250 ");
  Serial.println();
}

//Main loop
void loop() {

  //Timer for delays
  curMillisX = millis();
  curMillisY = millis();

  //Take Input
  while(Serial.available()){

    //Read user input and trigger appropriate function
    user_input = Serial.read();
    char c = user_input;
    readStr += c;
    delay(2);
  }

  //Can also call singular axis motion with one, but commas includes (Example: ,600 or 600,)
  if (readStr.length() > 0) {
    Serial.println(readStr);
    int commaInd = readStr.indexOf(',');
    desPosX = readStr.substring(0, commaInd).toInt(); // between 0 and 360
    desPosY = readStr.substring(commaInd+1).toInt(); // between 0 and 180
    pinMode(SLPX,INPUT);
    pinMode(SLPY,INPUT);
    desPosX = int((desPosX/360.0) * 800.0); //rounding?
    desPosY = int((desPosY/180.0) * 4500.0);
    Serial.println(desPosX);
    Serial.println(desPosY);
  }

  xStepDelay = 20;
  yStepDelay = 5; //smoothest at 20

  //Step until desPosY = currentPosY at yStepDelay rate
  digitalWrite(ENX, LOW); //Pull enable pin low to allow motor control
  if (desPosX > currentPosX && desPosX <800 && ((unsigned long)(curMillisX - prevMillisX) >= xStepDelay))
  {
    digitalWrite(dirX, HIGH); //Pull direction pin High to move "+ degrees"
    xState = !xState;
    digitalWrite(stpX,xState);
    currentPosX += 1;
    prevMillisX = curMillisX;
    Serial.println(currentPosX);
  }
  else if (desPosX < currentPosX && desPosX > 0 && ((unsigned long)(curMillisX - prevMillisX) >= xStepDelay)) {
    digitalWrite(dirX, LOW);
    xState = !xState;
    digitalWrite(stpX,xState);
    currentPosX -= 1;
    prevMillisX = curMillisX;
    Serial.println(currentPosX);
  }
  else if (desPosX == currentPosX) {
    digitalWrite(stpX, LOW);
    //digitalWrite(SLPX, LOW);
    readStr = "";
  }
  else if (desPosX == 1000) { //Sleep
    readStr = "";
    pinMode(SLPX, OUTPUT);
    digitalWrite(SLPX,LOW);
  }

  //Y!
  //Step until desPosY = currentPosY at yStepDelay rate
  digitalWrite(ENY, LOW); //Pull enable pin low to allow motor control
  if (desPosY > currentPosY && desPosY <8000 && ((unsigned long)(curMillisY - prevMillisY) >= yStepDelay))
  {
    digitalWrite(dirY, HIGH); //Pull direction pin High to move "+ degrees"
    yState = !yState;
    digitalWrite(stpY,yState);
    currentPosY += 1;
    prevMillisY = curMillisY;
    Serial.println(currentPosY);
  }
  else if (desPosY < currentPosY && desPosY > 0 && ((unsigned long)(curMillisY - prevMillisY) >= yStepDelay)) {
    digitalWrite(dirY, LOW);
    yState = !yState;
    digitalWrite(stpY,yState);
    currentPosY -= 1;
    prevMillisY = curMillisY;
    Serial.println(currentPosY);
  }
  else if (desPosY == currentPosY) {
    digitalWrite(stpY, LOW);
    //digitalWrite(SLPY, LOW);
    readStr = "";
  }
  else if (desPosY == 10000) { //Sleep
    readStr = "";
    pinMode(SLPY, OUTPUT);
    digitalWrite(SLPY,LOW);
    //if greater than 90, current pos = 180, else current pos = 0
    currentPosY = 0;
  }
}

//Reset Easy Driver pins to default states
void resetEDPins()
{
  digitalWrite(stpX, LOW);
  digitalWrite(dirX, LOW);
  digitalWrite(MS1X, LOW); //
  digitalWrite(MS2X, LOW); //
  digitalWrite(ENX, HIGH);
  digitalWrite(stpY, LOW);
  digitalWrite(dirY, LOW);
  digitalWrite(MS1Y, HIGH); //
  digitalWrite(MS2Y, HIGH); //
  digitalWrite(ENY, HIGH);

  // HIGH,HIGH = 1/8 step; LOW,HIGH = 1/4 step; HIGH,LOW = 1/2 step; LOW,LOW = full step (2 phase)
}
