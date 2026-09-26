import shutil
import subprocess
import tempfile
import os
from typing import Tuple, Dict, Any, Optional
from backend.models.logic import LogicSchema, ReasoningResultEnum
from backend.models.proof import ProofGraph
from backend.models.schemas import ContradictionAnalysis
from backend.reasoning.base import ReasoningBackend
from backend.reasoning.engine import DeterministicSymbolicEngine
from backend.formalization.compiler import PrologCompiler
from backend.config.settings import settings


class SWIPrologBackend(ReasoningBackend):
    """Reasoning backend utilizing SWI-Prolog subprocess with fallback to DeterministicSymbolicEngine."""

    def __init__(self, prolog_path: Optional[str] = None):
        self.prolog_path = prolog_path or settings.PROLOG_PATH or shutil.which("swipl")
        self.compiler = PrologCompiler()
        self.fallback_engine = DeterministicSymbolicEngine()

    def is_available(self) -> bool:
        """Check if SWI-Prolog executable is found on system."""
        if not self.prolog_path:
            return False
        try:
            res = subprocess.run(
                [self.prolog_path, "--version"],
                capture_output=True,
                text=True,
                timeout=2.0
            )
            return res.returncode == 0
        except Exception:
            return False

    def validate(self) -> bool:
        """Validate whether backend is operational."""
        if self.is_available():
            return True
        return self.fallback_engine.validate()

    def reason(self, schema: LogicSchema) -> Tuple[ReasoningResultEnum, ProofGraph, Dict[str, Any]]:
        # If SWI-Prolog is not locally installed on the host, use the validated pure symbolic engine
        if not self.is_available():
            result, proof, meta = self.fallback_engine.reason(schema)
            meta["backend"] = "swi_prolog_simulated_pure"
            meta["swipl_available"] = False
            return result, proof, meta

        prolog_kb_content = self.compiler.compile_schema(schema)
        pos_goal, neg_goal = self.compiler.compile_query_goals(schema.query)

        # Build runner script
        driver_script = f"""
{prolog_kb_content}

check_both :-
    ( {pos_goal} -> Pos = true ; Pos = false ),
    ( {neg_goal} -> Neg = true ; Neg = false ),
    format('RESULT: POS=~w NEG=~w~n', [Pos, Neg]),
    halt.

:- initialization(check_both, main).
"""
        with tempfile.NamedTemporaryFile("w", suffix=".pl", delete=False) as tf:
            tf.write(driver_script)
            tf_path = tf.name

        try:
            cmd = [self.prolog_path, "-q", "-s", tf_path]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=settings.DEFAULT_TIMEOUT_SECONDS)
            output = proc.stdout

            pos_provable = "POS=true" in output
            neg_provable = "NEG=true" in output

            # Determine classification
            if pos_provable and neg_provable:
                result = ReasoningResultEnum.CONTRADICTED
                conflict = True
            elif pos_provable and not neg_provable:
                result = ReasoningResultEnum.ENTAILED
                conflict = False
            elif not pos_provable and neg_provable:
                result = ReasoningResultEnum.CONTRADICTED
                conflict = False
            else:
                result = ReasoningResultEnum.UNKNOWN
                conflict = False

            # Use proof generator from fallback engine to produce structured DAG proof
            _, proof, _ = self.fallback_engine.reason(schema)

            analysis = ContradictionAnalysis(
                query_status=result,
                query_provable=pos_provable,
                opposite_provable=neg_provable,
                conflict_detected=conflict,
                query_proof=proof if pos_provable else None,
                opposite_proof=proof if neg_provable else None
            )

            metadata = {
                "backend": "swi_prolog_native",
                "swipl_available": True,
                "contradiction": analysis,
                "raw_prolog_output": output.strip()
            }

            return result, proof, metadata

        except Exception as e:
            # Fallback on any execution error
            result, proof, meta = self.fallback_engine.reason(schema)
            meta["backend"] = "swi_prolog_fallback_error"
            meta["prolog_error"] = str(e)
            return result, proof, meta

        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)
