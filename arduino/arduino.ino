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

#define readFlowRatePin 15  //A1
#define readPressurePin 14  //A0
#define setPressurePin 9

//メモリサイズが適切でないとJSONを正確に送れないぽい
StaticJsonDocument<64> readData;
DynamicJsonDocument sendData(128);

long measuringTime = -1;
long elapsedDt = -1;  //trigerredTime[s] -> trigerredTime + elapsedDt[s]までの間を推移
long trigerredTime = -1;
float setPressure = 0;
const long offsetTime = 100000;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  MsTimer2::set(50, InterruptSerial);
  MsTimer2::start();
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
}

void loop() {

  if (elapsedDt == -1) {
    if (Serial.available() > 0) {
      Rx(&measuringTime, &setPressure);
      //データがセットされたタイミングでtrigerが起動.
      trigerredTime = now();
    }
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

  delay(50);
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

void Rx(long *pt_measuringTime, float *pt_setPressure) {

  // {"d":1000,  "p":200}
  deserializeJson(readData, Serial);

  //汚いが...deserializeは開始と終わりで値がそれぞれ値が代入されるようにできているらしい（？）。
  //開始時のデータだけを読み取って、2回目はパスする。
  //そのため、loopのdelayを極端に短くすると、analog出力などがうまくできない...

  if (!readData.isNull()) {

    *pt_setPressure = readData["p"];
    // *pt_setPressure *= 0.01;
    // readData.remove("sP");

    *pt_measuringTime = readData["d"];
    // *pt_measuringTime *= 100;

    // readData.remove("sDt");
    readData.clear();
  }
}

void Tx(float _readPressure, float _readFlowRate) {
  // 送信するシリアルデータを整える.送信は割り込み中に行う。
  sendData["t"] = millis();
  //if (elapsedDt < 0)
  //elapsedDt = -1;
  sendData["d"] = elapsedDt;
  sendData["P"] = _readPressure;
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