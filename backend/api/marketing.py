from fastapi import APIRouter, HTTPException
from backend.models.schemas import AdCopyRequest, AdCopyResponse
from backend.services.marketing.ai_content import AIContentGenerator, AudienceTargeting

router = APIRouter()

@router.post("/generate-ad-copy", response_model=AdCopyResponse)
async def generate_ad_copy(request: AdCopyRequest):
    """Generate AI-powered ad copy"""
    generator = AIContentGenerator()
    
    ad_copy = await generator.generate_ad_copy(
        request.product_title,
        request.product_description,
        request.platform
    )
    
    return AdCopyResponse(
        headlines=ad_copy["headlines"],
        body_copy=ad_copy["body_copy"],
        call_to_actions=ad_copy["cta"],
        target_audiences=ad_copy["audiences"]
    )

@router.post("/generate-product-description")
async def generate_product_description(
    product_title: str,
    features: list[str],
    target_audience: str = "general"
):
    """Generate AI product description"""
    generator = AIContentGenerator()
    description = await generator.generate_product_description(
        product_title,
        features,
        target_audience
    )
    
    return {"description": description}

@router.post("/generate-video-script")
async def generate_video_script(
    product_title: str,
    key_benefits: list[str],
    duration: int = 30
):
    """Generate TikTok/Instagram video script"""
    generator = AIContentGenerator()
    script = await generator.generate_video_script(
        product_title,
        key_benefits,
        duration
    )
    
    return script

@router.post("/generate-email-sequence")
async def generate_email_sequence(product_title: str, customer_name: str = "[Name]"):
    """Generate email marketing sequence"""
    generator = AIContentGenerator()
    emails = await generator.generate_email_sequence(product_title, customer_name)
    
    return {"emails": emails}

@router.get("/identify-audience/{product_category}")
async def identify_audience(product_category: str, price_point: float):
    """Identify target audiences for a product"""
    targeting = AudienceTargeting()
    audiences = await targeting.identify_target_audience(product_category, price_point)
    
    return {"audiences": audiences}
