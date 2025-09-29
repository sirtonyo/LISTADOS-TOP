#!/usr/bin/env python3
"""
Product Analytics Utilities
Herramientas para análisis de datos de productos enriquecidos
"""

import json
import statistics
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Any, Tuple

class ProductAnalytics:
    """Clase para análisis de datos de productos"""
    
    def __init__(self, products_data: List[Dict[str, Any]]):
        self.products = products_data
    
    def load_from_file(self, filepath: str):
        """Cargar datos desde archivo JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.products = data.get('products', [])
    
    def get_category_performance(self) -> Dict[str, Dict[str, float]]:
        """Análisis de rendimiento por categoría"""
        category_stats = defaultdict(lambda: {
            'total_products': 0,
            'avg_price': 0,
            'avg_rating': 0,
            'total_views': 0,
            'total_purchases': 0,
            'avg_conversion_rate': 0,
            'total_revenue_estimate': 0
        })
        
        for product in self.products:
            category = product['category']['primary']
            analytics = product.get('analytics', {})
            price = product['price']['current']
            
            category_stats[category]['total_products'] += 1
            category_stats[category]['avg_price'] += price
            category_stats[category]['avg_rating'] += analytics.get('average_rating', 0)
            category_stats[category]['total_views'] += analytics.get('view_count', 0)
            category_stats[category]['total_purchases'] += analytics.get('purchase_count', 0)
            category_stats[category]['avg_conversion_rate'] += analytics.get('conversion_rate', 0)
            category_stats[category]['total_revenue_estimate'] += price * analytics.get('purchase_count', 0)
        
        # Calcular promedios
        for category, stats in category_stats.items():
            count = stats['total_products']
            if count > 0:
                stats['avg_price'] = round(stats['avg_price'] / count, 2)
                stats['avg_rating'] = round(stats['avg_rating'] / count, 2)
                stats['avg_conversion_rate'] = round(stats['avg_conversion_rate'] / count, 4)
        
        return dict(category_stats)
    
    def get_seasonal_trends(self) -> Dict[str, Dict[str, float]]:
        """Análisis de tendencias estacionales"""
        seasonal_data = defaultdict(lambda: defaultdict(list))
        
        for product in self.products:
            analytics = product.get('analytics', {})
            seasonal_trends = analytics.get('seasonal_trends', [])
            
            for trend in seasonal_trends:
                season = trend['season']
                multiplier = trend['demand_multiplier']
                seasonal_data[season]['multipliers'].append(multiplier)
                seasonal_data[season]['products'].append(product['name'])
        
        # Calcular estadísticas por temporada
        seasonal_stats = {}
        for season, data in seasonal_data.items():
            multipliers = data['multipliers']
            seasonal_stats[season] = {
                'avg_demand_multiplier': round(statistics.mean(multipliers), 2),
                'max_demand_multiplier': max(multipliers),
                'min_demand_multiplier': min(multipliers),
                'product_count': len(multipliers),
                'top_products': data['products'][:5]  # Top 5 productos
            }
        
        return seasonal_stats
    
    def get_price_analysis(self) -> Dict[str, Any]:
        """Análisis de precios y descuentos"""
        prices = []
        discounts = []
        discounted_products = []
        
        for product in self.products:
            current_price = product['price']['current']
            original_price = product['price'].get('original')
            discount = product['price'].get('discount_percentage', 0)
            
            prices.append(current_price)
            if discount > 0:
                discounts.append(discount)
                discounted_products.append({
                    'name': product['name'],
                    'discount': discount,
                    'savings': original_price - current_price if original_price else 0
                })
        
        return {
            'price_statistics': {
                'avg_price': round(statistics.mean(prices), 2),
                'median_price': round(statistics.median(prices), 2),
                'min_price': min(prices),
                'max_price': max(prices),
                'price_range': max(prices) - min(prices)
            },
            'discount_analysis': {
                'products_with_discount': len(discounted_products),
                'avg_discount': round(statistics.mean(discounts), 2) if discounts else 0,
                'max_discount': max(discounts) if discounts else 0,
                'top_discounted_products': sorted(discounted_products, 
                                                key=lambda x: x['discount'], reverse=True)[:5]
            }
        }
    
    def get_inventory_status(self) -> Dict[str, Any]:
        """Análisis de inventario y disponibilidad"""
        in_stock = 0
        out_of_stock = 0
        total_inventory = 0
        low_stock_products = []
        
        for product in self.products:
            availability = product['availability']
            stock_qty = availability.get('stock_quantity', 0)
            
            if availability['in_stock']:
                in_stock += 1
                total_inventory += stock_qty
                if stock_qty < 50:  # Considerar stock bajo si < 50 unidades
                    low_stock_products.append({
                        'name': product['name'],
                        'stock': stock_qty,
                        'category': product['category']['primary']
                    })
            else:
                out_of_stock += 1
        
        return {
            'inventory_summary': {
                'total_products': len(self.products),
                'in_stock': in_stock,
                'out_of_stock': out_of_stock,
                'availability_rate': round((in_stock / len(self.products)) * 100, 2),
                'total_inventory_units': total_inventory
            },
            'low_stock_alerts': sorted(low_stock_products, key=lambda x: x['stock'])
        }
    
    def get_purchase_insights(self) -> Dict[str, Any]:
        """Insights para optimización de compras"""
        bulk_eligible = []
        high_conversion = []
        popular_products = []
        
        for product in self.products:
            analytics = product.get('analytics', {})
            purchase_attrs = product.get('purchase_attributes', {})
            
            # Productos elegibles para descuentos por volumen
            if purchase_attrs.get('bulk_discount_tiers'):
                bulk_eligible.append({
                    'name': product['name'],
                    'min_qty': purchase_attrs.get('min_order_quantity', 1),
                    'max_discount': max([tier['discount_percentage'] 
                                       for tier in purchase_attrs['bulk_discount_tiers']])
                })
            
            # Productos con alta conversión
            conversion = analytics.get('conversion_rate', 0)
            if conversion > 0.05:  # > 5% conversión
                high_conversion.append({
                    'name': product['name'],
                    'conversion_rate': conversion,
                    'popularity_score': analytics.get('popularity_score', 0)
                })
            
            # Productos populares
            popularity = analytics.get('popularity_score', 0)
            if popularity > 80:
                popular_products.append({
                    'name': product['name'],
                    'popularity_score': popularity,
                    'purchase_count': analytics.get('purchase_count', 0)
                })
        
        return {
            'bulk_purchase_opportunities': sorted(bulk_eligible, 
                                                key=lambda x: x['max_discount'], reverse=True),
            'high_conversion_products': sorted(high_conversion, 
                                             key=lambda x: x['conversion_rate'], reverse=True),
            'popular_products': sorted(popular_products, 
                                     key=lambda x: x['popularity_score'], reverse=True)
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """Generar reporte completo de análisis"""
        return {
            'report_timestamp': datetime.now().isoformat(),
            'total_products_analyzed': len(self.products),
            'category_performance': self.get_category_performance(),
            'seasonal_trends': self.get_seasonal_trends(),
            'price_analysis': self.get_price_analysis(),
            'inventory_status': self.get_inventory_status(),
            'purchase_insights': self.get_purchase_insights()
        }

def main():
    """Función principal para ejecutar análisis"""
    # Cargar datos de ejemplo
    analytics = ProductAnalytics([])
    analytics.load_from_file('../data/sample_products.json')
    
    # Generar reporte
    report = analytics.generate_report()
    
    # Guardar reporte
    with open('analytics_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("✅ Reporte de análisis generado: analytics_report.json")
    print(f"📊 Productos analizados: {report['total_products_analyzed']}")
    print(f"📈 Categorías encontradas: {len(report['category_performance'])}")
    print(f"🛒 Productos con descuentos por volumen: {len(report['purchase_insights']['bulk_purchase_opportunities'])}")

if __name__ == "__main__":
    main()
