#!/usr/bin/env python3
"""
Punto de entrada principal para la aplicación Tienda de Muebles.
Este archivo inicializa la aplicación y proporciona datos de ejemplo.
"""

from models.composicion.comedor import Comedor
from models.concretos.armario import Armario
from models.concretos.cajonera import Cajonera
from models.concretos.cama import Cama
from models.concretos.escritorio import Escritorio
from models.concretos.mesa import Mesa
from models.concretos.silla import Silla
from models.concretos.sillon import Sillon
from models.concretos.sofa import Sofa
from models.concretos.sofacama import SofaCama
from services.tienda import TiendaMuebles
from ui.menu import MenuTienda


def crear_catalogo_inicial(tienda: "TiendaMuebles") -> None:
    """
    Crea un catálogo inicial de muebles para demostrar el funcionamiento del sistema.
    Esta función muestra cómo instanciar diferentes tipos de muebles y agregarlos a la tienda.

    Args:
        tienda: Instancia de TiendaMuebles donde agregar los muebles
    """
    print("🔨 Creando catálogo inicial de muebles...")

    sillas = [
        Silla(
            nombre="Silla Clásica",
            material="Madera",
            color="Café",
            precio_base=150.0,
            tiene_respaldo=True,
            material_tapizado="tela",
        ),
        Silla(
            nombre="Silla de Oficina Ejecutiva",
            material="Metal",
            color="Negro",
            precio_base=350.0,
            tiene_respaldo=True,
            material_tapizado="cuero",
            altura_regulable=True,
            tiene_ruedas=True,
        ),
        Silla(
            nombre="Silla Moderna Minimalista",
            material="Plástico",
            color="Blanco",
            precio_base=80.0,
            tiene_respaldo=True,
        ),
    ]

    mesas = [
        Mesa(
            nombre="Mesa de Comedor Familiar",
            material="Madera",
            color="Roble",
            precio_base=500.0,
            forma="rectangular",
            capacidad_personas=6,
        ),
        Mesa(
            nombre="Mesa de Centro Redonda",
            material="Vidrio",
            color="Transparente",
            precio_base=300.0,
            forma="redonda",
            capacidad_personas=4,
        ),
        Mesa(
            nombre="Mesa de Trabajo Industrial",
            material="Metal",
            color="Gris",
            precio_base=450.0,
            forma="rectangular",
            capacidad_personas=4,
        ),
    ]

    asientos_grandes = [
        Sillon(
            nombre="Sillón Reclinable de Lujo",
            material="Cuero",
            color="Marrón",
            precio_base=800.0,
            tiene_respaldo=True,
            material_tapizado="cuero",
            es_reclinable=True,
            tiene_reposapiés=True,
        ),
        Sofa(
            nombre="Sofá Modular de 3 Plazas",
            material="Tela",
            color="Gris",
            precio_base=1200.0,
            capacidad_personas=3,
            tiene_respaldo=True,
            material_tapizado="tela",
            es_modular=True,
            incluye_cojines=True,
        ),
        Sofa(
            nombre="Sofá Chesterfield Clásico",
            material="Cuero",
            color="Verde",
            precio_base=2000.0,
            capacidad_personas=2,
            tiene_respaldo=True,
            material_tapizado="cuero",
            es_modular=False,
            incluye_cojines=False,
        ),
    ]

    almacenamiento = [
        Armario(
            nombre="Armario Ropero 4 Puertas",
            material="Madera",
            color="Blanco",
            precio_base=600.0,
            num_puertas=4,
            num_cajones=2,
            tiene_espejos=True,
        ),
        Cajonera(
            nombre="Cajonera Vintage 5 Cajones",
            material="Madera",
            color="Vintage",
            precio_base=300.0,
            num_cajones=5,
            tiene_ruedas=False,
        ),
        Cajonera(
            nombre="Cajonera Oficina con Ruedas",
            material="Metal",
            color="Gris",
            precio_base=180.0,
            num_cajones=3,
            tiene_ruedas=True,
        ),
    ]

    dormitorio_oficina = [
        Cama(
            nombre="Cama King Size de Lujo",
            material="Madera",
            color="Nogal",
            precio_base=1000.0,
            tamaño="king",
            incluye_colchon=True,
            tiene_cabecera=True,
        ),
        Cama(
            nombre="Cama Individual Juvenil",
            material="Metal",
            color="Azul",
            precio_base=400.0,
            tamaño="individual",
            incluye_colchon=False,
            tiene_cabecera=True,
        ),
        Escritorio(
            nombre="Escritorio Ejecutivo L-Shape",
            material="Madera",
            color="Caoba",
            precio_base=750.0,
            forma="L",
            tiene_cajones=True,
            num_cajones=4,
        ),
        Escritorio(
            nombre="Escritorio Gaming RGB",
            material="Metal",
            color="Negro",
            precio_base=500.0,
            forma="rectangular",
            tiene_cajones=False,
            tiene_iluminacion=True,
        ),
    ]

    sofacama = SofaCama(
        nombre="SofaCama Convertible Premium",
        material="Tela",
        color="Beige",
        precio_base=1500.0,
        capacidad_personas=3,
        material_tapizado="tela",
        tamaño_cama="matrimonial",
        incluye_colchon=True,
        mecanismo_conversion="hidraulico",
    )

    todos_los_muebles = (
        sillas
        + mesas
        + asientos_grandes
        + almacenamiento
        + dormitorio_oficina
        + [sofacama]
    )

    for mueble in todos_los_muebles:
        resultado = tienda.agregar_mueble(mueble)
        print(f"  ✓ {resultado}")

    print("✅ Catálogo inicial creado con éxito!")


def crear_comedores_ejemplo(tienda: "TiendaMuebles") -> None:
    """
    Crea comedores de ejemplo para demostrar la composición.

    Args:
        tienda: Instancia de TiendaMuebles donde agregar los comedores
    """
    print("\n🍽️ Creando comedores de ejemplo...")

    mesa_familiar = Mesa(
        nombre="Mesa Familiar Extensible",
        material="Madera",
        color="Roble",
        precio_base=800.0,
        forma="rectangular",
        capacidad_personas=8,
    )

    sillas_familiares = []
    for i in range(1, 7):  # 6 sillas
        silla = Silla(
            nombre=f"Silla Familiar {i}",
            material="Madera",
            color="Roble",
            precio_base=120.0,
            tiene_respaldo=True,
            material_tapizado="tela",
        )
        sillas_familiares.append(silla)

    comedor_familiar = Comedor(
        nombre="Comedor Familiar Completo", mesa=mesa_familiar, sillas=sillas_familiares
    )

    mesa_moderna = Mesa(
        nombre="Mesa Moderna Cristal",
        material="Vidrio",
        color="Negro",
        precio_base=600.0,
        forma="redonda",
        capacidad_personas=4,
    )

    sillas_modernas = []
    for i in range(1, 5):  # 4 sillas
        silla = Silla(
            nombre=f"Silla Moderna {i}",
            material="Metal",
            color="Negro",
            precio_base=150.0,
            tiene_respaldo=True,
            material_tapizado="cuero",
        )
        sillas_modernas.append(silla)

    comedor_moderno = Comedor(
        nombre="Comedor Moderno Premium", mesa=mesa_moderna, sillas=sillas_modernas
    )

    comedores = [comedor_familiar, comedor_moderno]
    for comedor in comedores:
        resultado = tienda.agregar_comedor(comedor)
        print(f"  ✓ {resultado}")

    print("✅ Comedores de ejemplo creados!")


def aplicar_descuentos_ejemplo(tienda: "TiendaMuebles") -> None:
    """
    Aplica algunos descuentos de ejemplo para demostrar el sistema.

    Args:
        tienda: Instancia de TiendaMuebles donde aplicar descuentos
    """
    print("\n🏷️ Aplicando descuentos de ejemplo...")

    descuentos = [
        ("silla", 10),  # 10% de descuento en sillas
        ("mesa", 15),  # 15% de descuento en mesas
        ("sofa", 20),  # 20% de descuento en sofás
    ]

    for categoria, porcentaje in descuentos:
        resultado = tienda.aplicar_descuento(categoria, porcentaje)
        print(f"  ✓ {resultado}")

    print("✅ Descuentos aplicados!")


def mostrar_estadisticas_iniciales(tienda: "TiendaMuebles") -> None:
    """
    Muestra estadísticas iniciales de la tienda.

    Args:
        tienda: Instancia de TiendaMuebles para obtener estadísticas
    """
    print("\n📊 Estadísticas iniciales de la tienda:")

    stats = tienda.obtener_estadisticas()
    print(f"  📦 Total de muebles: {stats.get('total_muebles', 0)}")
    print(f"  🍽️ Total de comedores: {stats.get('total_comedores', 0)}")
    print(f"  💰 Valor del inventario: ${stats.get('valor_inventario', 0):,.2f}")
    print(f"  🏷️ Descuentos activos: {stats.get('descuentos_activos', {})}")
    print(f"  🛒 Ventas realizadas: {stats.get('ventas_realizadas', 0)}")
    print(
        f"  📈 Total muebles vendidos (acumulado): {stats.get('total_muebles_vendidos', 0)}"
    )
    print(
        f"  💵 Valor total de ventas (acumulado): ${stats.get('valor_total_ventas', 0):,.2f}"
    )
    print("\n  📋 Distribución por tipos:")
    for tipo, cantidad in (stats.get("tipos_muebles", {}) or {}).items():
        print(f"    • {tipo}: {cantidad} unidades")


def main():
    """
    Función principal que inicializa y ejecuta la aplicación.

    Esta función demuestra todos los conceptos de OOP implementados:
    - Creación de objetos de diferentes clases
    - Herencia y polimorfismo al agregar diferentes tipos de muebles
    - Composición con los comedores
    - Herencia múltiple con el sofá-cama
    - Encapsulación y abstracción en toda la jerarquía
    """
    try:
        print("🏠 Bienvenido a la Tienda de Muebles - Taller OOP 🏠")
        print("=" * 50)

        tienda = TiendaMuebles("Mueblería Moderna OOP")
        print(f"🏪 Inicializando {tienda.nombre}...")

        crear_catalogo_inicial(tienda)

        crear_comedores_ejemplo(tienda)

        aplicar_descuentos_ejemplo(tienda)

        mostrar_estadisticas_iniciales(tienda)

        print("\n🎯 Iniciando interfaz de usuario...")
        menu = MenuTienda(tienda)

        input("\nPresiona Enter para iniciar el menú interactivo...")

        menu.ejecutar()

    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback

        traceback.print_exc()
    finally:
        print("\n" + "=" * 50)
        print("✨ Programa finalizado. ¡Gracias por usar la Tienda de Muebles! ✨")


if __name__ == "__main__":
    # Punto de entrada de la aplicación
    main()
