# PyNasaDSTelemetryDecodingTool
PyNasaDSTelemetryDecodingTool is the python version of NasaDSTelemetryDecodingTool in c++.
 
decode/ds_tlm.bin は、NASAが開発する cFS と呼ばれるオープンソース のフライトソフトウェアが生成した 
Telemetry (100 telemetry分) のバイナリーファイルです。 以下の情報をもとに、Telemetryのフォーマットを調査して、バイナリーファ イルをデコードして、
全てのテレメトリの各パラメータ値を出力するツールを作成し てください。出力方法や表示の仕方、粒度などは自由に決めて問題ありません。 また指定されない限り任意の言語を使っていただいて構いません。

decode/ds_tlm.bin は、DS applicationの House Keeping telemetry の dump です
House Keeping (HK) telemetry の パラメータ (Headerを除く) は、Big endian とします
HK telemetry 内で定義されている OS_MAX_PATH_LEN は 32 とします
Headerで定義されている CFE_MISSION_SB_PACKET_TIME_FORMAT は CFE_MISSION_SB_TIME_32_16_SUBS とします
Headerで定義されている Timeの起点時間 (Epoch)は J2000.0 (2000-01-01 11:58:55.816 UTC) とします
DS application の version は 2.5.1、cFE の version は 6.5.0 とします
実行環境が Little / Big endianどちらでも動作することを想定してくだ さい。ただし実際に Big Endian の環境で動作させる必要はありません
ツールの使い方、動作環境の簡単な説明と、実行結果も添付してください

### AI Chat GPT
I use chat gpt to convert part of the c++ program in python.

## Environnement :
- Python 3
- Windows/linux

## Requirements
- Python 3

## Usage :  
```
py ./DSHKTelemetryDecoder.py run  < FilePath >
```
FilePath is the path to the telemetry binary file.  

### Result of py ./DSHKTelemetryDecoder.py run  < FilePath >
![image](https://github.com/moonlight83340/PyNasaDSTelemetryDecodingTool/assets/6190795/35e39606-9191-4828-9d95-ae24bee5376c)
result.txt contain the result of the command run with the telemetry bin file provided.
