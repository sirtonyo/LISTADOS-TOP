#!/usr/bin/env python3
"""
Data Manager
Utilidades para importación, exportación y validación de datos
"""

import json
import csv
import jsonschema
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

class DataManager:
    """Gestor de datos para LISTADOS-TOP"""
    
    def __init__(self, schema_path: str = None):
        self.schema_path = schema_path or '../schema/product_schema.json'
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict[str, Any]:
        """Cargar esquema de validación"""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Esquema no encontrado en {self.schema_path}")
            return {}
    
    def validate_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Validar un producto contra el esquema"""
        if not self.schema:
            return {'valid': False, 'errors': ['Esquema no disponible']}
        
        try:
            jsonschema.validate(product, self.schema)
            return {'valid': True, 'errors': []}
        except jsonschema.ValidationError as e:
            return {'valid': False, 'errors': [str(e)]}
        except Exception as e:
            return {'valid': False, 'errors': [f'Error de validación: {str(e)}']}
    
    def validate_products_batch(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validar un lote de productos"""
        results = {
            'total_products': len(products),
            'valid_products': 0,
            'invalid_products': 0,
            'errors': []
        }
        
        for i, product in enumerate(products):
            validation = self.validate_product(product)
            if validation['valid']:
                results['valid_products'] += 1
            else:
                results['invalid_products'] += 1
                results['errors'].append({
                    'product_index': i,
                    'product_id': product.get('id', 'N/A'),
                    'errors': validation['errors']
                })
        
        return results
    
    def import_from_json(self, filepath: str, validate: bool = True) -> Dict[str, Any]:
        """Importar productos desde archivo JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            products = data.get('products', []) if isinstance(data, dict) else data
            
            result = {
                'success': True,
                'products_loaded': len(products),
                'products': products,
                'validation': None
            }
            
            if validate:
                validation = self.validate_products_batch(products)
                result['validation'] = validation
                if validation['invalid_products'] > 0:
                    result['success'] = False
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'products_loaded': 0,
                'products': []
            }
    
    def export_to_json(self, products: List[Dict[str, Any]], filepath: str, 
                      include_metadata: bool = True) -> Dict[str, Any]:
        """Exportar productos a archivo JSON"""
        try:
            export_data = {
                'export_info': {
                    'timestamp': datetime.now().isoformat(),
                    'total_products': len(products),
                    'schema_version': '1.0'
                } if include_metadata else {},
                'products': products
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return {
                'success': True,
                'filepath': filepath,
                'products_exported': len(products)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'products_exported': 0
            }
    
    def export_to_csv(self, products: List[Dict[str, Any]], filepath: str) -> Dict[str, Any]:
        """Exportar productos a archivo CSV (formato plano)"""
        try:
            if not products:
                return {'success': False, 'error': 'No hay productos para exportar'}
            
            # Campos principales para CSV
            csv_fields = [
                'id', 'name', 'description', 'category_primary', 'price_current',
                'price_currency', 'discount_percentage', 'in_stock', 'stock_quantity',
                'supplier_name', 'supplier_country', 'popularity_score', 'average_rating',
                'view_count', 'purchase_count', 'conversion_rate', 'created_at', 'status'
            ]
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
                writer.writeheader()
                
                for product in products:
                    row = {
                        'id': product.get('id', ''),
                        'name': product.get('name', ''),
                        'description': product.get('description', ''),
                        'category_primary': product.get('category', {}).get('primary', ''),
                        'price_current': product.get('price', {}).get('current', 0),
                        'price_currency': product.get('price', {}).get('currency', ''),
                        'discount_percentage': product.get('price', {}).get('discount_percentage', 0),
                        'in_stock': product.get('availability', {}).get('in_stock', False),
                        'stock_quantity': product.get('availability', {}).get('stock_quantity', 0),
                        'supplier_name': product.get('supplier', {}).get('name', ''),
                        'supplier_country': product.get('supplier', {}).get('country', ''),
                        'popularity_score': product.get('analytics', {}).get('popularity_score', 0),
                        'average_rating': product.get('analytics', {}).get('average_rating', 0),
                        'view_count': product.get('analytics', {}).get('view_count', 0),
                        'purchase_count': product.get('analytics', {}).get('purchase_count', 0),
                        'conversion_rate': product.get('analytics', {}).get('conversion_rate', 0),
                        'created_at': product.get('metadata', {}).get('created_at', ''),
                        'status': product.get('metadata', {}).get('status', '')
                    }
                    writer.writerow(row)
            
            return {
                'success': True,
                'filepath': filepath,
                'products_exported': len(products)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'products_exported': 0
            }
    
    def create_sample_product(self, product_id: str, name: str, category: str, 
                            price: float, currency: str = "USD") -> Dict[str, Any]:
        """Crear un producto de muestra con estructura mínima"""
        return {
            "id": product_id,
            "name": name,
            "category": {
                "primary": category
            },
            "price": {
                "current": price,
                "currency": currency
            },
            "availability": {
                "in_stock": True,
                "stock_quantity": 100
            },
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
        }
    
    def merge_products(self, existing_products: List[Dict[str, Any]], 
                      new_products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fusionar listas de productos, actualizando existentes"""
        existing_ids = {p['id']: i for i, p in enumerate(existing_products)}
        merged = existing_products.copy()
        
        added = 0
        updated = 0
        
        for new_product in new_products:
            product_id = new_product.get('id')
            if not product_id:
                continue
            
            if product_id in existing_ids:
                # Actualizar producto existente
                index = existing_ids[product_id]
                merged[index] = new_product
                updated += 1
            else:
                # Agregar nuevo producto
                merged.append(new_product)
                added += 1
        
        return {
            'merged_products': merged,
            'total_products': len(merged),
            'products_added': added,
            'products_updated': updated
        }
    
    def filter_by_date_range(self, products: List[Dict[str, Any]], 
                           start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Filtrar productos por rango de fechas de creación"""
        filtered = []
        
        for product in products:
            created_at = product.get('metadata', {}).get('created_at')
            if created_at:
                try:
                    product_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    start = datetime.fromisoformat(start_date)
                    end = datetime.fromisoformat(end_date)
                    
                    if start <= product_date <= end:
                        filtered.append(product)
                except ValueError:
                    continue
        
        return filtered
    
    def generate_backup(self, products: List[Dict[str, Any]], backup_dir: str = "backups") -> str:
        """Generar backup de productos con timestamp"""
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"products_backup_{timestamp}.json"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        result = self.export_to_json(products, backup_path)
        
        if result['success']:
            return backup_path
        else:
            raise Exception(f"Error creando backup: {result['error']}")

def main():
    """Función principal de demostración"""
    print("📁 DATA MANAGER - DEMOSTRACIÓN")
    print("=" * 50)
    
    # Inicializar gestor de datos
    dm = DataManager()
    
    # 1. Cargar y validar datos existentes
    print("\n1. CARGANDO DATOS EXISTENTES:")
    result = dm.import_from_json('../data/sample_products.json')
    
    if result['success']:
        print(f"✅ Productos cargados: {result['products_loaded']}")
        if result['validation']:
            val = result['validation']
            print(f"   - Válidos: {val['valid_products']}")
            print(f"   - Inválidos: {val['invalid_products']}")
    else:
        print(f"❌ Error: {result['error']}")
        return
    
    products = result['products']
    
    # 2. Exportar a CSV
    print("\n2. EXPORTANDO A CSV:")
    csv_result = dm.export_to_csv(products, 'products_export.csv')
    if csv_result['success']:
        print(f"✅ CSV creado: {csv_result['filepath']}")
        print(f"   - Productos exportados: {csv_result['products_exported']}")
    
    # 3. Crear producto de muestra
    print("\n3. CREANDO PRODUCTO DE MUESTRA:")
    sample_product = dm.create_sample_product(
        "PROD-SAMPLE-001",
        "Producto de Prueba",
        "Pruebas",
        99.99
    )
    print(f"✅ Producto creado: {sample_product['name']}")
    
    # 4. Validar producto de muestra
    print("\n4. VALIDANDO PRODUCTO:")
    validation = dm.validate_product(sample_product)
    if validation['valid']:
        print("✅ Producto válido")
    else:
        print(f"❌ Errores de validación: {validation['errors']}")
    
    # 5. Generar backup
    print("\n5. GENERANDO BACKUP:")
    try:
        backup_path = dm.generate_backup(products)
        print(f"✅ Backup creado: {backup_path}")
    except Exception as e:
        print(f"❌ Error creando backup: {e}")
    
    print("\n✅ DEMOSTRACIÓN DEL DATA MANAGER COMPLETADA")

if __name__ == "__main__":
    main()
