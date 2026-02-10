# -*- coding: utf-8 -*-
"""
Generate 3 raw data CSV files for OBC Fault Diagnostic testing.
Each file triggers 4 specific faults (total 12 faults covered).

data1.csv: 0x01(Overcurrent), 0x04(Relay), 0x06(OverTemp), 0x0C(TempSensor)
data2.csv: 0x02(Undercurrent), 0x03(Plug), 0x09(Payment), 0x0B(SeqTimeout)
data3.csv: 0x05(BMS), 0x07(CAN), 0x08(ISO), 0x0A(WDT)
"""
import csv, os

HEADER = ["Cycle","SeqState","PlugInfo","FLAG_Stop","FLAG_Relay",
          "Ia","Ib","Ic","FaultState","Charg_Cnt",
          "Real_Battery_Voltage","Expected Battery_Voltage",
          "H","CanMsg_Received","IsoR"]

def write_csv(filepath, rows):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        for r in rows:
            w.writerow(r)
    print(f"Created: {filepath} ({len(rows)} cycles)")

def make_row(cy, seq, plug, stop, relay, ia, ib, ic, fs, cc, rv, ev, h, can, iso):
    return [cy, seq, plug, stop, relay, ia, ib, ic, fs, cc, rv, ev, h, can, iso]

# ============================================================
# data1.csv: 0x01(Overcurrent), 0x04(Relay), 0x06(OverTemp), 0x0C(TempSensor)
# ============================================================
def gen_data1():
    rows = []
    R = lambda *a: rows.append(make_row(*a))

    # Phase 1: INIT (1-5)
    for c in range(1,6):
        R(c, 0,0,1,0, 0,0,0, 0,0, 398+c%3,400, 15, 1,800000)

    # Phase 2: Plug connected (6-7)
    R(6, 0,1,1,0, 0,0,0, 0,0, 398,400, 15, 1,800000)
    R(7, 0,1,1,0, 0,0,0, 0,0, 399,400, 15, 1,800000)

    # Phase 3: WAIT (8-11)
    for c in range(8,12):
        R(c, 1,1,1,0, 0,0,0, 0,0, 399+c%2,400, 15, 1,800000)

    # Phase 4: Transition + CHARGING start (12-25)
    R(12, 1,2,0,1, 4,5,4, 0,0, 398,400, 15, 1,800000)
    cc = 0
    for c in range(13,26):
        cc += 1
        ia = min(10 + cc, 22)
        R(c, 2,2,0,1, ia,ia-1,ia-2, 0,cc, 400+cc//3,400, 15+cc//2, 1,800000)

    # Phase 5: Current rising toward overcurrent (26-35), temp rising
    for c in range(26,36):
        cc += 1
        ia = 22 + (c-26)*1  # 22->32
        h = 20 + (c-26)*3   # 20->50
        R(c, 2,2,0,1, ia,ia-1,ia-2, 0,cc, 405+cc//5,400, h, 1,800000)

    # Phase 6: Overcurrent zone Ia>32 for 12 cycles (36-47)
    # 0x01: over_cnt reaches 10 at cycle 45 -> CONFIRM
    for c in range(36,48):
        cc += 1
        ia = 33 + (c-36)%4  # 33-36 oscillating
        h = 50 + (c-36)*1   # 50->62
        fs = 1 if c >= 36 else 0
        R(c, 2,2,0,1, ia,ia-1,ia+1, fs,cc, 410+cc//5,400, h, 1,800000)

    # Phase 7: H > 60 sustained for 12 cycles (48-59), current drops
    # 0x06: heat_cnt reaches 10 at cycle 57 -> CONFIRM
    for c in range(48,60):
        cc += 1
        ia = 20 - (c-48)//3  # dropping current
        h = 62 + (c-48)*2    # 62->86
        R(c, 2,2,0,1, ia,ia+1,ia-1, 1,cc, 415+cc//8,400, h, 1,800000)

    # Phase 8: Relay fault - FLAG_Relay=0, FLAG_Stop=0 (60-61)
    # 0x04: immediate CONFIRM
    for c in range(60,62):
        cc += 1
        R(c, 2,2,0,0, 18,17,19, 1,cc, 420,400, 90+c-60, 1,800000)

    # Phase 9: Restore relay, temp spikes >120 for 4 cycles (62-65)
    # 0x0C: temp_fault_cnt reaches 3 at cycle 64 -> CONFIRM
    for c in range(62,66):
        cc += 1
        R(c, 2,2,0,1, 17,18,17, 1,cc, 422,400, 122+(c-62)*3, 1,800000)

    # Phase 10: Enter FAULT state (66-74)
    R(66, 2,2,1,0, 0,0,0, 2,cc, 422,400, 90, 1,800000)
    for c in range(67,75):
        R(c, 3,2,1,0, 0,0,0, 2,cc, 420-(c-67),400, 85-(c-67)*3, 1,800000)

    # Phase 11: RESET (75-76)
    R(75, 3,2,0,1, 0,0,0, 0,cc, 410,400, 50, 1,800000)
    R(76, 4,2,0,1, 0,0,0, 0,0, 408,400, 45, 1,800000)

    # Phase 12: Back to INIT (77-85)
    for c in range(77,86):
        h = max(15, 40-(c-77)*3)
        R(c, 0,0,1,0, 0,0,0, 0,0, 400,400, h, 1,800000)

    return rows

# ============================================================
# data2.csv: 0x02(Undercurrent), 0x03(Plug), 0x09(Payment), 0x0B(SeqTimeout)
# ============================================================
def gen_data2():
    rows = []
    R = lambda *a: rows.append(make_row(*a))

    # Phase 1: INIT (1-5)
    for c in range(1,6):
        R(c, 0,0,1,0, 0,0,0, 0,0, 398+c%3,400, 15, 1,800000)

    # Phase 2: Plug connected NO PAYMENT (6-7), PlugInfo=1
    R(6, 0,1,1,0, 0,0,0, 0,0, 398,400, 15, 1,800000)
    R(7, 0,1,1,0, 0,0,0, 0,0, 399,400, 15, 1,800000)

    # Phase 3: WAIT with PlugInfo=1 for 14 cycles (8-21)
    # 0x09: pay_err_cnt reaches 5 at cycle 12 -> CONFIRM (SeqState!=2, PlugInfo==1)
    # 0x0B: seq_timer reaches 10 at cycle 17 -> CONFIRM (SEQ_WAIT timeout)
    for c in range(8,22):
        R(c, 1,1,1,0, 0,0,0, 0,0, 399+c%2,400, 15, 1,800000)

    # Phase 4: Back to INIT, payment made -> recovers 0x09 and 0x0B
    R(22, 0,2,1,0, 0,0,0, 0,0, 399,400, 15, 1,800000)
    R(23, 0,2,1,0, 0,0,0, 0,0, 400,400, 15, 1,800000)

    # Phase 5: Proper WAIT -> CHARGING (24-27)
    R(24, 1,2,1,0, 0,0,0, 0,0, 399,400, 15, 1,800000)
    R(25, 1,2,1,0, 0,0,0, 0,0, 400,400, 15, 1,800000)
    R(26, 1,2,0,1, 4,5,4, 0,0, 399,400, 15, 1,800000)

    # Phase 6: Normal charging (27-50)
    cc = 0
    for c in range(27,51):
        cc += 1
        ia = min(10+cc, 19)
        R(c, 2,2,0,1, ia,ia-1,ia+1, 0,cc, 400+cc//3,400, 15+cc//3, 1,800000)

    # Phase 7: Current drops very low, Charg_Cnt > 20 (51-62)
    # 0x02: Ia<6 && Ib<6 && Ic<6, Charg_Cnt>20, SeqState==2
    # under_cnt reaches 10 at cycle 60 -> CONFIRM
    for c in range(51,63):
        cc += 1
        ia = 4 - (c-51)//4  # 4->2
        ia = max(1, ia)
        R(c, 2,2,0,1, ia,ia+1,ia, 0,cc, 415+cc//8,400, 22+cc//5, 1,800000)

    # Phase 8: Plug disconnects during charging (63-64)
    # 0x03: SeqState==CHARGING && PlugInfo==0 -> immediate CONFIRM
    R(63, 2,0,0,1, 3,4,3, 0,cc+1, 420,400, 25, 1,800000)
    R(64, 2,0,0,1, 2,3,2, 0,cc+2, 420,400, 25, 1,800000)

    # Phase 9: Enter FAULT (65-74)
    R(65, 2,0,1,0, 0,0,0, 2,cc+2, 420,400, 24, 1,800000)
    for c in range(66,75):
        R(c, 3,0,1,0, 0,0,0, 2,cc+2, 418-(c-66),400, 24-(c-66)//2, 1,800000)

    # Phase 10: RESET (75-76)
    R(75, 3,0,0,1, 0,0,0, 0,cc+2, 408,400, 20, 1,800000)
    R(76, 4,0,0,1, 0,0,0, 0,0, 406,400, 19, 1,800000)

    # Phase 11: INIT cooldown (77-90)
    for c in range(77,91):
        R(c, 0,0,1,0, 0,0,0, 0,0, 400,400, max(15, 19-(c-77)), 1,800000)

    return rows

# ============================================================
# data3.csv: 0x05(BMS), 0x07(CAN), 0x08(ISO), 0x0A(WDT)
# ============================================================
def gen_data3():
    rows = []
    R = lambda *a: rows.append(make_row(*a))

    # Phase 1: INIT (1-5)
    for c in range(1,6):
        R(c, 0,0,1,0, 0,0,0, 0,0, 398+c%3,400, 15, 1,800000)

    # Phase 2: Plug + WAIT (6-11)
    R(6, 0,1,1,0, 0,0,0, 0,0, 398,400, 15, 1,800000)
    R(7, 0,1,1,0, 0,0,0, 0,0, 399,400, 15, 1,800000)
    R(8, 1,1,1,0, 0,0,0, 0,0, 399,400, 15, 1,800000)
    R(9, 1,1,1,0, 0,0,0, 0,0, 400,400, 15, 1,800000)
    R(10, 1,2,0,1, 4,5,4, 0,0, 399,400, 15, 1,800000)

    # Phase 3: CHARGING normal (11-25)
    cc = 0
    for c in range(11,26):
        cc += 1
        ia = min(10+cc, 19)
        R(c, 2,2,0,1, ia,ia-1,ia+1, 0,cc, 400+cc//3,400, 15+cc//3, 1,800000)

    # Phase 4: BMS voltage deviation |Real_V - Exp_V| > 10 for 12 cycles (26-37)
    # 0x05: Charg_Cnt>10, diff>10 -> batt_cnt reaches 10 at cycle 35 -> CONFIRM
    for c in range(26,38):
        cc += 1
        rv = 415 + (c-26)  # voltage climbing away from 400
        R(c, 2,2,0,1, 18,17,19, 0,cc, rv,400, 20+cc//4, 1,800000)

    # Phase 5: CAN loss for 7 cycles (38-44)
    # 0x07: CanMsg==0, can_to_cnt reaches 5 at cycle 42 -> CONFIRM
    for c in range(38,45):
        cc += 1
        R(c, 2,2,0,1, 17,18,17, 1,cc, 420,400, 25, 0,800000)

    # Phase 6: CAN recovers, IsoR drops below 500 for 12 cycles (45-56)
    # 0x08: iso_cnt reaches 10 at cycle 54 -> CONFIRM
    for c in range(45,57):
        cc += 1
        iso = max(50, 450 - (c-45)*40)  # 450->10
        R(c, 2,2,0,1, 17,18,17, 1,cc, 420,400, 26, 1, iso)

    # Phase 7: WDT - cycle jumps (57->70, diff=13 >10)
    # 0x0A: single jump >10 -> immediate CONFIRM (latched)
    cc += 1
    R(70, 2,2,0,1, 17,18,17, 1,cc, 421,400, 27, 1,400)

    # Continue a few more cycles after WDT
    for c in range(71,76):
        cc += 1
        R(c, 2,2,0,1, 16,17,16, 1,cc, 421,400, 27, 1,800000)

    # Phase 8: Enter FAULT (76-84)
    R(76, 2,2,1,0, 0,0,0, 2,cc, 421,400, 26, 1,800000)
    for c in range(77,85):
        R(c, 3,2,1,0, 0,0,0, 2,cc, 418-(c-77),400, 25-(c-77)//2, 1,800000)

    # Phase 9: RESET (85-86)
    R(85, 3,2,0,1, 0,0,0, 0,cc, 410,400, 20, 1,800000)
    R(86, 4,2,0,1, 0,0,0, 0,0, 408,400, 19, 1,800000)

    # Phase 10: INIT cooldown (87-95)
    for c in range(87,96):
        R(c, 0,0,1,0, 0,0,0, 0,0, 400,400, max(15, 19-(c-87)), 1,800000)

    return rows


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    rawdir = os.path.join(base, "rawdata")

    write_csv(os.path.join(rawdir, "data1.csv"), gen_data1())
    write_csv(os.path.join(rawdir, "data2.csv"), gen_data2())
    write_csv(os.path.join(rawdir, "data3.csv"), gen_data3())

    print("\nFault coverage:")
    print("  data1.csv -> 0x01(Overcurrent), 0x04(Relay), 0x06(OverTemp), 0x0C(TempSensor)")
    print("  data2.csv -> 0x02(Undercurrent), 0x03(Plug), 0x09(Payment), 0x0B(SeqTimeout)")
    print("  data3.csv -> 0x05(BMS), 0x07(CAN), 0x08(ISO), 0x0A(WDT)")
    print("All 12 faults covered!")
