from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from google.cloud import translate_v2 as translate

# Initialize translation client
client = translate.Client.from_service_account_json("key.json")


def translate_text(text, target="hi"):
    result = client.translate(text, target_language=target)
    return result["translatedText"]


async def translate_api(request: Request):
    data = await request.json()

    text = data.get("text")
    target = data.get("target", "hi")

    translated = translate_text(text, target)

    return JSONResponse({
        "input": text,
        "target_language": target,
        "translated_text": translated
    })


routes = [
    Route("/translate", translate_api, methods=["POST"]),
]

app = Starlette(routes=routes)