#include <Servo.h>

#define TOP (6) // F
#define BOTTOM (5) // E

Servo top;
Servo bottom;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  top.attach(TOP);
  bottom.attach(BOTTOM);

  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(250);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);
}

int read_count = 0;
char cmd[2] = {0};
void loop() {

  while (Serial.available()) {
    
    uint8_t c = Serial.read();
    cmd[read_count] = c;

    if (read_count == 0) {
      cmd[0] -= 'A';
      
      if (cmd[0] == TOP || cmd[0] == BOTTOM) {
        read_count++;
      } else {
        read_count = cmd[0] = 0;
      }
    } else {
      break;
    }

    delay(2);
  }

  if (cmd[0] == TOP) {
//    analogWrite(TOP, cmd[1]);
    top.write(cmd[1]);
//    Serial.print("Top to ");
//    Serial.println(int(cmd[1]));
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(250);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  } else if (cmd[0] == BOTTOM) {
    bottom.write(cmd[1]);
//    Serial.print("Bottom to ");
//    Serial.println(int(cmd[1]));
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(250);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
//    analogWrite(BOTTOM, cmd[1]);
  } else {
    //Serial.println("Unknown command");
  }
  

  read_count = 0;
  cmd[0] = cmd[1] = 0;

}
