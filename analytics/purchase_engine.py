#!/usr/bin/env python3
"""
Purchase Engine
Motor de compras con filtrado, ordenamiento y recomendaciones
"""

import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

class SortBy(Enum):
    PRICE_LOW = "price_low"
    PRICE_HIGH = "price_high"
    POPULARITY = "popularity"
    RATING = "rating"
    NEWEST = "newest"
    DISCOUNT = "discount"

@dataclass
class FilterCriteria:
    """Criterios de filtrado para productos"""
    categories: Optional[List[str]] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None
    in_stock_only: bool = True
    min_stock: Optional[int] = None
    currencies: Optional[List[str]] = None
    suppliers: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    sizes: Optional[List[str]] = None
    payment_methods: Optional[List[str]] = None

class PurchaseEngine:
    """Motor de compras y recomendaciones"""
    
    def __init__(self, products_data: List[Dict[str, Any]]):
        self.products = products_data
        self.filtered_products = products_data.copy()
    
    def load_from_file(self, filepath: str):
        """Cargar datos desde archivo JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.products = data.get('products', [])
            self.filtered_products = self.products.copy()
    
    def apply_filters(self, criteria: FilterCriteria) -> List[Dict[str, Any]]:
        """Aplicar filtros a los productos"""
        filtered = self.products.copy()
        
        # Filtro por categoría
        if criteria.categories:
            filtered = [p for p in filtered 
                       if p['category']['primary'] in criteria.categories or
                       any(cat in p['category'].get('secondary', []) for cat in criteria.categories)]
        
        # Filtro por precio
        if criteria.min_price is not None:
            filtered = [p for p in filtered if p['price']['current'] >= criteria.min_price]
        
        if criteria.max_price is not None:
            filtered = [p for p in filtered if p['price']['current'] <= criteria.max_price]
        
        # Filtro por rating
        if criteria.min_rating is not None:
            filtered = [p for p in filtered 
                       if p.get('analytics', {}).get('average_rating', 0) >= criteria.min_rating]
        
        # Filtro por disponibilidad
        if criteria.in_stock_only:
            filtered = [p for p in filtered if p['availability']['in_stock']]
        
        if criteria.min_stock is not None:
            filtered = [p for p in filtered 
                       if p['availability'].get('stock_quantity', 0) >= criteria.min_stock]
        
        # Filtro por moneda
        if criteria.currencies:
            filtered = [p for p in filtered if p['price']['currency'] in criteria.currencies]
        
        # Filtro por proveedor
        if criteria.suppliers:
            filtered = [p for p in filtered 
                       if p.get('supplier', {}).get('name') in criteria.suppliers]
        
        # Filtro por tags
        if criteria.tags:
            filtered = [p for p in filtered 
                       if any(tag in p.get('metadata', {}).get('tags', []) for tag in criteria.tags)]
        
        # Filtro por colores
        if criteria.colors:
            filtered = [p for p in filtered 
                       if any(color in p.get('specifications', {}).get('color', []) for color in criteria.colors)]
        
        # Filtro por tallas
        if criteria.sizes:
            filtered = [p for p in filtered 
                       if any(size in p.get('specifications', {}).get('size', []) for size in criteria.sizes)]
        
        # Filtro por métodos de pago
        if criteria.payment_methods:
            filtered = [p for p in filtered 
                       if any(method in p.get('purchase_attributes', {}).get('payment_options', []) 
                             for method in criteria.payment_methods)]
        
        self.filtered_products = filtered
        return filtered
    
    def sort_products(self, sort_by: SortBy, ascending: bool = True) -> List[Dict[str, Any]]:
        """Ordenar productos según criterio especificado"""
        def get_sort_key(product: Dict[str, Any]) -> Any:
            if sort_by == SortBy.PRICE_LOW or sort_by == SortBy.PRICE_HIGH:
                return product['price']['current']
            elif sort_by == SortBy.POPULARITY:
                return product.get('analytics', {}).get('popularity_score', 0)
            elif sort_by == SortBy.RATING:
                return product.get('analytics', {}).get('average_rating', 0)
            elif sort_by == SortBy.NEWEST:
                return product.get('metadata', {}).get('created_at', '')
            elif sort_by == SortBy.DISCOUNT:
                return product['price'].get('discount_percentage', 0)
            return 0
        
        reverse_order = not ascending
        if sort_by == SortBy.PRICE_HIGH:
            reverse_order = True
        elif sort_by in [SortBy.POPULARITY, SortBy.RATING, SortBy.DISCOUNT]:
            reverse_order = True
        
        self.filtered_products.sort(key=get_sort_key, reverse=reverse_order)
        return self.filtered_products
    
    def get_recommendations(self, product_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Obtener recomendaciones basadas en un producto"""
        target_product = None
        for product in self.products:
            if product['id'] == product_id:
                target_product = product
                break
        
        if not target_product:
            return []
        
        recommendations = []
        target_category = target_product['category']['primary']
        target_price = target_product['price']['current']
        
        for product in self.products:
            if product['id'] == product_id:
                continue
            
            score = 0
            
            # Misma categoría principal (+30 pts)
            if product['category']['primary'] == target_category:
                score += 30
            
            # Categorías secundarias coincidentes (+10 pts cada una)
            target_secondary = set(target_product['category'].get('secondary', []))
            product_secondary = set(product['category'].get('secondary', []))
            score += len(target_secondary.intersection(product_secondary)) * 10
            
            # Rango de precio similar (+20 pts si está dentro del 50% del precio)
            price_diff = abs(product['price']['current'] - target_price) / target_price
            if price_diff <= 0.5:
                score += 20 - (price_diff * 20)
            
            # Tags coincidentes (+5 pts cada uno)
            target_tags = set(target_product.get('metadata', {}).get('tags', []))
            product_tags = set(product.get('metadata', {}).get('tags', []))
            score += len(target_tags.intersection(product_tags)) * 5
            
            # Rating alto (+score basado en rating)
            rating = product.get('analytics', {}).get('average_rating', 0)
            score += rating * 2
            
            # Popularidad (+score basado en popularidad)
            popularity = product.get('analytics', {}).get('popularity_score', 0)
            score += popularity * 0.1
            
            recommendations.append({
                'product': product,
                'score': score
            })
        
        # Ordenar por score y retornar solo los productos
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return [rec['product'] for rec in recommendations[:limit]]
    
    def calculate_bulk_savings(self, product_id: str, quantity: int) -> Dict[str, Any]:
        """Calcular ahorros por compra en volumen"""
        product = None
        for p in self.products:
            if p['id'] == product_id:
                product = p
                break
        
        if not product:
            return {'error': 'Producto no encontrado'}
        
        base_price = product['price']['current']
        bulk_tiers = product.get('purchase_attributes', {}).get('bulk_discount_tiers', [])
        
        if not bulk_tiers:
            return {
                'total_price': base_price * quantity,
                'savings': 0,
                'discount_percentage': 0,
                'applicable_tier': None
            }
        
        # Encontrar el tier aplicable
        applicable_tier = None
        for tier in sorted(bulk_tiers, key=lambda x: x['min_quantity'], reverse=True):
            if quantity >= tier['min_quantity']:
                applicable_tier = tier
                break
        
        if applicable_tier:
            discount_percentage = applicable_tier['discount_percentage']
            discounted_price = base_price * (1 - discount_percentage / 100)
            total_price = discounted_price * quantity
            savings = (base_price * quantity) - total_price
        else:
            discount_percentage = 0
            total_price = base_price * quantity
            savings = 0
        
        return {
            'base_price_per_unit': base_price,
            'discounted_price_per_unit': base_price * (1 - discount_percentage / 100) if discount_percentage > 0 else base_price,
            'quantity': quantity,
            'total_price': total_price,
            'savings': savings,
            'discount_percentage': discount_percentage,
            'applicable_tier': applicable_tier
        }
    
    def get_product_by_budget(self, budget: float, currency: str = "USD") -> List[Dict[str, Any]]:
        """Obtener productos dentro de un presupuesto"""
        criteria = FilterCriteria(
            max_price=budget,
            currencies=[currency],
            in_stock_only=True
        )
        
        filtered = self.apply_filters(criteria)
        
        # Ordenar por mejor valor (rating/precio)
        for product in filtered:
            rating = product.get('analytics', {}).get('average_rating', 0)
            price = product['price']['current']
            product['_value_score'] = (rating / price) * 1000 if price > 0 else 0
        
        filtered.sort(key=lambda x: x['_value_score'], reverse=True)
        
        # Remover el score temporal
        for product in filtered:
            product.pop('_value_score', None)
        
        return filtered
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Buscar productos por texto"""
        query_lower = query.lower()
        results = []
        
        for product in self.products:
            score = 0
            
            # Búsqueda en nombre (peso alto)
            if query_lower in product['name'].lower():
                score += 50
            
            # Búsqueda en descripción
            if 'description' in product and query_lower in product['description'].lower():
                score += 20
            
            # Búsqueda en categorías
            if query_lower in product['category']['primary'].lower():
                score += 30
            
            for secondary in product['category'].get('secondary', []):
                if query_lower in secondary.lower():
                    score += 15
            
            # Búsqueda en tags
            for tag in product.get('metadata', {}).get('tags', []):
                if query_lower in tag.lower():
                    score += 10
            
            # Búsqueda en especificaciones
            specs = product.get('specifications', {})
            if 'material' in specs and query_lower in specs['material'].lower():
                score += 10
            
            if 'color' in specs:
                for color in specs['color']:
                    if query_lower in color.lower():
                        score += 8
            
            if score > 0:
                results.append({
                    'product': product,
                    'relevance_score': score
                })
        
        # Ordenar por relevancia
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return [result['product'] for result in results]

def main():
    """Función principal de demostración"""
    # Cargar datos
    engine = PurchaseEngine([])
    engine.load_from_file('../data/sample_products.json')
    
    print("🛒 Motor de Compras - Demostración")
    print("=" * 50)
    
    # Ejemplo 1: Filtrar productos por categoría y precio
    print("\n📱 Productos de Electrónicos bajo $500:")
    criteria = FilterCriteria(
        categories=["Electrónicos"],
        max_price=500
    )
    filtered = engine.apply_filters(criteria)
    for product in filtered:
        print(f"- {product['name']}: ${product['price']['current']}")
    
    # Ejemplo 2: Recomendaciones
    print("\n🎯 Recomendaciones para Smartphone Pro Max:")
    recommendations = engine.get_recommendations("PROD-001", limit=3)
    for i, product in enumerate(recommendations, 1):
        print(f"{i}. {product['name']} - ${product['price']['current']}")
    
    # Ejemplo 3: Cálculo de descuentos por volumen
    print("\n💰 Descuento por volumen (10 unidades de Smartphone):")
    bulk_info = engine.calculate_bulk_savings("PROD-001", 10)
    if 'error' not in bulk_info:
        print(f"Precio total: ${bulk_info['total_price']:.2f}")
        print(f"Ahorro: ${bulk_info['savings']:.2f} ({bulk_info['discount_percentage']}% descuento)")
    
    # Ejemplo 4: Productos por presupuesto
    print("\n💵 Mejores productos con presupuesto de $300:")
    budget_products = engine.get_product_by_budget(300)
    for product in budget_products[:3]:
        rating = product.get('analytics', {}).get('average_rating', 0)
        print(f"- {product['name']}: ${product['price']['current']} (Rating: {rating})")
    
    # Ejemplo 5: Búsqueda de texto
    print("\n🔍 Búsqueda: 'wireless':")
    search_results = engine.search_products("wireless")
    for product in search_results[:3]:
        print(f"- {product['name']}")

if __name__ == "__main__":
    main()
