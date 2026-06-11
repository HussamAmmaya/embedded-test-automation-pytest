void setup() {
  Serial.begin(9600);
}

void loop() {
  int valueA0 = analogRead(A0);
  int valueA1 = analogRead(A1);

  Serial.print("A0=");
  Serial.println(valueA0);

  Serial.print("A1=");
  Serial.println(valueA1);

  Serial.println("STATUS=OK");

  delay(1000);
}