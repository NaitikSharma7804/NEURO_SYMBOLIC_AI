import pytest
from backend.formalization.validator import RepresentationValidator
from backend.formalization.compiler import PrologCompiler
from backend.models.logic import LogicSchema, FactModel, RuleModel, PredicateModel


def test_validator_accepts_valid_schema():
    validator = RepresentationValidator()
    valid_data = {
        "facts": [{"predicate": "human", "arguments": ["socrates"], "is_negated": False}],
        "rules": [
            {
                "variables": ["X"],
                "body": [{"predicate": "human", "arguments": ["X"], "is_negated": False}],
                "head": {"predicate": "mortal", "arguments": ["X"], "is_negated": False}
            }
        ],
        "query": {"predicate": "mortal", "arguments": ["socrates"], "is_negated": False}
    }
    result = validator.validate(valid_data)
    assert result.valid is True
    assert len(result.errors) == 0


def test_validator_rejects_undefined_variable_in_head():
    validator = RepresentationValidator()
    invalid_data = {
        "facts": [{"predicate": "human", "arguments": ["socrates"], "is_negated": False}],
        "rules": [
            {
                "variables": ["X", "Y"],
                "body": [{"predicate": "human", "arguments": ["X"], "is_negated": False}],
                "head": {"predicate": "mortal", "arguments": ["Y"], "is_negated": False}
            }
        ],
        "query": {"predicate": "mortal", "arguments": ["socrates"], "is_negated": False}
    }
    result = validator.validate(invalid_data)
    assert result.valid is False
    codes = [e.code for e in result.errors]
    assert "UNDEFINED_VARIABLE" in codes


def test_validator_detects_inconsistent_arity():
    validator = RepresentationValidator()
    # Predicate 'parent' used with 1 arg in fact, but 2 args in query
    inconsistent_data = {
        "facts": [
            {"predicate": "parent", "arguments": ["john"], "is_negated": False}
        ],
        "rules": [],
        "query": {"predicate": "parent", "arguments": ["john", "mary"], "is_negated": False}
    }
    result = validator.validate(inconsistent_data)
    assert result.valid is False
    codes = [e.code for e in result.errors]
    assert "INCONSISTENT_ARITY" in codes


def test_prolog_compiler_output():
    compiler = PrologCompiler()
    schema = LogicSchema(
        facts=[FactModel(predicate="human", arguments=["socrates"])],
        rules=[
            RuleModel(
                variables=["X"],
                body=[PredicateModel(predicate="human", arguments=["X"])],
                head=PredicateModel(predicate="mortal", arguments=["X"])
            )
        ],
        query=PredicateModel(predicate="mortal", arguments=["socrates"])
    )
    prolog_code = compiler.compile_schema(schema)
    assert "human('socrates')." in prolog_code
    assert "mortal(X) :- human(X)." in prolog_code

    pos_goal, neg_goal = compiler.compile_query_goals(schema.query)
    assert pos_goal == "mortal('socrates')"
    assert neg_goal == "not_mortal('socrates')"
