#include <stdio.h>
#include "fault.h"

#define input_file "Fault1.csv"
#define result_file "Result1.csv"

int main(void)
{

    FILE* fp = fopen(input_file, "r");
    FILE* out = fopen(result_file, "w");
    InputSnapshot in = { 0 };

    // 입력 CSV 오류 방지
    if (!fp)
    {
        printf("Input CSV open failed\n");
        return 1;
    }

    // 결과 CSV 오류 방지
    if (!out)
    {
        printf("Result CSV open failed\n");
        fclose(fp);
        return 1;
    }

    /* CSV 헤더 */
    fprintf(out, "Cycle,"
        "F_0x01,F_0x02,F_0x03,F_0x04,F_0x05,F_0x06,"
        "F_0x07,F_0x08,F_0x09,F_0x0A,F_0x0B,F_0x0C\n"
    );

    Fault_Init();

    /* 메인 진단 루프 */
    while (Input_ReadLine(fp, &in))
    {
        /* 1. 모든 고장 진단 (판단만) */
        Fault_Diagnose(&in);

        /* 2. 결과 기록 */
        fprintf(out, "%d", in.Cycle);

        fprintf(out, ",%d", Fault_GetStatus(FAULT_INPUT_OVERCURRENT));
        fprintf(out, ",%d", Fault_GetStatus(FAULT_INPUT_UNDERCURRENT));
        fprintf(out, ",%d", Fault_GetStatus(FAULT_PLUG));
        fprintf(out, ",%d", Fault_GetStatus(FAULT_RELAY));
        fprintf(out, ",%d", Fault_GetStatus(FAULT_BMS_STATE));
        fprintf(out, ",%d", Fault_GetStatus(FAULT_OVER_TEMP));
        fprintf(out, ",%d", Fault_GetStatus(FAULT_CAN));
        fprintf(out, ",%d", Fault_GetStatus(FAULT_ISO));
        fprintf(out, ",%d", Fault_GetStatus(FAULT_PAYMENT));
        fprintf(out, ",%d", Fault_GetStatus(FAULT_WDT));
        fprintf(out, ",%d", Fault_GetStatus(FAULT_SEQ_TIMEOUT));
        fprintf(out, ",%d", Fault_GetStatus(FAULT_TEMP_SENSOR));

        fprintf(out, "\n");
    }
    fclose(fp);
    fclose(out);

    // 단위 테스트 코드입니다. 
    // 하나씩 실행 시키면, 각각의 test_case에 대한 결과값이 출력됩니다.
    /*Test_Fault_0x01("fault_0x01_test.csv");*/
    /*Test_Fault_0x02("fault_0x02_test.csv");*/
    /*Test_Fault_0x03("fault_0x03_test.csv");*/
    /*Test_Fault_0x04("fault_0x04_test.csv");*/
    /*Test_Fault_0x05("fault_0x05_test.csv");*/
    /*Test_Fault_0x06("fault_0x06_test.csv");*/
    /*Test_Fault_0x07("fault_0x07_test.csv");*/
    /*Test_Fault_0x08("fault_0x08_test.csv");*/
    /*Test_Fault_0x09("fault_0x09_test.csv");*/
    /*Test_Fault_0x0A("fault_0x0A_test.csv");*/
    /*Test_Fault_0x0B("fault_0x0B_test.csv");*/
    /*Test_Fault_0x0C("fault_0x0C_test.csv");*/
    return 0;
}
