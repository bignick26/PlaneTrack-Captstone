
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
int currentPosY = -1; //0 - 4500 = full circle on 1/8 step
float desPosX = 400;
float desPosY = 0;

//Ranging
float set90Y = 1169; //number of steps to reach 90 + 40 deg (up) = 130deg
int set180Y = 0; //180 degree position
char setLock;
bool enter = false; //user will enter at 90 and 180 degree

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

  //Print function list for user selection
  Serial.println("Enter Yaw and Pitch coordinates bewteen 1-360 and 1-180 respectively.");
  Serial.println("Format: 'Yaw,Pitch' - Example: 90,90n");
  Serial.println();
  Serial.println("Extra Commands: sleep, set90 (be careful)");
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
    readStr += user_input;
    delay(2);
    

    //CONTROL MOTOR tg ON YAW AND PITCH (180,0n)
    //Serial.println(readStr);    
    if (readStr.charAt(readStr.length()-1) == 'n') {
      //Serial.println(readStr.length());
      readStr = readStr.substring(0,readStr.length()-1);
      //Serial.println(readStr);
      int commaInd = readStr.indexOf(',');
      desPosX = readStr.substring(0, commaInd).toInt(); // between 0 and 360
      desPosY = readStr.substring(commaInd+1).toInt(); // between 0 and 180
  
      desPosX = int((desPosX/360.0) * 800.0); //rounding?
      desPosY = int(((desPosY+40.0)/(220.0)) * (set90Y*220.0/130.0)); //40deg offset?
  
      pinMode(SLPX,INPUT);
      pinMode(SLPY,INPUT);
      //Serial.println(desPosX);
      //Serial.println(desPosY);
      readStr = "";
      break;
    }

    //Extra Commands Cant have 'n'!!
    if(readStr == "set90") {
      setRange();
    }

    if(readStr == "sleep") {
      sleep();
    }
    
  }

  xStepDelay = 5;
  yStepDelay = 1; //smoothest at 20

  //Step until desPosX = currentPosX at xStepDelay rate
  digitalWrite(ENX, LOW); //Pull enable pin low to allow motor control
  if (desPosX > currentPosX && ((unsigned long)(curMillisX - prevMillisX) >= xStepDelay))
  {
    digitalWrite(dirX, LOW); //Pull direction pin Low to move "+ degrees"
    xState = !xState;
    digitalWrite(stpX,xState);
    if (xState == LOW)
      currentPosX += 1;
    prevMillisX = curMillisX;
  }
  else if (desPosX < currentPosX && ((unsigned long)(curMillisX - prevMillisX) >= xStepDelay)) {
    digitalWrite(dirX, HIGH);
    xState = !xState;
    digitalWrite(stpX,xState);
    if (xState == LOW)
      currentPosX -= 1;
    prevMillisX = curMillisX;
  }
  else if (desPosX == currentPosX) {
    digitalWrite(stpX, LOW);
    //digitalWrite(SLPX, LOW);
    readStr = "";
  }

  //Y!
  //Step until desPosY = currentPosY at yStepDelay rate
  digitalWrite(ENY, LOW); //Pull enable pin low to allow motor control
  if (desPosY > currentPosY && ((unsigned long)(curMillisY - prevMillisY) >= yStepDelay))
  {
    digitalWrite(dirY, HIGH); //Pull direction pin High to move "+ degrees"
    yState = !yState;
    digitalWrite(stpY,yState);
    if (yState == LOW)
      currentPosY += 1;
    prevMillisY = curMillisY;
  }
  else if (desPosY < currentPosY && ((unsigned long)(curMillisY - prevMillisY) >= yStepDelay)) {
    digitalWrite(dirY, LOW);
    yState = !yState;
    digitalWrite(stpY,yState);
    if (yState == LOW)
      currentPosY -= 1;
    prevMillisY = curMillisY;
  }
  else if (desPosY == currentPosY) {
    digitalWrite(stpY, LOW);
    //digitalWrite(SLPY, LOW);
    readStr = "";
  }
}

void sleep()
{
  sleepStep();
  pinMode(SLPX, OUTPUT);
  digitalWrite(SLPX,LOW);
  pinMode(SLPY, OUTPUT);
  digitalWrite(SLPY,LOW);
  currentPosY = 0;
}

void sleepStep()
{
  pinMode(SLPY,INPUT);
  digitalWrite(ENY,LOW);
  digitalWrite(dirY, LOW);
  pinMode(SLPX,INPUT);
  digitalWrite(ENX,LOW);
  
  while(currentPosY > 0) {
    digitalWrite(stpY,HIGH);
    delay(2);
    digitalWrite(stpY,LOW);
    currentPosY -= 1;
  }

  /*This isn't working!
  while(currentPosX != 180) {
    if (currentPosX > 180) {
      digitalWrite(dirX, HIGH);
      digitalWrite(stpX,HIGH);
      delay(5);
      digitalWrite(stpX,LOW);
      currentPosX -= 1;
    }
    else if (currentPosX < 180) {
      digitalWrite(dirX, LOW);
      digitalWrite(stpX,HIGH);
      delay(5);
      digitalWrite(stpX,LOW);
      currentPosX += 1;
    }
  }
  */
}

void setRange()
{
  delay(5000);
  pinMode(SLPY,INPUT);
  digitalWrite(ENY,LOW);
  digitalWrite(dirY, HIGH);
  Serial.println("Setting Range!");
  //Clear Buffer
  while(Serial.available())
    Serial.read();
        
  while(!enter) {
    digitalWrite(stpY,HIGH);
    delay(12);
    digitalWrite(stpY,LOW);
    currentPosY += 1;

    //Check if user pressed Enter
    if(Serial.available()){

      //Clear Buffer
      while(Serial.available())
        Serial.read();
        
      //Small Adjustments
      Serial.println("Set 90? Use 'w' and 's' to fine tune, 'y' to confirm!");
      fineTuneY();
            
      set90Y = currentPosY; //90 degree position = 1112
      Serial.println("90 Set! Value:");
      Serial.println(set90Y);
      Serial.println("Please enter this into the definitions in the Arduino Script");
      enter = true;
    }
  }
  
  //Clear Buffer
  while(Serial.available())
    Serial.read();
  delay(2000);
  
  //Set 180!
  /*
  while(!enter) {
    digitalWrite(stpY,HIGH);
    delay(12);
    digitalWrite(stpY,LOW);
    currentPosY += 1;

    //Check if user pressed Enter
    if(Serial.available()){

      //Clear Buffer
      while(Serial.available())
        Serial.read();
        
      //Small Adjustments
      Serial.println("Set 180?");
      fineTuneY();
            
      set180Y = currentPosY; //180 degree position
      Serial.println("180 Set! Value:");
      Serial.println(set180Y);
      enter = false;
    }
  }
  delay(2000);
  */
  //Go Home and Sleep
  sleepStep();
}

void fineTuneY() {
  //Adjust Around 90
  while (setLock != 'y') {
    
    if(Serial.available()) {
      setLock = Serial.read();

      if (setLock == 'w') {
        digitalWrite(dirY, HIGH);
        digitalWrite(stpY,HIGH);
        delay(12);
        digitalWrite(stpY,LOW);
        currentPosY += 1;
      }
      if (setLock == 's') {
        digitalWrite(dirY, LOW);
        digitalWrite(stpY,HIGH);
        delay(12);
        digitalWrite(stpY,LOW);
        currentPosY -= 1;
      }
      Serial.println(currentPosY);
      //Clear Buffer
      while(Serial.available())
        Serial.read();
    }
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
