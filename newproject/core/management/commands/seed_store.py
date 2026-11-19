from django.core.management.base import BaseCommand
from core.models import Category, Product, Review
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seeds initial mug categories, products, and reviews'

    def handle(self, *args, **options):
        self.stdout.write("Seeding store with artisan mug products...")

        # Categories
        cat_artisanal, _ = Category.objects.get_or_create(
            slug='artisanal-ceramic',
            defaults={
                'name': 'Artisanal Ceramic',
                'description': 'Handcrafted stoneware mugs thrown on the wheel and kiln-fired with organic glazes.',
                'image_url': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80'
            }
        )

        cat_travel, _ = Category.objects.get_or_create(
            slug='travel-insulated',
            defaults={
                'name': 'Insulated Travel Mugs',
                'description': 'Vacuum insulated stainless steel mugs designed to keep your coffee piping hot for 8+ hours.',
                'image_url': 'https://images.unsplash.com/photo-1578357078586-491adf1aa5ba?auto=format&fit=crop&w=800&q=80'
            }
        )

        cat_campfire, _ = Category.objects.get_or_create(
            slug='vintage-enamel',
            defaults={
                'name': 'Vintage Enamel Campfire',
                'description': 'Ultra-durable, shatterproof enamel mugs ready for campfires, mountain hikes, and cozy mornings.',
                'image_url': 'https://images.unsplash.com/photo-1516762689617-e1cffcef479d?auto=format&fit=crop&w=800&q=80'
            }
        )

        cat_minimalist, _ = Category.objects.get_or_create(
            slug='minimalist-espresso',
            defaults={
                'name': 'Minimalist & Espresso',
                'description': 'Clean Scandinavian aesthetics, wide handles, and perfectly balanced ceramic rims.',
                'image_url': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=800&q=80'
            }
        )

        # Products
        products_data = [
            {
                'category': cat_artisanal,
                'name': 'Nordic Speckled Stoneware Mug',
                'slug': 'nordic-speckled-stoneware-mug',
                'tagline': 'Hand-thrown natural clay with speckled eggshell glaze',
                'description': 'Each Nordic Speckled Mug is individually shaped by hand from mineral-rich stoneware clay. Fired at 1250°C for exceptional durability and chip-resistance. Features a cozy thumb rest handle for a natural grip during your morning coffee ritual.',
                'price': Decimal('28.00'),
                'discount_price': Decimal('24.00'),
                'capacity': '380 ml (13 oz)',
                'material': 'High-fire Stoneware Clay',
                'dimensions': '9.8cm H x 8.5cm Dia',
                'color': 'Oatmeal & Raw Clay',
                'dishwasher_safe': True,
                'microwave_safe': True,
                'allow_custom_engraving': True,
                'image_url': 'https://images.unsplash.com/photo-1577937927133-66ef06acdf18?auto=format&fit=crop&w=800&q=80',
                'secondary_image_url': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80',
                'stock': 35,
                'is_featured': True,
                'is_bestseller': True,
                'rating': Decimal('4.95'),
                'reviews_count': 42,
            },
            {
                'category': cat_artisanal,
                'name': 'Charcoal Matte Pottery Mug',
                'slug': 'charcoal-matte-pottery-mug',
                'tagline': 'Bold volcanic black glaze with tactile satin texture',
                'description': 'Crafted for espresso connoisseurs and dark roast lovers. The volcanic charcoal matte finish feels warm and velvety in the hands, offering a tactile drinking experience. Lead-free, cadmium-free food-safe glaze.',
                'price': Decimal('32.00'),
                'discount_price': None,
                'capacity': '350 ml (12 oz)',
                'material': 'Dark Iron Stoneware',
                'dimensions': '9.2cm H x 8.0cm Dia',
                'color': 'Volcanic Charcoal Matte',
                'dishwasher_safe': True,
                'microwave_safe': True,
                'allow_custom_engraving': True,
                'image_url': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=800&q=80',
                'secondary_image_url': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80',
                'stock': 22,
                'is_featured': True,
                'is_bestseller': True,
                'rating': Decimal('4.88'),
                'reviews_count': 29,
            },
            {
                'category': cat_artisanal,
                'name': 'Terracotta Ribbed Barrel Mug',
                'slug': 'terracotta-ribbed-barrel-mug',
                'tagline': 'Fluted ribbed body for ergonomic hand warmth',
                'description': 'Inspired by Mediterranean pottery traditions. The fluted outer ribs keep the exterior cooler while letting gentle warmth radiate into your fingers. Finished with a contrasting milky cream glaze on the inside.',
                'price': Decimal('30.00'),
                'discount_price': Decimal('26.50'),
                'capacity': '420 ml (14.5 oz)',
                'material': 'Terracotta Ceramic with Satin Glaze',
                'dimensions': '10.5cm H x 9.0cm Dia',
                'color': 'Warm Terracotta / Cream',
                'dishwasher_safe': True,
                'microwave_safe': True,
                'allow_custom_engraving': True,
                'image_url': 'https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=800&q=80',
                'secondary_image_url': 'https://images.unsplash.com/photo-1572119865084-43c285814d63?auto=format&fit=crop&w=800&q=80',
                'stock': 18,
                'is_featured': True,
                'is_bestseller': False,
                'rating': Decimal('4.90'),
                'reviews_count': 16,
            },
            {
                'category': cat_travel,
                'name': 'Nomad Thermal Tumbler Mug',
                'slug': 'nomad-thermal-tumbler-mug',
                'tagline': 'Double-wall vacuum insulation with leak-proof flip lid',
                'description': 'Engineered for everyday commuters and weekend road trippers. Dual-wall 18/8 food-grade stainless steel with copper heat shield. Keeps beverages hot for 6 hours or ice-cold for 12 hours without condensation.',
                'price': Decimal('36.00'),
                'discount_price': Decimal('29.99'),
                'capacity': '450 ml (16 oz)',
                'material': '18/8 Stainless Steel & BPA-Free Lid',
                'dimensions': '14.0cm H x 8.5cm Dia',
                'color': 'Stealth Matte Black',
                'dishwasher_safe': False,
                'microwave_safe': False,
                'allow_custom_engraving': True,
                'image_url': 'https://images.unsplash.com/photo-1578357078586-491adf1aa5ba?auto=format&fit=crop&w=800&q=80',
                'secondary_image_url': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b675?auto=format&fit=crop&w=800&q=80',
                'stock': 40,
                'is_featured': True,
                'is_bestseller': True,
                'rating': Decimal('4.97'),
                'reviews_count': 54,
            },
            {
                'category': cat_campfire,
                'name': 'Pine Ridge Campfire Enamel Mug',
                'slug': 'pine-ridge-campfire-enamel-mug',
                'tagline': 'Steel core coated in porcelain enamel with stainless steel rim',
                'description': 'Built to survive rugged outdoor escapades. Whether placed directly over camp stove embers or enjoyed by the kitchen hearth, this lightweight enamel mug delivers timeless rustic charm.',
                'price': Decimal('22.00'),
                'discount_price': Decimal('18.50'),
                'capacity': '360 ml (12 oz)',
                'material': 'Heavy-gauge Steel with Porcelain Enamel',
                'dimensions': '8.5cm H x 9.0cm Dia',
                'color': 'Alpine White & Forest Green Rim',
                'dishwasher_safe': True,
                'microwave_safe': False,
                'allow_custom_engraving': False,
                'image_url': 'https://images.unsplash.com/photo-1516762689617-e1cffcef479d?auto=format&fit=crop&w=800&q=80',
                'secondary_image_url': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80',
                'stock': 50,
                'is_featured': False,
                'is_bestseller': True,
                'rating': Decimal('4.85'),
                'reviews_count': 38,
            },
            {
                'category': cat_minimalist,
                'name': 'Sage Green Studio Ceramic Cup',
                'slug': 'sage-green-studio-ceramic-cup',
                'tagline': 'Soft pastel green glaze with ergonomic curved rim',
                'description': 'Designed in collaboration with independent baristas. Perfectly tapered for latte art pouring and comfortable one-handed sipping. Matte exterior and glossy interior for easy cleaning.',
                'price': Decimal('26.00'),
                'discount_price': None,
                'capacity': '300 ml (10 oz)',
                'material': 'Porcelain Stoneware',
                'dimensions': '8.8cm H x 8.4cm Dia',
                'color': 'Earthy Sage Green',
                'dishwasher_safe': True,
                'microwave_safe': True,
                'allow_custom_engraving': True,
                'image_url': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=800&q=80',
                'secondary_image_url': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80',
                'stock': 28,
                'is_featured': True,
                'is_bestseller': False,
                'rating': Decimal('4.92'),
                'reviews_count': 21,
            },
            {
                'category': cat_minimalist,
                'name': 'Kyoto Clean Porcelain Coffee Mug',
                'slug': 'kyoto-clean-porcelain-coffee-mug',
                'tagline': 'Pure minimalist architecture with thin elegant rim',
                'description': 'Handcrafted pure white porcelain inspired by Japanese wabi-sabi philosophy. Feathery light yet astonishingly strong, offering an unfiltered pure taste with every brew.',
                'price': Decimal('24.00'),
                'discount_price': None,
                'capacity': '340 ml (11.5 oz)',
                'material': 'Bone-grade White Porcelain',
                'dimensions': '9.0cm H x 8.0cm Dia',
                'color': 'Silk White',
                'dishwasher_safe': True,
                'microwave_safe': True,
                'allow_custom_engraving': True,
                'image_url': 'https://images.unsplash.com/photo-1534040385115-33dcb3acba5b?auto=format&fit=crop&w=800&q=80',
                'secondary_image_url': 'https://images.unsplash.com/photo-1577937927133-66ef06acdf18?auto=format&fit=crop&w=800&q=80',
                'stock': 30,
                'is_featured': False,
                'is_bestseller': False,
                'rating': Decimal('4.78'),
                'reviews_count': 14,
            },
            {
                'category': cat_artisanal,
                'name': 'Dusk Indigo Ombre Mug',
                'slug': 'dusk-indigo-ombre-mug',
                'tagline': 'Gradient glaze transition from midnight navy to sandy clay',
                'description': 'Dip-glazed by hand to create a mesmerizing horizon line reminiscent of dusk falling over the mountains. The exposed raw clay base provides grounding texture while the polished upper keeps sipping velvety smooth.',
                'price': Decimal('34.00'),
                'discount_price': Decimal('29.00'),
                'capacity': '400 ml (13.5 oz)',
                'material': 'Heavy Stoneware',
                'dimensions': '10.0cm H x 8.8cm Dia',
                'color': 'Indigo Gradient & Raw Sand',
                'dishwasher_safe': True,
                'microwave_safe': True,
                'allow_custom_engraving': True,
                'image_url': 'https://images.unsplash.com/photo-1521449256184-170b4a4c437c?auto=format&fit=crop&w=800&q=80',
                'secondary_image_url': 'https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=800&q=80',
                'stock': 15,
                'is_featured': True,
                'is_bestseller': False,
                'rating': Decimal('4.98'),
                'reviews_count': 25,
            }
        ]

        for p_data in products_data:
            slug = p_data.pop('slug')
            product, created = Product.objects.update_or_create(slug=slug, defaults=p_data)
            action = "Created" if created else "Updated"
            self.stdout.write(f"  {action} product: {product.name}")

            # Add sample reviews
            if created or not product.reviews.exists():
                Review.objects.create(
                    product=product,
                    user_name='Elena Vasquez',
                    rating=5,
                    comment='The craftsmanship is breathtaking! It feels so substantial and warm in my hands every single morning.'
                )
                Review.objects.create(
                    product=product,
                    user_name='Marcus Chen',
                    rating=5,
                    comment='Quick shipping, arrived safely packed in biodegradable paper wrap. The glaze looks even better in person!'
                )

        self.stdout.write(self.style.SUCCESS("Successfully seeded store with categories, products, and reviews!"))
