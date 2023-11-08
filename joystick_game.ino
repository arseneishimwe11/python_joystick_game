// Pins for joystick X and Y axes and switch
const int switchPin = 7;
const int joystickXPin = A0;
const int joystickYPin = A1;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set the switch pin as input
  pinMode(switchPin, INPUT);
}

void loop() {
  // Read the state of the switch
  int switchState = digitalRead(switchPin);

  // Print the switch state on the serial monitor
  // Serial.print("Switch state: ");
  // Serial.println(switchState);

  // Read the analog input values from the joystick
  int xValue = analogRead(joystickXPin);
  int yValue = analogRead(joystickYPin);

  // Print the X and Y values on the serial monitor
  Serial.print(xValue);
  Serial.print(", ");
  Serial.print(yValue);
  Serial.println("");

  // Add a small delay if needed
  delay(50);
}
