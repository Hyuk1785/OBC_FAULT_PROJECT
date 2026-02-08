# OBC_FAULT_PROJECT

## Overview
본 프로젝트는 OBC 고장 사양 진단서를 기반으로 고장 진단 로직을 설계 및 구현한 진단 엔진입니다.  
CAN Raw Data (CSV 파일)를 입력받아 각 고장 코드(0x01 ~ 0x0C)에 대한 진단 결과를 생성합니다.

## Development Period
2025.01 ~ 2025.02

## Features
- 고장 진단 로직 설계 및 구현 (C Language)
- Fault Code별 개별 테스트 CSV 제공
- PyQt5 기반 GUI 진단 툴 구현
- 입력 CSV 분석 후 결과 CSV 자동 생성

## Directory Structure
```
OBC_FAULT_PROJECT/
├── lhj/
│   ├── Debug/ # 각 고장 코드 테스트용 CSV 파일 저장
│   │   ├── fault_0x01_test.csv
│   │   ├── fault_0x02_test.csv
│   │   ├── OBC_FAULT_LOGIC.exe
│   │
│   ├── result/ # 진단 결과 파일 저장
│   │   ├── fault_0x01_test_result.csv
│   │   ├── fault_0x02_test_result.csv
│   │
│   ├── fault.c          # OBC 고장 진단 로직 구현
│   ├── fault.h          # Fault Code 및 진단 인터페이스 정의
│   ├── input.c          # CSV 입력 파싱 모듈
│   ├── input.h
│   ├── main.c           # 진단 엔진 실행 Entry Point
│   ├── fault_test.c     # 개별 Fault 테스트 코드
│   ├── sequence.cpp     # OBC 로직 예시 코드
│   ├── pyqt_test.py     # PyQt5 기반 GUI 진단 프로그램
```

## How to Use
1. PyQt5 GUI 실행(pyqt_test.py)
2. CAN Raw Data CSV 파일 선택
3. "진단 실행" 버튼 클릭
4. 결과 파일이 `lhj/result` 폴더에 생성됨

## Environment
- Language : C
- GUI : Python (PyQt5)
- OS : Windows
- Tool : Visual Studio 2022, VsCode

## Example Input
fault_0x01_test.csv

## Output
fault_0x01_test_result.csv (각 Cycle별 고장 상태 출력)
