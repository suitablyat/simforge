from .schemas import SimJobRequest, SimJobResult
from .simc_runner import run_simc, SimcError

def run_sim_job(payload: dict) -> dict:
    req = SimJobRequest(**payload)
    try:
        data = run_simc(req.input_text)
        return SimJobResult(ok=True, data=data).model_dump()
    except SimcError as e:
        return SimJobResult(ok=False, error=str(e)).model_dump()
