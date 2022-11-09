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

#define readFlowRatePin 15  //A1
#define readPressurePin 14  //A0
#define setPressurePin 11
const unsigned long offsettime = 1100;

// allocate the memory for the document
// StaticJsonDocument<1024> inSerialData;
// StaticJsonDocument<1024> outSerialData;

//メモリサイズが適切でないとJSONを正確に送れないぽい
DynamicJsonDocument readData(516);
DynamicJsonDocument sendData(516);

bool rxAvailable = false;
long setDt = -1;
long elapsedDt = -1;  //0[s] -> elapsedDt[s]までの間を推移
unsigned long trigerTiming = 0;
float setPressure = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  MsTimer2::set(100, OperateSerial);
  MsTimer2::start();
}

void loop() {


  // exp) {"sDt":5000,  "sP":20}
  // シリアル通信
  if (rxAvailable == true) {
    Rx(&setDt, &setPressure);
  }

  // put your main code here, to run repeatedly:

  //フラグ処理:micros() - trigerTimingは、計測開始してからの経過時間。
  // 計測の経過時間が計測の設定時間を超えない限りは経過時間に計測時間が代入される。計測時間が過ぎると経過時間は-1になる。
  if (setDt != -1 && long(millis() - trigerTiming - offsettime) <= setDt) {
    elapsedDt = millis() - trigerTiming - offsettime;
  } else {
    elapsedDt = -1;
  }

  if (elapsedDt > 0) {
    SetPressure(setPressure);
  } else {
    SetPressure(0);
  }
  
  if(long(millis() - trigerTiming - offsettime) > setDt)
  {
    trigerTiming = millis();
    setDt = -1;
  }


  Tx(GetPressure(), GetFlowRate());

  delay(50);
}


void OperateSerial() {
  if (Serial.available() > 0) {
    rxAvailable = true;
  }

  serializeJson(sendData, Serial);
  Serial.println("");
}

void Rx(long *pt_setDt, float *pt_setPressure) {
  deserializeJson(readData, Serial);

  if (!readData.isNull()) {

    *pt_setPressure = readData["sP"];
    // readData.remove("sP");

    *pt_setDt = readData["sDt"];
    // readData.remove("sDt");
    readData.clear();
  }

  rxAvailable = false;
}

void Tx(float _readPressure, float _readFlowRate) {
  // 送信するシリアルデータを整える
  sendData["T"] = millis();
  sendData["Dt"] = elapsedDt;
  sendData["P"] = _readPressure;
  sendData["F"] = _readFlowRate;

  //parametercheck
  // Serial.print("setPressure: ");
  // Serial.print(setPressure);
  // Serial.print(", setDt: ");
  // Serial.print(setDt);
  // Serial.print(", elapsedDt: ");
  // Serial.println(elapsedDt);
}

float GetPressure() {
  return analogRead(readPressurePin);
}

void SetPressure(float _val) {
  _val = map(_val, 0, 1023, 0, 255);
  analogWrite(setPressurePin, _val);
}

float GetFlowRate() {
  return analogRead(readFlowRatePin);
}