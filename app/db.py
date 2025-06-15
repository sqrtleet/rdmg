from decimal import Decimal

from bson import Decimal128
from bson.codec_options import TypeCodec, CodecOptions, TypeRegistry
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.config import settings
from app.models import Defect


class DecimalCodec(TypeCodec):
    python_type = Decimal
    bson_type = Decimal128

    def transform_python(self, value: Decimal) -> Decimal128:
        return Decimal128(value)

    def transform_bson(self, value: Decimal128) -> Decimal:
        return value.to_decimal()


codec_options = CodecOptions(type_registry=TypeRegistry([DecimalCodec()]))


async def connect_to_mongo():
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client.get_database(settings.database_name, codec_options=codec_options)
    await init_beanie(database=db, document_models=[Defect])
