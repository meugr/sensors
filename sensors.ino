#include <SoftwareSerial.h>
#include <BME280I2C.h>
#include <Wire.h>  //enable I2C

#define Z19_SERIAL_BAUD 9600
#define ESP_SERIAL_BAUD 115200
#define DEBUG_SERIAL_BAUD 115200

BME280I2C bme; // BME SDA -> A4, SCL -> A5
SoftwareSerial z19Serial(A0, A1); // Z19 A0 -> TX, A1 -> RX
SoftwareSerial espSerial(A2, A3); // ESP01 A2 -> TX, A3 -> RX

const int port = 5000;
const String host = "\"192.168.1.100\"";
bool needReset = false;

byte z19_cmd[9] = {0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79};
// byte z19_off_abc[9] = {0xFF,0x01,0x79,0x00,0x00,0x00,0x00,0x00,0x86};
unsigned char z19_response[9];

int redPin = 6;
int greenPin = 9;
int bluePin = 10;

void setup() {
  espSerial.begin(ESP_SERIAL_BAUD);
  z19Serial.begin(Z19_SERIAL_BAUD);
  Wire.begin();
  bme.begin();
  //z19Serial.write(z19_off_abc, 9); uncomment for disable autocalibrate

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  String res = "";
  res = getZ19Data();
  delay(1000);
  res += ";" + getBME280Data();
  sendData(res);
  
  if (needReset) {
    void(* reset) (void) = 0;
    reset();
  }
  delay(10000);
}

String getZ19Data() {
  z19Serial.write(z19_cmd, 9);
  memset(z19_response, 0, 9);
  z19Serial.readBytes(z19_response, 9);
  byte checksum = 0;
  for (int i = 1; i < 8; i++) checksum+=z19_response[i];
  checksum = 255 - checksum;
  checksum++;

  if (!(z19_response[0] == 0xFF && z19_response[1] == 0x86 && z19_response[8] == checksum) ) {
    needReset = true;
    return "Checksum error: " + String(checksum) + " / "+ String(z19_response[8]);
  }
  else {
    unsigned int z19_responseHigh = (unsigned int) z19_response[2];
    unsigned int z19_responseLow = (unsigned int) z19_response[3];
    unsigned int ppm = (256*z19_responseHigh) + z19_responseLow;

    return String(ppm);
  }
}

String getBME280Data() {
  float temp(NAN), hum(NAN), pres(NAN);
  
  BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
  BME280::PresUnit presUnit(BME280::PresUnit_torr);
  
  bme.read(pres, temp, hum, tempUnit, presUnit);
  
  String res =  String(temp) + ";" + String(hum) + ";" + String(pres);
  
  return res;
}

void sendData(String payload) {
  espSerial.println("AT+CIPSTART=\"TCP\"," + host + "," + String(port));
  delay(300);
  espSerial.println("AT+CIPSEND=" + String(payload.length()));
  delay(300);
  espSerial.println(payload);
}

void setColor(byte red, byte green, byte blue) {
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);

}
