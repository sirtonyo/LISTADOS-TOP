#!/usr/bin/env python3
"""
Ejemplos de uso del sistema LISTADOS-TOP
Demuestra las capacidades de análisis y compras
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'analytics'))

from product_analytics import ProductAnalytics
from purchase_engine import PurchaseEngine, FilterCriteria, SortBy

def demo_analytics():
    """Demostración de capacidades de análisis"""
    print("📊 DEMO: ANÁLISIS DE DATOS")
    print("=" * 50)
    
    # Inicializar analizador
    analytics = ProductAnalytics([])
    analytics.load_from_file('../data/sample_products.json')
    
    # 1. Análisis por categoría
    print("\n1. RENDIMIENTO POR CATEGORÍA:")
    category_perf = analytics.get_category_performance()
    for category, stats in category_perf.items():
        print(f"\n📱 {category}:")
        print(f"   - Productos: {stats['total_products']}")
        print(f"   - Precio promedio: ${stats['avg_price']}")
        print(f"   - Rating promedio: {stats['avg_rating']}")
        print(f"   - Conversión promedio: {stats['avg_conversion_rate']:.1%}")
        print(f"   - Ingresos estimados: ${stats['total_revenue_estimate']:,.2f}")
    
    # 2. Análisis estacional
    print("\n2. TENDENCIAS ESTACIONALES:")
    seasonal = analytics.get_seasonal_trends()
    for season, data in seasonal.items():
        print(f"\n🌱 {season.upper()}:")
        print(f"   - Multiplicador promedio: {data['avg_demand_multiplier']}")
        print(f"   - Productos analizados: {data['product_count']}")
    
    # 3. Análisis de precios
    print("\n3. ANÁLISIS DE PRECIOS:")
    price_analysis = analytics.get_price_analysis()
    price_stats = price_analysis['price_statistics']
    discount_stats = price_analysis['discount_analysis']
    
    print(f"   💰 Precio promedio: ${price_stats['avg_price']}")
    print(f"   📊 Rango de precios: ${price_stats['min_price']} - ${price_stats['max_price']}")
    print(f"   🎯 Productos con descuento: {discount_stats['products_with_discount']}")
    print(f"   💸 Descuento promedio: {discount_stats['avg_discount']}%")
    
    # 4. Estado de inventario
    print("\n4. ESTADO DE INVENTARIO:")
    inventory = analytics.get_inventory_status()
    inv_summary = inventory['inventory_summary']
    
    print(f"   📦 Productos en stock: {inv_summary['in_stock']}/{inv_summary['total_products']}")
    print(f"   ✅ Tasa de disponibilidad: {inv_summary['availability_rate']}%")
    print(f"   📊 Unidades totales: {inv_summary['total_inventory_units']}")
    
    if inventory['low_stock_alerts']:
        print(f"   ⚠️  Productos con stock bajo:")
        for product in inventory['low_stock_alerts'][:3]:
            print(f"      - {product['name']}: {product['stock']} unidades")

def demo_purchase_engine():
    """Demostración del motor de compras"""
    print("\n\n🛒 DEMO: MOTOR DE COMPRAS")
    print("=" * 50)
    
    # Inicializar motor
    engine = PurchaseEngine([])
    engine.load_from_file('../data/sample_products.json')
    
    # 1. Filtrado de productos
    print("\n1. FILTRADO DE PRODUCTOS:")
    print("\n🎯 Electrónicos bajo $500 con rating > 4.5:")
    criteria = FilterCriteria(
        categories=["Electrónicos"],
        max_price=500,
        min_rating=4.5
    )
    filtered = engine.apply_filters(criteria)
    for product in filtered:
        rating = product.get('analytics', {}).get('average_rating', 0)
        print(f"   - {product['name']}: ${product['price']['current']} (⭐ {rating})")
    
    # 2. Ordenamiento
    print("\n2. ORDENAMIENTO POR POPULARIDAD:")
    engine.sort_products(SortBy.POPULARITY)
    top_popular = engine.filtered_products[:3]
    for i, product in enumerate(top_popular, 1):
        popularity = product.get('analytics', {}).get('popularity_score', 0)
        print(f"   {i}. {product['name']}: {popularity} pts de popularidad")
    
    # 3. Recomendaciones
    print("\n3. RECOMENDACIONES:")
    print("\n🎯 Productos similares al Smartphone Pro Max:")
    recommendations = engine.get_recommendations("PROD-001", limit=3)
    for i, product in enumerate(recommendations, 1):
        print(f"   {i}. {product['name']} - ${product['price']['current']}")
    
    # 4. Descuentos por volumen
    print("\n4. DESCUENTOS POR VOLUMEN:")
    quantities = [5, 15, 30]
    for qty in quantities:
        bulk_info = engine.calculate_bulk_savings("PROD-004", qty)
        if 'error' not in bulk_info:
            print(f"\n   📦 {qty} unidades de Smartwatch:")
            print(f"      Precio total: ${bulk_info['total_price']:.2f}")
            if bulk_info['savings'] > 0:
                print(f"      Ahorro: ${bulk_info['savings']:.2f} ({bulk_info['discount_percentage']}%)")
    
    # 5. Búsqueda por presupuesto
    print("\n5. PRODUCTOS POR PRESUPUESTO:")
    budget = 300
    budget_products = engine.get_product_by_budget(budget)
    print(f"\n💰 Mejores opciones con presupuesto de ${budget}:")
    for product in budget_products[:3]:
        rating = product.get('analytics', {}).get('average_rating', 0)
        print(f"   - {product['name']}: ${product['price']['current']} (⭐ {rating})")
    
    # 6. Búsqueda de texto
    print("\n6. BÚSQUEDA POR TEXTO:")
    search_terms = ["inalámbrico", "premium", "deportivo"]
    for term in search_terms:
        results = engine.search_products(term)
        print(f"\n🔍 Resultados para '{term}':")
        for product in results[:2]:
            print(f"   - {product['name']}")

def demo_business_insights():
    """Demostración de insights de negocio"""
    print("\n\n💡 DEMO: INSIGHTS DE NEGOCIO")
    print("=" * 50)
    
    analytics = ProductAnalytics([])
    analytics.load_from_file('../data/sample_products.json')
    
    insights = analytics.get_purchase_insights()
    
    # 1. Oportunidades de venta por volumen
    print("\n1. OPORTUNIDADES DE VENTA POR VOLUMEN:")
    bulk_ops = insights['bulk_purchase_opportunities']
    for i, product in enumerate(bulk_ops[:3], 1):
        print(f"   {i}. {product['name']}")
        print(f"      - Cantidad mínima: {product['min_qty']}")
        print(f"      - Descuento máximo: {product['max_discount']}%")
    
    # 2. Productos de alta conversión
    print("\n2. PRODUCTOS DE ALTA CONVERSIÓN:")
    high_conv = insights['high_conversion_products']
    for i, product in enumerate(high_conv[:3], 1):
        print(f"   {i}. {product['name']}")
        print(f"      - Conversión: {product['conversion_rate']:.1%}")
        print(f"      - Popularidad: {product['popularity_score']} pts")
    
    # 3. Productos más populares
    print("\n3. PRODUCTOS MÁS POPULARES:")
    popular = insights['popular_products']
    for i, product in enumerate(popular[:3], 1):
        print(f"   {i}. {product['name']}")
        print(f"      - Popularidad: {product['popularity_score']} pts")
        print(f"      - Compras: {product['purchase_count']}")

def demo_data_export():
    """Demostración de exportación de datos"""
    print("\n\n📤 DEMO: EXPORTACIÓN DE DATOS")
    print("=" * 50)
    
    analytics = ProductAnalytics([])
    analytics.load_from_file('../data/sample_products.json')
    
    # Generar reporte completo
    print("\n📊 Generando reporte completo...")
    report = analytics.generate_report()
    
    # Guardar en archivo
    import json
    output_file = 'demo_analytics_report.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Reporte guardado en: {output_file}")
    print(f"📈 Timestamp del reporte: {report['report_timestamp']}")
    print(f"🔢 Productos analizados: {report['total_products_analyzed']}")
    print(f"📂 Categorías analizadas: {len(report['category_performance'])}")

def main():
    """Función principal que ejecuta todas las demostraciones"""
    print("🚀 LISTADOS-TOP - SISTEMA DE DEMOSTRACIÓN")
    print("Sistema de listados enriquecidos para compras y analítica")
    print("=" * 70)
    
    try:
        demo_analytics()
        demo_purchase_engine()
        demo_business_insights()
        demo_data_export()
        
        print("\n\n✅ DEMOSTRACIÓN COMPLETADA")
        print("=" * 50)
        print("El sistema LISTADOS-TOP está listo para:")
        print("• 📊 Análisis avanzado de productos")
        print("• 🛒 Motor de compras inteligente")
        print("• 🎯 Recomendaciones personalizadas")
        print("• 💰 Optimización de precios y descuentos")
        print("• 📈 Insights de negocio en tiempo real")
        
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")
        print("Verifique que los archivos de datos estén disponibles.")

if __name__ == "__main__":
    main()
