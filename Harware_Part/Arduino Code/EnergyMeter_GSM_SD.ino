#include <SoftwareSerial.h>
#include <SD.h>

// Pin configuration
#define SIM800L_TX 3
#define SIM800L_RX 2
#define PULSE_SENSOR A0
#define RELAY_PIN 1

// SIM800L and SD Card
SoftwareSerial SIM800L(SIM800L_TX, SIM800L_RX);
File myFile;

// State variables
int pulseState = 0, count = 0;
float kwh = 0.0;
bool state = false, lastState = false;

// Constants
const int PULSE_THRESHOLD = 350;
const int COUNTS_PER_KWH = 16;

// Function prototypes
void showSerialData();
void submitHttpRequest();
void readKWH();
void readCount();
void writeCount();
void writeKWH();

void setup() {
    pinMode(PULSE_SENSOR, INPUT);
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW);

    SIM800L.begin(19200);
    Serial.begin(19200);
    delay(500);

    // Initialize SD card
    if (!SD.begin()) {
        Serial.println("SD Card Initialization failed!");
        while (true) delay(1000);
    }
    Serial.println("SD Card Initialized!");

    // Read previous data
    readCount();
    readKWH();

    // Display previous data
    Serial.println("Previous Count: " + String(count));
    Serial.println("Previous kWh: " + String(kwh));

    // Initialize GSM module
    SIM800L.println("AT");
    delay(500);
    showSerialData();

    SIM800L.println("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"");
    delay(500);
    SIM800L.println("AT+SAPBR=3,1,\"APN\",\"GPINTERNET\"");
    delay(500);
    SIM800L.println("AT+SAPBR=1,1");
    delay(500);
    SIM800L.println("AT+HTTPINIT");
    delay(500);
    SIM800L.println("AT+HTTPPARA=\"URL\",\"http://electricity-billing.herokuapp.com/info?id=10001&code=101\"");
    delay(1000);
    showSerialData();

    Serial.println("System Online!");
    digitalWrite(RELAY_PIN, HIGH); // Relay on
}

void loop() {
    pulseState = analogRead(PULSE_SENSOR);
    Serial.println(pulseState);

    if (pulseState > PULSE_THRESHOLD) {
        state = true;
        if (lastState != state) {
            count++;
            writeCount();
            Serial.println("Pulse Detected! Count: " + String(count));
        }
    } else {
        state = false;
    }

    lastState = state;

    if (count >= COUNTS_PER_KWH) {
        kwh += 0.01;
        writeKWH();
        count = 0;
        writeCount();
    }

    delay(10);
}

// Display data received from SIM800L
void showSerialData() {
    while (SIM800L.available()) {
        Serial.write(SIM800L.read());
    }
}

// Submit HTTP request with kWh data
void submitHttpRequest() {
    SIM800L.println("AT+HTTPPARA=\"URL\",\"http://e--bill.herokuapp.com/meter?id=0170875&code=101&kwh=" + String(kwh) + "\"");
    delay(100);
    SIM800L.println("AT+HTTPACTION=0");
    delay(500);
    showSerialData();
}

// Read kWh from SD card
void readKWH() {
    myFile = SD.open("kwh.txt");
    if (myFile) {
        String data = myFile.readString();
        kwh = data.toFloat();
        myFile.close();
    } else {
        Serial.println("Error opening kwh.txt");
    }
}

// Read count from SD card
void readCount() {
    myFile = SD.open("count.txt");
    if (myFile) {
        String data = myFile.readString();
        count = data.toInt();
        myFile.close();
    } else {
        Serial.println("Error opening count.txt");
    }
}

// Write count to SD card
void writeCount() {
    myFile = SD.open("count.txt", O_WRITE | O_CREAT | O_TRUNC);
    if (myFile) {
        myFile.print(count);
        myFile.close();
    } else {
        Serial.println("Error writing to count.txt");
    }
}

// Write kWh to SD card and submit to server
void writeKWH() {
    myFile = SD.open("kwh.txt", O_WRITE | O_CREAT | O_TRUNC);
    if (myFile) {
        myFile.print(kwh);
        myFile.close();
        submitHttpRequest();
    } else {
        Serial.println("Error writing to kwh.txt");
    }
}
