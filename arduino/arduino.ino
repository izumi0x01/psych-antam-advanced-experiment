// 処理の流れ

// 1,PC2arduinoでシリアル通信
// 入力データ:Json形式{dt秒,圧力の大きさ}->Arduino_JSON@0.1.0を使用.インストールが必要
// bool isSerialCanGet;
// void GetSerialData();

// 2,電空レギュレータの制御
// 入力:A0、出力:11
// void GetPressure()
// float setPressure()

// 3,流量計の制御
// 入力:A1
// float GetFlowRate()

// 4,arduino2PC,Timer2.hを使用
// 出力データ:JSON形式{arduinoの開始からの経過時間,噴射時間（噴射してないなら-1）,圧力、流量}
// void SetSerialData();

#include <ArduinoJson.h>
#include <MsTimer2.h>
#include <limits.h>

#define readFlowRatePin 55  //A1
#define readPressurePin 54  //A0
#define setPressurePin 8

//メモリサイズが適切でないとJSONを正確に送れないぽい
DynamicJsonDocument readData(32);
DynamicJsonDocument sendData(128);
DeserializationError err;

long measuringTime = -1;
//trigerredTime[s] -> trigerredTime + long measuringTime[s]までの間を推移
long elapsedDt = -1;  
long trigerredTime = -1;
float setPressure = 0;

void setup() {
  
  //シリアル通信の初期化
  Serial.begin(115200);
  sendData["Err"] = 0;
  Serial.setTimeout(10);

  //タイマ割り込みの設定
  MsTimer2::set(20, InterruptSerial);
  MsTimer2::start();

  //ピンモードの設定
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);

}

void loop() {

  // Serial.println("---InLoop---");
  // Serial.print("Serial.available() : ");
  // Serial.println(Serial.available());
  // Serial.print("Serial.peek() : ");
  // Serial.println(Serial.peek());

  if (elapsedDt == -1) {
    Rx(&measuringTime, &setPressure);
  }

  if (now() <= trigerredTime + measuringTime) {
    elapsedDt = now() - trigerredTime;
    SetPressure(setPressure);
  } else if (now() > trigerredTime + measuringTime) {
    elapsedDt = -1;
    trigerredTime = -1;
    SetPressure(0);
  }

  Tx(GetPressure(), GetFlowRate());

  delay(20);
}

long now() {
  if (millis() > (unsigned long)(LONG_MAX)) {
    //arduino止めるなど。
  } else {
    return long(millis());
  }
}

void InterruptSerial() {

  serializeJson(sendData, Serial);
  Serial.println("");
}

// exp) JSONを送る例
//  {"d":500,  "p":200}
// {"d":100,  "p":400}
//      {"d":1000,  "p":200}
//      {"d":1000,  "p":500}
//      {"d":1000,  "p":100}
//      {"d":500,  "p":500}
//      {"d":500,  "p":200}
//     ,{"d":1000,  "p":200,  "_":200}
void Rx(long *pt_measuringTime, float *pt_setPressure) {


  if (Serial.available() == 0)
    return;

  // Serial.println("---OutLoop1---");
  // Serial.print("Ser.avl() : ");
  // Serial.print(Serial.available());
  // Serial.print(", Ser.peek() : ");
  // Serial.println(Serial.peek());

  if (Serial.peek() == 13 || Serial.peek() == 10 || Serial.peek() == 32 || Serial.peek() == 34 || Serial.peek() == 125) {
    sendData["Err"] = "1";//"InvalidInput"
  } else {
    sendData["Err"] = 0;
  }

  delay(5);
  err = deserializeJson(readData, Serial);
  if (err) {
    // Serial.print(F("deserializeJson() failed: "));
    // Serial.println(err.c_str());

    if(String(err.c_str()).equalsIgnoreCase("InvalidInput"))
      sendData["Err"] = 1;
    if(String(err.c_str()).equalsIgnoreCase("IncompleteInput"))
      sendData["Err"] = 2;
    if(String(err.c_str()).equalsIgnoreCase("EmptyInput"))
      sendData["Err"] = 3;
    
  } else {
    sendData["Err"] = 0;
  }



//デシリアライズ後に処理が1000msかかってしまうのは、エラーによりタイムアウトが発生している。
confirm_pos:

  if (Serial.peek() == 13) {
    Serial.read();
    goto confirm_pos;
  } else if (Serial.peek() == 10) {
    Serial.read();
    goto confirm_pos;
  } else if (Serial.peek() == 123) {
    Serial.read();
    goto confirm_pos;
  } else if (Serial.peek() == 34) {
    Serial.read();
    goto confirm_pos;
  } else if (Serial.peek() == 125) {
    Serial.read();
    goto confirm_pos;
  } else if (Serial.peek() == 32) {
    Serial.read();
    goto confirm_pos;
  }


    // Serial.println("---OutLoop2---");
    // Serial.print("Serial.available() : ");
    // Serial.print(Serial.available());
    // Serial.print(", Serial.peek() : ");
    // Serial.println(Serial.peek());

  long _d = readData["d"];
  float _p = readData["p"];

  // Serial.println("changedData!");
  // Serial.print("d:");
  // Serial.print(_d);
  // Serial.print(" ,p:");
  // Serial.println(_p);

  if (!readData.isNull()) {

    *pt_setPressure = readData["p"];
    // *pt_setPressure *= 0.01;
    // readData.remove("sP");

    *pt_measuringTime = readData["d"];
    // *pt_measuringTime *= 100;

    readData.clear();
  }

  //エラーが出てタイムアウトした場合は,JSONOBJECTの要素に0要素が格納される。エラー処理。
  if (_d == long(0) || _p == float(0))
    return;

  //データがセットされたタイミングでtrigerが起動.
  trigerredTime = now();
  sendData["Err"] = 0;
}

void Tx(float _readPressure, float _readFlowRate) {
  // 送信するシリアルデータを整える.送信は割り込み中に行う。
  // sendData["t"] = millis();
  // //if (elapsedDt < 0)
  // //elapsedDt = -1;
   sendData["d"] = elapsedDt;
  // sendData["P"] = _readPressure;
  sendData["F"] = _readFlowRate;

  //parametercheck
  // Serial.print("setPressure: ");
  // Serial.print(setPressure);
  // Serial.print(", measuringTime: ");
  // Serial.print(measuringTime);
  // Serial.print(", elapsedDt: ");
  // Serial.println(elapsedDt);
}

float GetPressure() {
  return analogRead(readPressurePin);
}

void SetPressure(float _val) {
  _val = map(_val, 0, 1000, 0, 255);
  analogWrite(setPressurePin, _val);
}

float GetFlowRate() {
  return analogRead(readFlowRatePin);
}