# LISTADOS-TOP

## Sistema de Listados Enriquecidos para Compras y Analítica de Datos

**LISTADOS-TOP** es un sistema integral diseñado para el enriquecimiento de listados de productos, optimizado tanto para sistemas de compras como para análisis de datos avanzados. Proporciona un esquema robusto de datos, herramientas de análisis y un motor de compras inteligente.

## 🚀 Características Principales

### 📊 **Análisis de Datos Avanzado**
- **Análisis por categorías**: Rendimiento detallado por categoría de productos
- **Tendencias estacionales**: Identificación de patrones de demanda estacional
- **Análisis de precios**: Estadísticas de precios y optimización de descuentos
- **Métricas de conversión**: Análisis de conversión de vistas a compras
- **Insights de inventario**: Gestión y alertas de stock

### 🛒 **Motor de Compras Inteligente**
- **Filtrado avanzado**: Filtros por categoría, precio, rating, disponibilidad, etc.
- **Recomendaciones personalizadas**: Sistema de recomendaciones basado en similitud
- **Descuentos por volumen**: Cálculo automático de descuentos en compras al por mayor
- **Búsqueda inteligente**: Búsqueda por texto con scoring de relevancia
- **Optimización por presupuesto**: Mejores productos dentro de un presupuesto específico

### 📋 **Esquema de Datos Enriquecido**
- **Validación JSON Schema**: Estructura de datos bien definida y validada
- **Metadatos completos**: Información rica para análisis y compras
- **Soporte multimoneda**: Compatible con múltiples monedas
- **Información de proveedores**: Datos detallados de proveedores
- **Especificaciones técnicas**: Dimensiones, materiales, colores, tallas

## 📁 Estructura del Proyecto

```
LISTADOS-TOP/
├── README.md                          # Documentación principal
├── schema/
│   └── product_schema.json           # Esquema de validación JSON
├── data/
│   └── sample_products.json          # Datos de ejemplo
├── analytics/
│   ├── product_analytics.py          # Análisis de productos
│   ├── purchase_engine.py            # Motor de compras
│   └── data_manager.py               # Gestión de datos
├── config/
│   ├── config.json                   # Configuración principal
│   └── environments.json             # Configuraciones por entorno
└── examples/
    └── usage_examples.py             # Ejemplos de uso
```

## 🛠️ Instalación y Configuración

### Requisitos
- Python 3.7+
- jsonschema (para validación)

### Instalación de dependencias
```bash
pip install jsonschema
```

### Uso básico

#### 1. Análisis de Datos
```python
from analytics.product_analytics import ProductAnalytics

# Inicializar analizador
analytics = ProductAnalytics([])
analytics.load_from_file('data/sample_products.json')

# Generar reporte completo
report = analytics.generate_report()

# Análisis específicos
category_performance = analytics.get_category_performance()
seasonal_trends = analytics.get_seasonal_trends()
price_analysis = analytics.get_price_analysis()
```

#### 2. Motor de Compras
```python
from analytics.purchase_engine import PurchaseEngine, FilterCriteria, SortBy

# Inicializar motor
engine = PurchaseEngine([])
engine.load_from_file('data/sample_products.json')

# Filtrar productos
criteria = FilterCriteria(
    categories=["Electrónicos"],
    max_price=500,
    min_rating=4.0
)
filtered_products = engine.apply_filters(criteria)

# Obtener recomendaciones
recommendations = engine.get_recommendations("PROD-001", limit=5)

# Calcular descuentos por volumen
bulk_savings = engine.calculate_bulk_savings("PROD-001", quantity=10)
```

#### 3. Gestión de Datos
```python
from analytics.data_manager import DataManager

# Inicializar gestor
dm = DataManager()

# Importar y validar datos
result = dm.import_from_json('data/sample_products.json', validate=True)

# Exportar a diferentes formatos
dm.export_to_json(products, 'output.json')
dm.export_to_csv(products, 'output.csv')

# Crear backup
backup_path = dm.generate_backup(products)
```

## 📊 Ejemplos de Datos

### Producto de Ejemplo
```json
{
  "id": "PROD-001",
  "name": "Smartphone Pro Max 256GB",
  "description": "Smartphone de última generación...",
  "category": {
    "primary": "Electrónicos",
    "secondary": ["Smartphones", "Tecnología"]
  },
  "price": {
    "current": 899.99,
    "original": 1199.99,
    "currency": "USD",
    "discount_percentage": 25
  },
  "availability": {
    "in_stock": true,
    "stock_quantity": 150
  },
  "analytics": {
    "popularity_score": 95,
    "view_count": 15420,
    "purchase_count": 1247,
    "conversion_rate": 0.081,
    "average_rating": 4.6
  },
  "purchase_attributes": {
    "bulk_discount_tiers": [
      {"min_quantity": 10, "discount_percentage": 5},
      {"min_quantity": 50, "discount_percentage": 10}
    ],
    "shipping_info": {
      "free_shipping_threshold": 500,
      "estimated_delivery_days": 3
    }
  }
}
```

## 🎯 Casos de Uso

### Para Comercio Electrónico
- **Catálogo de productos enriquecido** con metadatos completos
- **Sistema de recomendaciones** para aumentar ventas
- **Gestión de inventario** con alertas automáticas
- **Optimización de precios** basada en datos

### Para Análisis de Datos
- **Análisis de tendencias** de mercado y estacionales
- **Métricas de rendimiento** por categoría y producto
- **Análisis de conversión** y comportamiento del usuario
- **Reportes ejecutivos** automatizados

### Para Sistemas de Compra
- **Filtrado inteligente** de productos
- **Cálculo automático** de descuentos por volumen
- **Comparación de proveedores** y precios
- **Optimización de presupuesto** de compras

## 🔧 Configuración Avanzada

### Entornos
El sistema soporta múltiples entornos configurables:
- **Development**: Para desarrollo local
- **Staging**: Para pruebas
- **Production**: Para producción

### Personalización
- **Esquemas personalizados**: Modifica `schema/product_schema.json` según necesidades
- **Métricas específicas**: Ajusta pesos de análisis en configuración
- **Nuevas funcionalidades**: Extiende las clases base para casos específicos

## 📈 Métricas y KPIs Soportados

- **Popularidad**: Score basado en vistas, compras y ratings
- **Conversión**: Ratio de vistas a compras
- **Rentabilidad**: Análisis de márgenes y descuentos
- **Satisfacción**: Ratings y reviews de clientes
- **Inventario**: Rotación y disponibilidad
- **Estacionalidad**: Patrones de demanda temporal

## 🚦 Ejecución de Ejemplos

### Demo Completo
```bash
cd examples/
python usage_examples.py
```

### Análisis Individual
```bash
cd analytics/
python product_analytics.py
```

### Motor de Compras
```bash
cd analytics/
python purchase_engine.py
```

### Gestión de Datos
```bash
cd analytics/
python data_manager.py
```

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo una licencia de uso interno. Para uso comercial, contactar al equipo de desarrollo.

## 📞 Soporte

Para soporte técnico y consultas:
- **Documentación**: Consulta la carpeta `examples/` para casos de uso
- **Issues**: Reporta problemas en el sistema de issues del repositorio
- **Contribuciones**: Las contribuciones son bienvenidas siguiendo las guías establecidas

---

**LISTADOS-TOP** - Transformando datos de productos en insights accionables para compras inteligentes y análisis avanzado. 🚀