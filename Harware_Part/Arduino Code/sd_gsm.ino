#include <SoftwareSerial.h>
#include <SD.h>
#include <SPI.h>
SoftwareSerial mySerial(3, 2); //SIM800L Tx & Rx is connected to Arduino #3 & #2
int meter_count = 0, count = 0, relay=10, pre_kwh, new_kwh;
bool state = 0, lastState = 0;
float kwh = 0.00;
File myFile;

void setup()
{
  pinMode(relay, OUTPUT);
  pinMode(A0, INPUT);
  Serial.begin(9600);
  mySerial.begin(9600);
  Serial.println("Initializing GSM...");
  mySerial.println("AT"); //Once the handshake test is successful, it will back to OK
  updateSerial();
  delay(1000);
  
  if (!SD.begin(4))
  {
    error_msg();
    Serial.println("Initialization failed!");
    return;
  }
  Serial.println("Memory Initialization Done !");
  readCount();
  readKWH();
  Serial.println("Previous Count = ");
  Serial.println(count);
  Serial.println("Previous  kWh  = ");
  Serial.println(kwh);
  pre_kwh = (int)kwh;
  Serial.println("System online in - 3s");
  delay(1000);
  Serial.println("."); 
  delay(1000);
  Serial.println("."); 
  delay(1000);
  Serial.println("."); 
  Serial.println("System Online !"); 
  digitalWrite(relay,HIGH);  //Relay on
}

//-------------------------------------------------------------//
void readCount(){
  myFile = SD.open("count.txt");
  if (myFile){
    while (myFile.available()){
      String a = myFile.readString();
      count = a.toInt();
    }
    myFile.close();
  }
  else  {
    //Serial.println("Error ! opening count.txt"); // if the file didn't open, print an error:
    //error_msg();
    delay(3000);
  }
}
//-------------------------------------------------------------//
void readKWH()
{
  myFile = SD.open("kwh.txt");
  if (myFile)
  {
    //Serial.print("Reading From - kwh.txt");
    while (myFile.available())
    {
      String a = myFile.readString();
      kwh = a.toFloat();
    }
    myFile.close();
   //Serial.println("\nkWh open done!  File Closed");
  }
  else
  {
   // Serial.println("\nError ! Opening kwh.txt");
   //error_msg();
    delay(3000);
  }
}
//-------------------------------------------------------------//
void writeCount()
{
  myFile = SD.open("count.txt", O_WRITE | O_CREAT | O_TRUNC);
  if (myFile){
    myFile.seek(0);
    myFile.print(count);
    if (count < 10){
      myFile.seek(1);
      myFile.print("-");
    }
    myFile.close();
  }
  else{
    //Serial.println("Write Count Error ! opening count.txt");
    //error_msg();
    delay(3000);
  }
}
//---------------------------------------------------------------//
void writeKWH(){
  unsigned int b = (int)kwh;
  int c = 0;
  if (b < 10){
    c = 1;
  }
  else if (b < 100){
    c = 2;
  }
  else if (b < 1000){
    c = 3;
  }
  else if (b < 10000){
    c = 4;
  }
  myFile = SD.open("kwh.txt", O_WRITE | O_CREAT | O_TRUNC);
  if (myFile)
  {
    //Serial.print("Writing to kwh.txt ");
    myFile.seek(0);
    myFile.print(kwh);
    myFile.seek(c+3);
    myFile.print("-");
    myFile.close();
    //Serial.println("\nkWh = ");
    //Serial.println(kwh);
    new_kwh = (int)kwh;  
    if (pre_kwh < new_kwh){
      kwh_msg();
      pre_kwh = new_kwh;
    }
    //delay(5000);
  }
  else{
    //Serial.println("\nkWh Error ! opening kwh.txt");
    //error_msg();
    delay(3000);
  }
}

//-------------------------------------------------------------------//
void loop(){
  meter_count = analogRead(A0);
  //Serial.print("Count: ");
  //Serial.println(count);
  //Serial.print("Meter Count: ");
  //Serial.println(meter_count);
  if (meter_count > 300){
    state = 1;
    if (lastState != state){
      count++;
      writeCount();
    }
  }
  else{
    state = 0;
  }
  lastState = state; 
  if (count == 16){
    kwh = kwh + 0.01;
    writeKWH(); //save to sd
    count = 0;
//   Serial.print("Power in KwH: ");
  // Serial.println(kwh);
  // delay(2000);
  }
}
//------------------------------------------------------------------------//
void error_msg(){
  digitalWrite(relay,LOW);
  //Serial.println("Message Sent: Memory Error !");
  mySerial.println("AT+CMGF=1"); // Configuring TEXT mode
  updateSerial();
  mySerial.println("AT+CMGS=\"+8801762333199\""); //Setting Mbile number
  updateSerial();
  mySerial.print("Memory Error Occured ! \nBill_Id: 0001 \nUser_Name: Sohan "); //text content
  updateSerial();
  mySerial.write(26);
}
//----------------------------------------------------------------------//
void kwh_msg(){
  digitalWrite(relay,LOW);
  //Serial.println("\nMessage Sent: ");
  String msg;
  msg += F("You have used : ");
  msg += String(kwh, 2);
  msg += F("kWh ");
  //Serial.println(msg);
  mySerial.println("AT+CMGF=1"); // Configuring TEXT mode
  updateSerial();
  mySerial.println("AT+CMGS=\"+8801762333199\"");
  updateSerial();
  mySerial.print(msg); //text content
  updateSerial();
  mySerial.write(26);
}
//---------------------------------------------------------------------//
void updateSerial(){
  delay(10);
  while (Serial.available()) {
    mySerial.write(Serial.read());//Forward what Serial received to Software Serial Port
  }
  while(mySerial.available()) {
    Serial.write(mySerial.read());//Forward what Software Serial received to Serial Port
  }
}
