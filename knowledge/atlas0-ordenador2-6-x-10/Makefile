# Atlas0 build and validation commands.

PYTHON ?= python3
VENV ?= .venv
RUSTCVER ?= 1.70
CARGO ?= cargo
.PHONY: check-deps venv test-all clean install-tqc install-rewind install-theseus

check-deps:
	@echo "[A8] Checking system dependencies..."
	@command -v $(PYTHON) >/dev/null 2>&1 || (echo "ERROR: Python3 not found" && exit 1)
	@command -v rustc >/dev/null 2>&1 || (echo "ERROR: Rust toolchain not installed" && exit 1)
	@command -v $(CARGO) >/dev/null 2>&1 || (echo "ERROR: Cargo not found" && exit 1)
	@echo "✓ Python3: $$(python3 --version)"
	@echo "✓ Rustc: $$(rustc --version)"
	@echo "✓ Cargo: $$(cargo --version)"
	@echo "Dependency check PASSED."

venv:
	@echo "Creating isolated Python venv..."
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && python -m pip install --upgrade pip setuptools wheel
	@echo "Venv ready at $(VENV)"

install-tqc: venv
	@echo "[A1] Installing TQC demo dependencies..."
	. $(VENV)/bin/activate && pip install numpy scipy

install-rewind: check-deps
	@echo "[A2] Building reversible logic (Rust)..."
	$(CARGO) build --manifest-path tests/rewind/Cargo.toml --release

install-theseus:
	@echo "[A2.Lean4] Theseus Lean4 environment placeholder."
	@echo "Note: Lean 4 integration deferred to Phase 2."

test-all: check-deps
	@echo "[A8] Running full test suite..."
	@set -e; \
	$(PYTHON) -m py_compile src/tqc_demo.py && echo "✓ tqc_demo.py compiles"; \
	$(CARGO) test --manifest-path tests/rewind/Cargo.toml -- --nocapture && echo "✓ Reversible logic tests pass"; \
	$(PYTHON) src/tqc_demo.py && echo "✓ TQC demo executes"; \
	 echo "\n[A8] ALL TESTS PASSED - Pipeline green."

clean:
	@echo "Cleaning build artifacts..."
	rm -rf $(VENV) target/
	$(CARGO) clean --manifest-path tests/rewind/Cargo.toml 2>/dev/null || true
	@echo "Clean complete."
