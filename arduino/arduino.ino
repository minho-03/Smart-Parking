const int buttonPin = 2;   // 스위치를 연결한 핀
const int ledPin = 13;     // 상태 표시용 내장 LED 핀

int lastButtonState = HIGH; // default로 HIGH

void setup() {
  // 버튼 핀을 풀업 저항 모드로 설정 (누르면 LOW, 떼면 HIGH가 됨)
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  
  // PC와 통신하기 위한 시리얼 통신 시작 (속도: 115200)
  Serial.begin(115200); 
}

void loop() {
  int currentButtonState = digitalRead(buttonPin);

  // 버튼이 방금 눌렸을 때 (HIGH -> LOW로 변하는 순간)
  if (lastButtonState == HIGH && currentButtonState == LOW) {
    Serial.println("EMERGENCY_STOP");  // 시리얼모니터로 긴급 정지 신호 전송
    digitalWrite(ledPin, HIGH);        // 경고등(LED) ON
    delay(50);                         
  } 
  // 버튼에서 손을 뗐을 때 (LOW -> HIGH로 변하는 순간)
  else if (lastButtonState == LOW && currentButtonState == HIGH) {
    Serial.println("RELEASED");        // PC로 해제 신호 전송
    digitalWrite(ledPin, LOW);         // 경고등(LED) OFF
    delay(50);                         
  }

  lastButtonState = currentButtonState;
}