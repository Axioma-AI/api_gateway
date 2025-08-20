from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class CreateSubscriptionRequest(BaseModel):
    product_id: str = Field(..., description="Product ID from the store")
    platform: str = Field(..., description="Platform (google_play, apple)")
    receipt_data: Optional[Dict[str, Any]] = Field(None, description="Receipt data from store")
    auto_renew: bool = Field(True, description="Auto-renew subscription")