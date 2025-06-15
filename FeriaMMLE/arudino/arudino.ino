// Pines del sensor y actuadores
const int pinSensorAgua = A0;
 
const int ledRojo = 2;
const int ledVerde = 3;
const int ledExtra = 4;
const int buzzer = 5;
 
bool estadoBuzzer = false; // Estado intermitente del buzzer
unsigned long tiempoAnterior = 0;
const unsigned long intervaloBuzzer = 1000; // 1 segundo
 
void setup() {
  Serial.begin(9600);
  // Configurar los pines como salida
  pinMode(ledRojo, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledExtra, OUTPUT);
  pinMode(buzzer, OUTPUT);
}
 
void loop() {
  int valorSensor = analogRead(pinSensorAgua);
  Serial.print("Nivel de agua: ");
  Serial.println(valorSensor);
  delay(1000); // Espera 1 segundo entre lecturas
 
  unsigned long tiempoActual = millis();
 
  if (valorSensor > 250) {
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
  }
 
  digitalWrite(ledExtra, LOW); // LED extra apagado por ahora
}