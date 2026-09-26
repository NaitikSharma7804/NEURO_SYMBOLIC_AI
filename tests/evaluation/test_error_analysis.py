import pytest
from backend.experiments.error_analyzer import AutomatedErrorAnalyzer, ErrorCategoryEnum


def test_error_analyzer_taxonomy_report():
    analyzer = AutomatedErrorAnalyzer()
    report = analyzer.get_taxonomy_report()
    
    assert report.total_evaluated == 10
    assert report.total_errors == 10
    
    # Check that all 10 error categories are present in the report
    for cat in ErrorCategoryEnum:
        assert cat.value in report.cases_by_category
        cases = report.cases_by_category[cat.value]
        assert len(cases) >= 1
        assert cases[0].category == cat
        assert cases[0].root_cause != ""
        assert cases[0].remediation != ""
