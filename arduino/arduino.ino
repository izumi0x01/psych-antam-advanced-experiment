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

// allocate the memory for the document
// StaticJsonDocument<1024> inSerialData;
// StaticJsonDocument<1024> outSerialData;

//メモリサイズが適切でないとJSONを正確に送れないぽい
DynamicJsonDocument data(1024);

bool rxAvailable = false;
long setDt = -1;
long elapsedDt = 0;  //0[s] -> elapsedDt[s]までの間を推移
unsigned long trigerTiming = 0;
float setPressure = 0;
float readPressure = 100.000001;
float readFlowRate = 2.302038;


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
    Rx();
  }

  // put your main code here, to run repeatedly:

  //フラグ処理:micros() - trigerTimingは、計測開始してからの経過時間。
  // 計測の経過時間が計測の設定時間を超えない限りは経過時間に計測時間が代入される。計測時間が過ぎると経過時間は-1になる。
  if (setDt != -1 && long(millis() - trigerTiming) <= setDt) {
    elapsedDt = millis() - trigerTiming;
    SetPressure();
  } else {
    elapsedDt = -1;
  }

  if (elapsedDt == -1) {
    trigerTiming = millis();
    setDt = -1;
  }

  GetPressure();
  GetFlowRate();


  Tx();


  delay(100);
}


void OperateSerial() {
  if (Serial.available() > 0) {
    rxAvailable = true;
  }

  serializeJson(data, Serial);
  Serial.println("");
}

void Rx() {
  deserializeJson(data, Serial);

  if (!data["sP"].isNull())
  {

    setPressure = data["sP"];
  data.remove("sP");
  }

  if (!data["sDt"].isNull())
  {
    setDt = data["sDt"];
  data.remove("sDt");

  }

  rxAvailable = false;

}

void Tx() {
  // 送信するシリアルデータを整える
  data["T"] = millis();
  data["Dt"] = elapsedDt;
  data["P"] = readPressure;
  data["F"] = readFlowRate;

  //parametercheck
  Serial.print("setPressure: ");
  Serial.print(setPressure);
  Serial.print(", setDt: ");
  Serial.print(setDt);
  Serial.print(", elapsedDt: ");
  Serial.println(elapsedDt);
}

void GetPressure() {
}

float SetPressure() {
}

float GetFlowRate() {
}