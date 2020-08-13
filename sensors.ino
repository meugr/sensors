#include <SoftwareSerial.h>
#include <BME280I2C.h>
#include <Wire.h>  //enable I2C


#define SERIAL_BAUD 9600
#define Z19RX A0
#define Z19TX A1

BME280I2C bme; // BME SDA -> A4, SCL -> A5
SoftwareSerial z19Serial(Z19RX, Z19TX); // Z19 A0 -> TX, A1 -> RX

//const int port = 5000;
//const char* host = "\"192.168.1.100\"";

byte z19_cmd[9] = {0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79};
byte z19_off_abc[9] = {0xFF,0x01,0x79,0x00,0x00,0x00,0x00,0x00,0x86};
unsigned char z19_response[9];

void setup() {
  Serial.begin(115200);
  z19Serial.begin(SERIAL_BAUD);
  while(!Serial) {}
  Wire.begin();
  bme.begin();
  z19Serial.write(z19_off_abc, 9);
}

void loop() {
  String res = "";
  res = getBME280Data();
  delay(1000);
  res += ";" + getZ19Data();
  sendData(res);
  //Serial.println(res);
  delay(10000);
}

String getZ19Data()
{
  z19Serial.write(z19_cmd, 9);
  memset(z19_response, 0, 9);
  z19Serial.readBytes(z19_response, 9);
  byte crc = 0;
  for (int i = 1; i < 8; i++) crc+=z19_response[i];
  crc = 255 - crc;
  crc++;

  if (!(z19_response[0] == 0xFF && z19_response[1] == 0x86 && z19_response[8] == crc) ) {
    return "CRC error: " + String(crc) + " / "+ String(z19_response[8]);
  }
  else {
    unsigned int z19_responseHigh = (unsigned int) z19_response[2];
    unsigned int z19_responseLow = (unsigned int) z19_response[3];
    unsigned int ppm = (256*z19_responseHigh) + z19_responseLow;
  
    return String(ppm);
  }
}

String getBME280Data()
{
  float temp(NAN), hum(NAN), pres(NAN);
  
  BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
  BME280::PresUnit presUnit(BME280::PresUnit_Pa);
  
  bme.read(pres, temp, hum, tempUnit, presUnit);
  
  String res =  String(temp) + ";" + String(pres) + ";" + String(hum);
  
  return res;
}

void sendData(String payload) {
  Serial.println("AT+CIPSTART=\"TCP\",\"192.168.1.100\",5000");
  delay(1000);
  //char in = wifi.read();
  //Serial.println(in); 
  Serial.println("AT+CIPSEND=" + String(payload.length()));
  delay(1000);
  Serial.println(payload);
}
