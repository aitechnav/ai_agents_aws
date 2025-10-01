from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# create a MCP server
mcp = FastMCP("restaurant-menu-mcp")

class MenuItem(BaseModel):
    """Menu item structure"""
    
    price: float = Field(description="Price in USD")
    cuisine: str = Field(description="Cuisine type")
    calories: int = Field(description="Calorie count")
    spicy_level: int = Field(description="Spiciness level 0-5")
    ingredients: list[str] = Field(description="Main ingredients")

# restaurant menu database
menu_db: dict[str, MenuItem] = {
    "Margherita Pizza": MenuItem(price=12.99, cuisine="Italian", calories=800, spicy_level=0, ingredients=["mozzarella", "tomato", "basil"]),
    "Chicken Tikka": MenuItem(price=15.99, cuisine="Indian", calories=650, spicy_level=3, ingredients=["chicken", "yogurt", "spices"]),
    "Sushi Roll": MenuItem(price=18.99, cuisine="Japanese", calories=450, spicy_level=1, ingredients=["rice", "salmon", "nori"]),
    "Pad Thai": MenuItem(price=13.99, cuisine="Thai", calories=700, spicy_level=2, ingredients=["noodles", "shrimp", "peanuts"]),
    "Caesar Salad": MenuItem(price=10.99, cuisine="American", calories=350, spicy_level=0, ingredients=["lettuce", "parmesan", "croutons"]),
}

# return menu item tool with fuzzy matching
@mcp.tool()
def get_menu_item(dish_name: str) -> MenuItem:
    """Get menu item details for a dish name. Supports partial matching (e.g., 'pizza' will find 'Margherita Pizza')."""
    
    # First try exact match
    if dish_name in menu_db:
        return menu_db[dish_name]
    
    # Try case-insensitive exact match
    for key in menu_db.keys():
        if key.lower() == dish_name.lower():
            return menu_db[key]
    
    # Try partial match (if dish_name is contained in any menu item)
    dish_name_lower = dish_name.lower()
    matches = []
    for key in menu_db.keys():
        if dish_name_lower in key.lower():
            matches.append(key)
    
    if len(matches) == 1:
        return menu_db[matches[0]]
    elif len(matches) > 1:
        raise ValueError(f"Multiple dishes found matching '{dish_name}': {', '.join(matches)}. Please be more specific.")
    
    # No matches found
    available_dishes = ", ".join(menu_db.keys())
    raise ValueError(f"Dish '{dish_name}' not found in menu. Available dishes: {available_dishes}")

if __name__ == "__main__":
    mcp.run(transport="stdio")