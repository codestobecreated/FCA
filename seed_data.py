import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fca_project.settings')
django.setup()

from shop.models import Category, Product

def seed():
    # Create Categories
    categories_data = [
        {'name': 'Exterior', 'slug': 'exterior', 'desc': 'Enhance your car\'s outer look and performance.'},
        {'name': 'Interior', 'slug': 'interior', 'desc': 'Premium comfort and style for your cabin.'},
        {'name': 'Performance', 'slug': 'performance', 'desc': 'Boost your engine and handling capabilities.'},
        {'name': 'Lighting', 'slug': 'lighting', 'desc': 'Advanced LED and HID lighting solutions.'},
        {'name': 'Wheels & Tires', 'slug': 'wheels-tires', 'desc': 'High-performance alloys and durable tires.'},
    ]

    categories = {}
    for cat in categories_data:
        c, created = Category.objects.get_or_create(name=cat['name'], slug=cat['slug'], defaults={'description': cat['desc']})
        categories[cat['slug']] = c

    # Create Products
    products_data = [
        # Exterior
        {
            'cat': 'exterior',
            'name': 'Carbon Fiber Spoiler',
            'slug': 'carbon-fiber-spoiler',
            'desc': 'Premium lightweight carbon fiber spoiler for enhanced aerodynamics and aggressive looks.',
            'price': 299.99,
            'stock': 10,
            'image': 'products/aero.png'
        },
        {
            'cat': 'exterior',
            'name': 'Matte Black Front Grille',
            'slug': 'matte-black-grille',
            'desc': 'Sleek matte black finish front grille for a stealthy look.',
            'price': 145.00,
            'stock': 15
        },
        # Interior
        {
            'cat': 'interior',
            'name': 'Alcantara Steering Wheel Cover',
            'slug': 'alcantara-cover',
            'desc': 'Premium Alcantara cover for a luxurious grip and sportier feel.',
            'price': 89.99,
            'stock': 25,
            'image': 'products/steering.png'
        },
        {
            'cat': 'interior',
            'name': 'Custom Floor Mats',
            'slug': 'custom-floor-mats',
            'desc': 'All-weather durable floor mats custom-fitted for maximum protection.',
            'price': 120.00,
            'stock': 40
        },
        # Lighting
        {
            'cat': 'lighting',
            'name': 'LED Ambient Lighting Kit',
            'slug': 'led-ambient-lighting',
            'desc': 'Customizable interior LED lighting with smartphone app control.',
            'price': 49.99,
            'stock': 50
        },
        {
            'cat': 'lighting',
            'name': 'Matrix LED Headlights',
            'slug': 'matrix-led-headlights',
            'desc': 'Ultra-bright matrix LED headlights with adaptive beam technology.',
            'price': 850.00,
            'stock': 8,
            'image': 'products/lighting.png'
        },
        # Performance
        {
            'cat': 'performance',
            'name': 'Cold Air Intake System',
            'slug': 'cold-air-intake',
            'desc': 'High-flow air intake system for improved horsepower and engine sound.',
            'price': 189.50,
            'stock': 5
        },
        {
            'cat': 'performance',
            'name': 'Stage 2 ECU Tune',
            'slug': 'ecu-tune-stage2',
            'desc': 'Professional ECU remapping for significant power gains and optimization.',
            'price': 450.00,
            'stock': 100
        },
        # Wheels & Tires
        {
            'cat': 'wheels-tires',
            'name': '20" Forged Alloy Wheels',
            'slug': '20-forged-wheels',
            'desc': 'Ultra-light forged alloy wheels for superior strength and style.',
            'price': 1200.00,
            'stock': 4,
            'image': 'products/wheels.png'
        },
    ]

    for prod in products_data:
        Product.objects.update_or_create(
            slug=prod['slug'],
            defaults={
                'category': categories[prod['cat']],
                'name': prod['name'],
                'description': prod['desc'],
                'price': prod['price'],
                'stock': prod['stock'],
                'image': prod.get('image', ''),
                'available': True
            }
        )

    print(f"Sample data seeded successfully! {len(products_data)} products total.")

if __name__ == "__main__":
    seed()
