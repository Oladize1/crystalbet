from models.main import AZMenuModel, QuickLinksModel
from schemas.main import AZMenuSchema, QuickLinksSchema
from typing import List
from db.mongodb import init_db, get_collection


# Create the MainService instance after database initialization


class MainService:
    def __init__(self):
        self.az_menu_collection = get_collection("az_menu")  # Assuming get_collection is a function
        self.quick_links_collection = get_collection("quick_links")

    async def get_az_menu(self) -> List[AZMenuModel]:
        az_menu_items = await self.az_menu_collection.find().to_list(100)
        return [AZMenuModel(**item) for item in az_menu_items]

    async def get_quick_links(self) -> List[QuickLinksModel]:
        quick_links_items = await self.quick_links_collection.find().to_list(100)
        return [QuickLinksModel(**item) for item in quick_links_items]

    async def add_az_menu_item(self, item: AZMenuSchema) -> AZMenuModel:
        new_item = AZMenuModel(**item.dict())
        result = await self.az_menu_collection.insert_one(new_item.dict())
        new_item.id = str(result.inserted_id)  # Ensure id is a string
        return new_item

    async def add_quick_link(self, item: QuickLinksSchema) -> QuickLinksModel:
        new_item = QuickLinksModel(**item.dict())
        result = await self.quick_links_collection.insert_one(new_item.dict())
        new_item.id = str(result.inserted_id)  # Ensure id is a string
        return new_item
