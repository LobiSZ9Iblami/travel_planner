import httpx

from app.core.exceptions import ExternalAPIException

class ArtInstituteClient:

    BASE_URL = "https://api.artic.edu/api/v1"

    async def get_artwork_or_raise(self, external_id: str):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/artworks/{external_id}"
            )

        if response.status_code == 200:
            return True

        raise ExternalAPIException(
            status_code=response.status_code,
            detail=response.json()
        )

def get_art_institute_client():
    return ArtInstituteClient()
