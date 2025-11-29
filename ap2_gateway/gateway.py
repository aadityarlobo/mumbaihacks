from fastapi import FastAPI, HTTPException, BackgroundTasks
from ap2_gateway.models import PaymentRequest, PaymentResponse
from ap2_gateway.processor import processor
from ap2_gateway.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AP2 Payment Gateway",
    description="A mock implementation of the Agent-to-Payment (AP2) protocol.",
    version="1.0.0"
)

@app.post("/api/payments", response_model=PaymentResponse)
async def initiate_payment(request: PaymentRequest, background_tasks: BackgroundTasks):
    """
    Initiates a payment request from an agent.
    """
    try:
        logger.info(f"Received payment request: {request.request_id}")
        response = await processor.initiate_payment(request)
        return response
    except ValueError as e:
        logger.error(f"Validation error for request {request.request_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Internal server error for request {request.request_id}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/status/{transaction_id}")
async def get_payment_status(transaction_id: str):
    """
    Retrieves the status of a payment transaction.
    """
    logger.info(f"Fetching status for transaction: {transaction_id}")
    status = processor.get_transaction_status(transaction_id)
    if status:
        return status
    else:
        logger.warning(f"Transaction not found: {transaction_id}")
        raise HTTPException(status_code=404, detail="Transaction not found")

@app.get("/")
def read_root():
    return {"message": "AP2 Payment Gateway is running."}

if __name__ == "__main__":
    import uvicorn
    from ap2_gateway.config import config
    uvicorn.run(app, host="0.0.0.0", port=config.GATEWAY_PORT)
