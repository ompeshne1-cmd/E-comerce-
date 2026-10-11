from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = "Seed initial Hedlum soft drink products"

    def handle(self, *args, **options):
        # Create categories
        cat_craft, _ = Category.objects.get_or_create(
            name="Craft Soft Drinks",
            defaults={"description": "Artisanal non-alcoholic brew-style beverages crafted with botanical extracts."}
        )
        cat_soda, _ = Category.objects.get_or_create(
            name="Sparkling Infusions",
            defaults={"description": "Crisp effervescent fruit fusions with zero sugar."}
        )

        products_data = [
            {
                "name": "HEDLUM EASY DOWN",
                "tagline": "Brewed to be Wild • Non-Alcoholic Brew",
                "hero_headline": "LOREM IPSUM CONSECTETUR DOLOR SIT CONSECT.",
                "category": cat_craft,
                "price": 14.99,
                "original_price": 18.00,
                "description": "Lager-style easy down craft soda. Engineered with slow-roasted toasted barley essence, crisp cascade hops notes, and pure sparkling mountain water. 100% alcohol-free refreshment that hits the spot anytime.",
                "flavor_notes": "Golden malt aroma, toasted biscuit sweetness, crisp effervescence, clean dry finish",
                "alcohol_vol": "<0.5% NON-ALCOHOLIC",
                "volume": "12 FL. OZ. (355 ML)",
                "calories": "15 CAL",
                "sugar": "0g SUGAR",
                "primary_color": "#E5A812",
                "image_url": "/static/shop/images/hedlum_can_original.png",
                "is_featured": True,
                "rating": 4.9,
                "review_count": 218,
            },
            {
                "name": "HEDLUM WILD BERRY CRUSH",
                "tagline": "Wild Forest Berries • Natural Sparkling Rush",
                "hero_headline": "BURSTING WITH DARK FOREST BERRY ESSENCE.",
                "category": cat_soda,
                "price": 15.99,
                "original_price": 19.50,
                "description": "Infused with crushed Pacific Northwest blackberries, mountain raspberries, and elderberry botanicals. Rich ruby brilliance with a punchy sweet-tart balance.",
                "flavor_notes": "Sun-ripened blackberries, wild raspberry tartness, hints of vanilla vine",
                "alcohol_vol": "0.0% ZERO ALCOHOL",
                "volume": "12 FL. OZ. (355 ML)",
                "calories": "12 CAL",
                "sugar": "0g SUGAR",
                "primary_color": "#E11D48",
                "image_url": "/static/shop/images/hedlum_can_berry.png",
                "is_featured": False,
                "rating": 4.8,
                "review_count": 145,
            },
            {
                "name": "HEDLUM CITRUS LIME SURGE",
                "tagline": "Cold-Pressed Key Lime & Mountain Botanicals",
                "hero_headline": "HIGH VOLTAGE CRISP CITRUS CRAFT SODA.",
                "category": cat_soda,
                "price": 14.99,
                "original_price": 17.50,
                "description": "Electric citrus punch made with cold-pressed Key lime oils, Meyer lemon peel, and sparkling mineral water. Ultra-crisp, thirst-quenching, and revitalizing.",
                "flavor_notes": "Zesty key lime zing, lemon zest fizz, botanical herbal undertone",
                "alcohol_vol": "0.0% ZERO ALCOHOL",
                "volume": "12 FL. OZ. (355 ML)",
                "calories": "10 CAL",
                "sugar": "0g SUGAR",
                "primary_color": "#10B981",
                "image_url": "/static/shop/images/hedlum_can_lime.png",
                "is_featured": False,
                "rating": 4.9,
                "review_count": 182,
            },
            {
                "name": "HEDLUM BLUE GLACIER RAZZ",
                "tagline": "Arctic Glacier Chill • Blue Agave Infusion",
                "hero_headline": "ARCTIC MOUNTAIN CHILL CRAFT BEVERAGE.",
                "category": cat_soda,
                "price": 15.49,
                "original_price": 18.99,
                "description": "Sub-zero freshness with glacier blueberries, touch of blue agave nectar, and crisp carbonation. Vibrant electric azure hue with a smooth, cooling finish.",
                "flavor_notes": "Glacier wild blueberries, hint of sweet agave, ice mint cooling finish",
                "alcohol_vol": "0.0% ZERO ALCOHOL",
                "volume": "12 FL. OZ. (355 ML)",
                "calories": "14 CAL",
                "sugar": "0g SUGAR",
                "primary_color": "#0284C7",
                "image_url": "/static/shop/images/hedlum_can_blue.png",
                "is_featured": False,
                "rating": 4.7,
                "review_count": 94,
            },
        ]

        for p_data in products_data:
            prod, created = Product.objects.update_or_create(
                name=p_data["name"],
                defaults=p_data
            )
            status_str = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{status_str} product: {prod.name}"))

        self.stdout.write(self.style.SUCCESS("All Hedlum products successfully seeded!"))
