//Nicholas Restivo
//https://learn.sparkfun.com/tutorials/easy-driver-hook-up-guide/all

//Stepper: Black,Green,Red,Blue?? -> A+,A-,B+,B-
#define stp 2
#define dir 3
#define MS1 4
#define MS2 5
#define EN  6
//Pin 7 is Sleep


//Declare variables for functions
char user_input;
int x = 0;

//Step Speed
unsigned long prevMillisX = 0;
unsigned long prevMillisY = 0;
int xStepDelay;
int xStepDelay;

void setup() {
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(EN, OUTPUT);
  
  resetEDPins(); //Set step, direction, microstep and enable pins to default states
  Serial.begin(19200); //Open Serial connection for debugging
  Serial.println("Begin motor control");
  Serial.println();
  //Print function list for user selection
  Serial.println("Use WASD for control");
  Serial.println();
}

//Main loop
void loop() {

  //Timer for delays
  unsigned long curMillisX = millis(); //
  unsigned long curMillisY = millis(); //
  
  while(Serial.available()){
      user_input = Serial.read(); //Read user input and trigger appropriate function
      digitalWrite(EN, LOW); //Pull enable pin low to allow motor control
      if (user_input =='w')
      {
         StepUp();
      }
      else if(user_input =='s')
      {
        StepDown();
      }
      else if (user_input == '5')
      {
        SmallStepMode();
      }
      resetEDPins();
  }
}

//Reset Easy Driver pins to default states
void resetEDPins()
{
  digitalWrite(stp, LOW);
  digitalWrite(dir, LOW);
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(EN, HIGH);
}

void StepUp()
{
  digitalWrite(dir, HIGH); //Pull direction pin High to move "up"
  xStepDelay = 100;
  
  while(x<100) {
    if((unsigned long)(currentMillisX - previousMillisX) >= xStepDelay)) {
      
    }
  }

  
  Serial.println("Enter new option");
  Serial.println();
}

//Forward/reverse stepping function
void StepDown()
{
  digitalWrite(dir, LOW); //Pull direction pin Low to move "Down"
  for(x= 1; x<100; x++)  //Loop the forward stepping enough times for motion to be visible
  {
    digitalWrite(stp,HIGH); //Trigger one step forward
    delay(20);
    digitalWrite(stp,LOW); //Pull step pin low so it can be triggered again
    delay(20);
  }
  Serial.println("Enter new option");
  Serial.println();
}


// 1/8th microstep foward mode function
void SmallStepMode()
{
  digitalWrite(dir, LOW); //Pull direction pin low to move "forward"
  digitalWrite(MS1, HIGH); //Pull MS1, and MS2 high to set logic to 1/8th microstep resolution
  digitalWrite(MS2, HIGH);
  for(x= 1; x<8; x++)  //Loop the forward stepping enough times for motion to be visible
  {
    digitalWrite(stp,HIGH); //Trigger one step forward
    delay(1);
    digitalWrite(stp,LOW); //Pull step pin low so it can be triggered again
    delay(1);
  }
  Serial.println("Enter new option");
  Serial.println();
}
