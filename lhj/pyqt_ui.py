import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QFileDialog, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import QProcess


class FaultDiagUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OBC Fault Diagnostic Tool")
        self.resize(500, 230)

        self.input_path = ""

        # UI
        self.label = QLabel("Input CSV: 선택되지 않음")
        self.btn_select = QPushButton("Input CSV 선택")
        self.btn_run = QPushButton("진단 실행")

        self.btn_select.clicked.connect(self.select_csv)
        self.btn_run.clicked.connect(self.run_diagnosis)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select)
        layout.addWidget(self.btn_run)
        self.setLayout(layout)

    # =========================
    # CSV 선택
    # =========================
    def select_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Input CSV 선택",
            "",
            "CSV Files (*.csv)"
        )

        if path:
            self.input_path = os.path.normpath(path)
            self.label.setText(f"Input CSV:\n{self.input_path}")

    # =========================
    # 진단 실행 (EXE 호출)
    # =========================
    def run_diagnosis(self):
        if not self.input_path:
            QMessageBox.warning(self, "오류", "Input CSV를 먼저 선택하세요.")
            return

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # -------------------------
        # result 폴더 보장
        # -------------------------
        result_dir = os.path.join(BASE_DIR, "result")
        os.makedirs(result_dir, exist_ok=True)

        # -------------------------
        # 결과 파일 경로 (lhj/result)
        # -------------------------
        base = os.path.splitext(os.path.basename(self.input_path))[0]
        result_path = os.path.normpath(
            os.path.join(result_dir, f"{base}_result.csv")
        )

        # -------------------------
        # exe 경로 (lhj/Debug)
        # -------------------------
        exe_path = os.path.normpath(
            os.path.join(BASE_DIR, "Debug", "OBC_FAULT_LOGIC.exe")
        )

        if not os.path.exists(exe_path):
            QMessageBox.critical(
                self,
                "오류",
                f"OBC_FAULT_LOGIC.exe를 찾을 수 없습니다.\n\n{exe_path}"
            )
            return

        # -------------------------
        # 디버깅 로그
        # -------------------------
        print("====================================")
        print("EXE PATH   :", exe_path)
        print("INPUT PATH :", self.input_path)
        print("RESULT PATH:", result_path)
        print("====================================")

        # -------------------------
        # QProcess 실행
        # -------------------------
        self.process = QProcess(self)

        # Debug 폴더를 작업 디렉토리로 설정
        self.process.setWorkingDirectory(
            os.path.join(BASE_DIR, "Debug")
        )

        self.process.readyReadStandardOutput.connect(
            lambda: print(self.process.readAllStandardOutput().data().decode())
        )
        self.process.readyReadStandardError.connect(
            lambda: print(self.process.readAllStandardError().data().decode())
        )

        self.process.start(exe_path, [self.input_path, result_path])
        self.process.waitForFinished()

        exit_code = self.process.exitCode()
        print("PROCESS EXIT CODE:", exit_code)

        if exit_code != 0:
            QMessageBox.critical(
                self,
                "실패",
                "진단 실행 중 오류가 발생했습니다.\n"
                "콘솔 로그를 확인하세요."
            )
            return

        QMessageBox.information(
            self,
            "완료",
            f"진단 완료!\n\n결과 파일:\n{result_path}"
        )


# =========================
# main
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FaultDiagUI()
    win.show()
    sys.exit(app.exec_())
