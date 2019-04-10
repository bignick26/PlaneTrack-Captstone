//Nicholas Restivo

//Stepper: Black,Green,Red,Blue?? -> A+,A-,B+,B-
#define stp 2
#define dir 3
#define MS1 4
#define MS2 5
#define EN  6
//Pin 7 is Sleep

//Motor 2
#define stp2 8
#define dir2 9
#define MS12 10
#define MS22 11
#define EN2  12
//Pin 13 is Sleep2

//Declare variables for functions
char user_input;
int x;
int y;
int state,state2;

void setup() {
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(EN, OUTPUT);
  pinMode(stp2, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(MS12, OUTPUT);
  pinMode(MS22, OUTPUT);
  pinMode(EN2, OUTPUT);
  pinMode(13, INPUT);
  
  resetEDPins(); //Set step, direction, microstep and enable pins to default states
  Serial.begin(9600); //Open Serial connection for debugging
  Serial.println("Begin motor control");
  Serial.println();
  //Print function list for user selection
  Serial.println("Use WASD for control");
  Serial.println();
}

//Main loop
void loop() {
  while(Serial.available()){
      user_input = Serial.read(); //Read user input and trigger appropriate function
      digitalWrite(EN, LOW); //Pull enable pin low to allow motor control
      if (user_input =='w')
      {
         StepUp();
      }
      else if(user_input =='a')
      {
        StepLeft();
      }
      else if(user_input =='s')
      {
        StepDown();
      }
      else if(user_input =='d')
      {
        StepRight();
      }
      else if (user_input == '5')
      {
        ChangeDir();
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

//Default microstep mode function
void StepUp()
{
  digitalWrite(dir, HIGH); //Pull direction pin High to move "up"
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
void StepLeft()
{
  digitalWrite(dir2, LOW); 
  for(x= 1; x<100; x++)  //Loop the forward stepping enough times for motion to be visible
  {
    digitalWrite(stp2,HIGH); //Trigger one step forward
    delay(20);
    digitalWrite(stp2,LOW); //Pull step pin low so it can be triggered again
    delay(20);
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

void StepRight()
{
  digitalWrite(dir2, HIGH); 
  for(x= 1; x<100; x++)  //Loop the forward stepping enough times for motion to be visible
  {
    digitalWrite(stp2,HIGH); //Trigger one step forward
    delay(20);
    digitalWrite(stp2,LOW); //Pull step pin low so it can be triggered again
    delay(20);
  }
  Serial.println("Enter new option");
  Serial.println();
}

void ChangeDir() {
  
    state=digitalRead(dir);
    if(state == HIGH)
    {
      digitalWrite(dir, LOW);
    }
    else if(state ==LOW)
    {
      digitalWrite(dir,HIGH);
    }
    state2=digitalRead(dir2);
    if(state2 == HIGH)
    {
      digitalWrite(dir2, LOW);
    }
    else if(state2 ==LOW)
    {
      digitalWrite(dir2,HIGH);
    }
}

