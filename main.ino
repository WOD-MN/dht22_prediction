#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // Read temperature and humidity from the sensor
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Create a JSON object with the data
  StaticJsonDocument<200> doc;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;

  // Convert the JSON object to a string and send it over the serial port
  String output;
  serializeJson(doc, output);
  Serial.println(output);

  delay(5000); // Wait 5 seconds before reading again
}
