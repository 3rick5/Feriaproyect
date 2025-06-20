#include "DHT.h"

#define DHTPIN 6         // Pin donde está conectado el sensor
#define DHTTYPE DHT11    // Cambiá a DHT22 si usás ese

DHT dht(DHTPIN, DHTTYPE);  // <- Aquí estás creando el objeto 'dht'

// Pines del sensor y actuadores
const int pinSensorAgua = A0;
const int ledRojo = 3;
const int ledVerde = 2;
const int ledExtra = 4;
const int buzzer = 5;
 
bool estadoBuzzer = false; // Estado intermitente del buzzer
unsigned long tiempoAnterior = 0;
const unsigned long intervaloBuzzer = 1000; // 1 segundo


void setup() {
  Serial.begin(9600);
  dht.begin();  // <-- Muy importante para que el sensor funcione

  // Configurar los pines como salida
  pinMode(ledRojo, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledExtra, OUTPUT);
  pinMode(buzzer, OUTPUT);
}
void loop() {

  int sensorValue = analogRead(A0);
  Serial.print("Nivel de agua: ");
  Serial.println(sensorValue);  // Esto manda el valor tal como lo lee el sensor
  delay(3000);

  int valorSensor = analogRead(pinSensorAgua);
  Serial.print("Nivel de agua: ");
  Serial.println(valorSensor);
 
  unsigned long tiempoActual = millis();
 
  if (valorSensor > 850) {
    digitalWrite(ledRojo, HIGH);
    digitalWrite(ledVerde, LOW);
 
    // Buzzer intermitente
    if (tiempoActual - tiempoAnterior >= intervaloBuzzer) {
      tiempoAnterior = tiempoActual;
      estadoBuzzer = !estadoBuzzer; // Alterna entre encendido y apagado
      digitalWrite(buzzer, estadoBuzzer);
    }
 
  } else {
    // Nivel bajo: LED verde encendido, rojo y buzzer apagados
    digitalWrite(ledRojo, LOW);
    digitalWrite(ledVerde, HIGH);
    digitalWrite(buzzer, LOW);
    estadoBuzzer = false; // Reinicia el estado del buzzer
    delay(3000);
  }
 delay(1000);
  digitalWrite(ledExtra, LOW); // LED extra apagado por ahora

    delay(3000);
  float h = dht.readHumidity(); //Leemos la Humedad
  float t = dht.readTemperature(); //Leemos la temperatura en grados Celsius
  float f = dht.readTemperature(true); //Leemos la temperatura en grados Fahrenheit
  //--------Enviamos las lecturas por el puerto serial-------------
  Serial.print("Humedad ");
  Serial.print(h);
  Serial.print(" %t");
  Serial.print("Temperatura: ");
  Serial.print(t);
  Serial.print(" *C ");
  Serial.print(f);
  Serial.println(" *F");
}