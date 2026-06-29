volatile int cnt = 0;
volatile int can_move = 1;
String state = "";
void setup() {
  pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), switchInterrupt, FALLING);
  Serial.begin(9600);
}
void move(int sleep_time){
  if(can_move){
    digitalWrite(6, HIGH);
    digitalWrite(LED_BUILTIN, HIGH);
    cnt += can_move;
    delay(sleep_time);
    digitalWrite(LED_BUILTIN, LOW);
    digitalWrite(6, LOW); 
  }
}
void move_slow(){
  move(100);
}
void move_fast(){
  move(10);
}
void switchInterrupt(){
  cnt = 0;
  state = "INTERRUPTED";
  Serial.println("STOPPED");
  can_move = 0;
}
void move_conv(int conv){
  if(conv < 0){
    digitalWrite(5, LOW);
    conv = -conv;
  }else{
    digitalWrite(5, HIGH);
  }
  if(cnt > conv){
    cnt = 0;
    state = "";
  }else{
    move_fast();
  }
}

void loop() {
  Serial.println(state);
  can_move = 1;
  if(state == "INTERRUPTED"){
    digitalWrite(5, !digitalRead(5));
    move(10);
    state = "";
    cnt = 0;
  }
  if(Serial.available() > 0){
    state = Serial.readStringUntil('\n');
  }
  if(state == "" || state == "N"){
    if(state == "N"){
      cnt = 0;
    }
  }
  if(state == "FAST"){
    move_fast();
  }
  else if(state == "SLOW"){
    move_slow();
  }
  else if(state == "R"){
    digitalWrite(5, !digitalRead(5));
    cnt = 0;
    state = "";
  }else if(state.startsWith("I:")){
    move_conv(state.substring(2).toInt());
  }
}
