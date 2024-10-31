#include "Display.h"

const int baking_time = 10000;
const int starButtonPin = 8;
const int buzzerPin = 3;
const int redLEDPin = 4;
const int greenLEDPin = 5;
void setup() {
  Serial.begin(9600);
  pinMode(starButtonPin, INPUT_PULLUP);
  pinMode(buzzerPin, OUTPUT);
  pinMode(redLEDPin, OUTPUT);
}

void bakeAPizza() {

  int remaining_seconds = baking_time/1000;
  Serial.println("Oven started");
  digitalWrite(redLEDPin, HIGH);
  while(remaining_seconds >= 0){
    Display.show(remaining_seconds);
    delay(1000);
    remaining_seconds -= 1;
  }
  Serial.println("Ready");
  digitalWrite(redLEDPin, LOW);
  ringBuzzer();
}

void ringBuzzer() {
  tone(buzzerPin, 1000);
  delay(500);
  noTone(buzzerPin);
  delay(200);
  tone(buzzerPin, 1000);
  delay(500);
  noTone(buzzerPin);
  delay(200);
  tone(buzzerPin, 1000); 
  delay(500);
  noTone(buzzerPin);
  delay(200);
}

void loop() {
  digitalWrite(greenLEDPin, HIGH);
  if(digitalRead(starButtonPin) == LOW){
    digitalWrite(greenLEDPin, LOW);
    bakeAPizza();
    delay(400);
  }
}
