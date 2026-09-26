from fastapi import APIRouter

router = APIRouter(prefix="/api/datasets", tags=["Datasets"])


@router.get("/")
async def list_datasets():
    return {
        "datasets": [
            {"id": "ruletaker", "name": "RuleTaker"},
            {"id": "proofwriter", "name": "ProofWriter"},
            {"id": "folio", "name": "FOLIO"},
            {"id": "custom", "name": "Custom Diagnostic Suite"}
        ]
    }
