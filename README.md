# OBC_FAULT_PROJECT

## Overview
본 프로젝트는 OBC 고장 사양 진단서를 기반으로 고장 진단 로직을 설계 및 구현한 진단 엔진입니다.  
CAN Raw Data (CSV 파일)를 입력받아 각 고장 코드(0x01 ~ 0x0C)에 대한 진단 결과를 생성합니다.

## Development Period
2026.01 ~ 2026.02

## Features
- 고장 진단 로직 설계 및 구현 (C Language)
- Fault Code별 개별 테스트 CSV 제공
- PyQt5 기반 GUI 진단 툴 구현
- 입력 CSV 분석 후 결과 CSV 자동 생성

## Directory Structure
```
OBC_FAULT_PROJECT/
│   ├── Debug/ # 각 고장 코드 테스트용 CSV 파일 저장
│   │   ├── OBC_FAULT_LOGIC.exe
│   │   ├── Unit_Test/ # 각 고장 코드 테스트용 CSV 파일 저장
│   │         ├── fault_0x01_test.csv
│   │         ├── fault_0x02_test.csv
│   │
│   ├── result/ # 종합 진단 결과 파일 저장
│   │   ├── Fault1_test_result.csv # Fault1.csv 전체 고장코드 Log Data 
│   │   ├── Fault2_test_result.csv
│   │
│   │
│   ├── cause/ # 고장 코드별 결과 파일 저장
│   │   ├── Fault1_test # Fault1파일 결과
│   │         ├── F_0x01.csv # 고장코드 0x01 발생 cycle표시
│   │         ├── F_0x03.csv # 고장코드 0x03 발생 cycle표시
│   │   ├── Fault2_test
│   │         ├── F_0x01.csv
│   │         ├── F_0x05.csv
│   │   
│   │
│   ├── fault_log_data/ # 실제 CAN Log Data csv 파일 저장
│   │   ├── Fault1.csv
│   │   ├── Fault2.csv
│   │
│   ├── fault.c          # OBC 고장 진단 로직 구현
│   ├── fault.h          # Fault Code 및 진단 인터페이스 정의
│   ├── input.c          # CSV 입력 파싱 모듈
│   ├── input.h
│   ├── main.c           # 진단 엔진 실행 Entry Point
│   ├── fault_test.c     # 개별 Fault 테스트 코드
│   ├── sequence.cpp     # OBC 로직 예시 코드
│   ├── pyqt_ui.py     # PyQt5 기반 GUI 진단 프로그램
```

## How to Use
1. PyQt5 GUI 실행(pyqt_ui.py)
2. CAN Raw Data CSV 파일 선택
3. "진단 실행" 버튼 클릭
4. 종합 고장 진단 결과 파일이 'result' 폴더에 생성됨
5. 각 고장별 로그 파일이 'cause' 폴더에 생성됨
   
## Environment
- Language : C
- GUI : Python (PyQt5)
- OS : Windows
- Tool : Visual Studio 2022, VsCode

## Example Input
fault_0x01_test.csv

## Output
fault_0x01_test_result.csv (각 Cycle별 고장 상태 출력)

## Change Log
2026.01.27
고장 사양 진단서 작성 완료

2026.02.01
고장 사양 진단서 수정 및 사양 기반 고장 진단 로직 설계&구현

2026.02.03
각 Fault Code(0x01 ~ 0x0C) 진단 로직 단위 테스트(Unit Test) 수행

2026.02.05
PyQt5 기반 GUI 진단 도구 구현

2026.02.07
PyQt5 GUI를 통한 진단 결과 출력 기능 개선 및 상세화

2026.02.09
각 Fault Code 진단 로직 재검증 및 로직 안정화
