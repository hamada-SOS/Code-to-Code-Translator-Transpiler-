import sys
import unicodedata
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QTextEdit, QPushButton, QFileDialog, QTabWidget, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

from lexer import tokenize
from parser import Parser
from codegen import generate_c

class TranspilerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✨ Pseudo-to-C Transpiler")
        self.resize(1000, 650)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                font-size: 16px;
                color: #1e3a8a;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QTabWidget::pane {
                border: 1px solid #cbd5e1;
                border-radius: 6px;
            }
            QTabBar::tab {
                background: #e0f2fe;
                padding: 6px;
                margin: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #3b82f6;
                color: white;
            }
        """)

        layout = QVBoxLayout()

        self.input_label = QLabel("📝 Enter Pseudo-code:")
        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Type your pseudo-code here...")
        self.input_box.setMinimumHeight(120)

        self.transpile_button = QPushButton("⚙️ Transpile")
        self.transpile_button.clicked.connect(self.transpile_code)

        self.tabs = QTabWidget()
        self.lexer_output = QTextEdit()
        self.lexer_output.setReadOnly(True)
        self.tabs.addTab(self.lexer_output, "🧩 Lexer Output")

        self.ast_output = QTextEdit()
        self.ast_output.setReadOnly(True)
        self.tabs.addTab(self.ast_output, "🌳 AST")

        self.c_output = QTextEdit()
        self.c_output.setReadOnly(False)
        self.tabs.addTab(self.c_output, "💻 C Code")

        self.save_button = QPushButton("💾 Save C Code")
        self.save_button.clicked.connect(self.save_code)

        layout.addWidget(self.input_label)
        layout.addWidget(self.input_box)

        buttons = QHBoxLayout()
        buttons.addWidget(self.transpile_button)
        buttons.addWidget(self.save_button)
        layout.addLayout(buttons)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def transpile_code(self):
        pseudocode = self.input_box.toPlainText()
        if not pseudocode.strip():
            return

        try:
            pseudocode = pseudocode.replace('\r\n', '\n').replace('\t', '    ').strip()
            pseudocode = unicodedata.normalize('NFKC', pseudocode)
            tokens = list(tokenize(pseudocode))
            self.lexer_output.setPlainText("\n".join(map(str, tokens)))

            parser = Parser(tokens)
            ast = parser.parse()

            self.ast_output.setPlainText(self.format_ast(ast))
            c_code = generate_c(ast)
            self.c_output.setPlainText(c_code)

        except Exception as e:
            self.lexer_output.setPlainText(f"Error: {str(e)}")
            self.ast_output.setPlainText("")
            self.c_output.setPlainText("")

    def format_ast(self, ast, level=0):
        indent = "  " * level
        if isinstance(ast, list):
            return "\n".join(self.format_ast(item, level) for item in ast)
        elif hasattr(ast, '__dict__'):
            lines = [f"{indent}{ast.__class__.__name__}:"]
            for k, v in ast.__dict__.items():
                lines.append(f"{indent}  {k}: {self.format_ast(v, level + 1)}")
            return "\n".join(lines)
        else:
            return f"{indent}{repr(ast)}"

    def save_code(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save C Code", "output.c", "C Files (*.c)")
        if path:
            with open(path, "w") as f:
                f.write(self.c_output.toPlainText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranspilerApp()
    window.show()
    sys.exit(app.exec_())
