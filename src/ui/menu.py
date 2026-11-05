"""
Interfaz de usuario usando Rich para crear un menú interactivo y atractivo.
"""

import time

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

from models.mueble import Mueble

# Corrección de imports para ejecución directa
from services.tienda import TiendaMuebles

# TODO: Importar los servicios y modelos


class MenuTienda:
    """
    Clase que maneja la interfaz de usuario de la tienda usando Rich.

    Proporciona un menú interactivo con opciones para:
    - Ver catálogo de muebles
    - Buscar y filtrar productos
    - Realizar ventas
    - Ver estadísticas
    - Gestionar inventario

    Conceptos aplicados:
    - Separación de responsabilidades: La UI está separada de la lógica de negocio
    - Encapsulación: Agrupa toda la lógica de interfaz de usuario
    - Composición: Usa una instancia de TiendaMuebles para las operaciones
    """

    def __init__(self, tienda: "TiendaMuebles"):
        """
        Constructor del menú.

        Args:
            tienda: Instancia de TiendaMuebles para las operaciones
        """
        # Inicializar atributos
        self.tienda = tienda
        self.console = Console()
        self.running = True

    def mostrar_catalogo_completo(self):
        """Muestra todos los muebles disponibles en una tabla."""

        # Implementar visualización del catálogo
        muebles = self.tienda._inventario  # Acceso directo para el ejemplo

        if not muebles:
            self.console.print("[yellow]No hay muebles en el inventario.[/yellow]")
            return

        table = Table(title="📋 Catálogo de Muebles")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Nombre", style="magenta")
        table.add_column("Tipo", style="green")
        table.add_column("Material", style="yellow")
        table.add_column("Color", style="blue")
        table.add_column("Precio", style="red", justify="right")

        for i, mueble in enumerate(muebles, 1):
            try:
                precio = f"${mueble.calcular_precio():.2f}"
                tipo = type(mueble).__name__
                table.add_row(
                    str(i), mueble.nombre, tipo, mueble.material, mueble.color, precio
                )
            except Exception:
                table.add_row(str(i), mueble.nombre, "Error", "-", "-", "Error")

        self.console.print(table)

    def buscar_muebles_interactivo(self):
        """Interfaz interactiva para buscar muebles."""

        termino_busqueda = Prompt.ask(
            "[green]Ingresa el nombre o parte del nombre a buscar[/green]"
        )

        if not termino_busqueda.strip():
            self.console.print("[red]Término de búsqueda vacío.[/red]")
            return

        with self.console.status("[bold green]Buscando muebles..."):
            time.sleep(0.5)  # Simular tiempo de búsqueda
            resultados = self.tienda.buscar_muebles_por_nombre(termino_busqueda)

        if not resultados:
            self.console.print(
                f"[yellow]No se encontraron muebles que contengan '{termino_busqueda}'.[/yellow]"
            )
            return

        self.console.print(
            f"\n[green]Se encontraron {len(resultados)} resultado(s):[/green]"
        )
        self._mostrar_lista_muebles(resultados)

    def filtrar_por_precio_interactivo(self):
        """Interfaz interactiva para filtrar por precio."""

        self.console.print("[cyan]Filtrar muebles por rango de precio[/cyan]")

        precio_min = IntPrompt.ask("Precio mínimo", default=0, show_default=True)

        precio_max = IntPrompt.ask(
            "Precio máximo (0 = sin límite)", default=0, show_default=True
        )

        if precio_max == 0:
            precio_max = float("inf")

        if precio_min > precio_max:
            self.console.print(
                "[red]Error: El precio mínimo no puede ser mayor al máximo.[/red]"
            )
            return

        with self.console.status("[bold green]Filtrando muebles..."):
            time.sleep(0.3)
            resultados = self.tienda.filtrar_por_precio(precio_min, precio_max)

        if not resultados:
            self.console.print(
                f"[yellow]No hay muebles en el rango ${precio_min} - ${precio_max}.[/yellow]"
            )
            return

        self.console.print(
            f"\n[green]Se encontraron {len(resultados)} mueble(s) en el rango:[/green]"
        )
        self._mostrar_lista_muebles(resultados)

    def filtrar_por_material_interactivo(self):
        """Interfaz interactiva para filtrar por material."""

        material = Prompt.ask(
            "[green]Ingresa el material a buscar (ej: madera, metal, plástico)[/green]"
        )

        if not material.strip():
            self.console.print("[red]Material no puede estar vacío.[/red]")
            return

        with self.console.status(f"[bold green]Buscando muebles de {material}..."):
            time.sleep(0.3)
            resultados = self.tienda.filtrar_por_material(material)

        if not resultados:
            self.console.print(
                f"[yellow]No hay muebles de material '{material}'.[/yellow]"
            )
            return

        self.console.print(f"\n[green]Muebles de {material} encontrados:[/green]")
        self._mostrar_lista_muebles(resultados)

    def mostrar_comedores(self):
        """Muestra todos los comedores disponibles."""

        comedores = self.tienda._comedores

        if not comedores:
            self.console.print("[yellow]No hay comedores disponibles.[/yellow]")
            return

        for i, comedor in enumerate(comedores, 1):
            panel_content = comedor.obtener_descripcion_completa()
            panel = Panel(panel_content, title=f"Comedor #{i}", border_style="green")
            self.console.print(panel)

    def realizar_venta_interactiva(self):
        """Interfaz interactiva para realizar ventas."""

        muebles = self.tienda._inventario

        if not muebles:
            self.console.print("[red]No hay muebles disponibles para venta.[/red]")
            return

        self.console.print("[cyan]Selecciona un mueble para vender:[/cyan]")
        self._mostrar_lista_muebles(muebles, numerada=True)

        try:
            indice = IntPrompt.ask(
                "Número del mueble",
                choices=[str(i) for i in range(1, len(muebles) + 1)],
            )

            mueble_seleccionado = muebles[indice - 1]

            # Mostrar detalles del mueble
            self.console.print("\n[green]Mueble seleccionado:[/green]")
            self.console.print(mueble_seleccionado.obtener_descripcion())

            confirmar = Confirm.ask("\n¿Confirmar la venta?")
            if not confirmar:
                self.console.print("[yellow]Venta cancelada.[/yellow]")
                return

            cliente = Prompt.ask("Nombre del cliente", default="Cliente Anónimo")

            resultado = self.tienda.realizar_venta(mueble_seleccionado, cliente)

            if "error" in resultado:
                self.console.print(f"[red]Error: {resultado['error']}[/red]")
            else:
                self._mostrar_comprobante_venta(resultado)

        except (ValueError, IndexError):
            self.console.print("[red]Selección inválida.[/red]")

    def mostrar_estadisticas(self):
        """Muestra las estadísticas de la tienda."""

        with self.console.status("[bold green]Calculando estadísticas..."):
            time.sleep(0.5)
            stats = self.tienda.obtener_estadisticas()
            if not isinstance(stats, dict):
                stats = {}
        table = Table(title="📊 Estadísticas de la Tienda")
        table.add_column("Métrica", style="cyan", no_wrap=True)
        table.add_column("Valor", style="magenta", justify="right")
        table.add_row("Total de muebles", str(stats.get("total_muebles", 0)))
        table.add_row("Total de comedores", str(stats.get("total_comedores", 0)))
        table.add_row(
            "Valor del inventario", f"${stats.get('valor_inventario', 0):.2f}"
        )
        table.add_row("Ventas realizadas", str(stats.get("ventas_realizadas", 0)))
        table.add_row("Descuentos activos", str(stats.get("descuentos_activos", {})))
        # Estadísticas acumulativas
        table.add_row(
            "Total muebles vendidos (acumulado)",
            str(stats.get("total_muebles_vendidos", 0)),
        )
        table.add_row(
            "Valor total de ventas (acumulado)",
            f"${stats.get('valor_total_ventas', 0):.2f}",
        )
        self.console.print(table)
        tipos = stats.get("tipos_muebles", {})
        if tipos:
            self.console.print("\n[cyan]Distribución por tipos:[/cyan]")
            for tipo, cantidad in tipos.items():
                self.console.print(f"  • {tipo}: {cantidad} unidades")

    def generar_reporte_interactivo(self):
        """Genera y muestra el reporte de inventario."""

        with self.console.status("[bold green]Generando reporte..."):
            time.sleep(1)  # Simular tiempo de generación
            reporte = self.tienda.generar_reporte_inventario()

        panel = Panel(
            reporte,
            title="📋 Reporte de Inventario",
            border_style="blue",
            padding=(1, 2),
        )

        self.console.print(panel)

        # Preguntar si desea guardar el reporte
        guardar = Confirm.ask("¿Deseas guardar el reporte en un archivo?")
        if guardar:
            filename = Prompt.ask(
                "Nombre del archivo", default="reporte_inventario.txt"
            )
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(reporte)
                self.console.print(f"[green]Reporte guardado en {filename}[/green]")
            except Exception as e:
                self.console.print(f"[red]Error al guardar: {str(e)}[/red]")

    def aplicar_descuentos_interactivo(self):
        """Interfaz para aplicar descuentos por categoría."""

        categorias_disponibles = [
            "silla",
            "mesa",
            "sofa",
            "cama",
            "armario",
            "escritorio",
        ]

        self.console.print("[cyan]Categorías disponibles:[/cyan]")
        for i, categoria in enumerate(categorias_disponibles, 1):
            self.console.print(f"  {i}. {categoria.title()}")

        try:
            indice = IntPrompt.ask(
                "Selecciona una categoría",
                choices=[str(i) for i in range(1, len(categorias_disponibles) + 1)],
            )

            categoria = categorias_disponibles[indice - 1]

            porcentaje = IntPrompt.ask(
                f"Porcentaje de descuento para {categoria}s (1-50)",
                choices=[str(i) for i in range(1, 51)],
            )

            resultado = self.tienda.aplicar_descuento(categoria, porcentaje)
            self.console.print(f"[green]{resultado}[/green]")

        except (ValueError, IndexError):
            self.console.print("[red]Selección inválida.[/red]")

    def _mostrar_lista_muebles(self, muebles: list["Mueble"], numerada: bool = False):
        """
        Muestra una lista de muebles en formato tabla.
        Método auxiliar privado.

        Args:
            muebles: Lista de muebles a mostrar
            numerada: Si incluir números para selección
        """

        table = Table()

        if numerada:
            table.add_column("#", style="cyan", no_wrap=True)

        table.add_column("Nombre", style="magenta")
        table.add_column("Tipo", style="green")
        table.add_column("Material", style="yellow")
        table.add_column("Precio", style="red", justify="right")

        for i, mueble in enumerate(muebles, 1):
            try:
                precio = f"${mueble.calcular_precio():.2f}"
                tipo = type(mueble).__name__

                row_data = [mueble.nombre, tipo, mueble.material, precio]
                if numerada:
                    row_data.insert(0, str(i))

                table.add_row(*row_data)
            except Exception:
                row_data = [mueble.nombre, "Error", mueble.material, "Error"]
                if numerada:
                    row_data.insert(0, str(i))
                table.add_row(*row_data)

        self.console.print(table)

    def _mostrar_comprobante_venta(self, venta: dict):
        """
        Muestra el comprobante de venta.
        Método auxiliar privado.

        Args:
            venta: Diccionario con información de la venta
        """

        comprobante = f"""
        🧾 COMPROBANTE DE VENTA 🧾

        Cliente: {venta["cliente"]}
        Producto: {venta["mueble"]}
        Precio original: ${venta["precio_original"]:.2f}
        Descuento aplicado: {venta["descuento"]:.1f}%
        PRECIO FINAL: ${venta["precio_final"]:.2f}

        ¡Gracias por su compra!
        """

        panel = Panel(
            comprobante.strip(),
            title="Venta Exitosa",
            border_style="green",
            padding=(1, 2),
        )

        self.console.print(panel)

    def ejecutar(self):
        """Ejecuta el bucle principal del menú."""

        self.console.clear()
        self.mostrar_banner()

        while self.running:
            try:
                opcion = self.mostrar_menu_principal()

                if opcion == 0:
                    self.console.print("[red]¡Hasta luego! 👋[/red]")
                    self.running = False
                elif opcion == 1:
                    self.mostrar_catalogo_completo()
                elif opcion == 2:
                    self.buscar_muebles_interactivo()
                elif opcion == 3:
                    self.filtrar_por_precio_interactivo()
                elif opcion == 4:
                    self.filtrar_por_material_interactivo()
                elif opcion == 5:
                    self.mostrar_comedores()
                elif opcion == 6:
                    self.realizar_venta_interactiva()
                elif opcion == 7:
                    self.mostrar_estadisticas()
                elif opcion == 8:
                    self.generar_reporte_interactivo()
                elif opcion == 9:
                    self.aplicar_descuentos_interactivo()

                if self.running:
                    input("\nPresiona Enter para continuar...")
                    self.console.clear()

            except KeyboardInterrupt:
                self.console.print("\n[red]Operación cancelada por el usuario.[/red]")
                self.running = False
            except Exception as e:
                self.console.print(f"[red]Error inesperado: {str(e)}[/red]")
                input("Presiona Enter para continuar...")

    def mostrar_banner(self):
        """Muestra el banner de bienvenida de la tienda."""

        banner_text = Text(f"🏠 {self.tienda.nombre} 🏠", style="bold magenta")
        banner_text.stylize("bold blue", 0, 2)  # Emoji inicial
        banner_text.stylize("bold blue", -2, -0)  # Emoji final

        panel = Panel(
            banner_text,
            title="Bienvenido",
            subtitle="Tu tienda de muebles favorita",
            border_style="blue",
        )

        self.console.print(panel)
        self.console.print()

    def mostrar_menu_principal(self) -> int:
        """
        Muestra el menú principal y obtiene la selección del usuario.

        Returns:
            int: Opción seleccionada por el usuario
        """

        menu_text = Text()
        menu_text.append("🔹 MENÚ PRINCIPAL 🔹\n\n", style="bold cyan")

        opciones = [
            "1. Ver catálogo completo",
            "2. Buscar muebles",
            "3. Filtrar por precio",
            "4. Filtrar por material",
            "5. Ver comedores disponibles",
            "6. Realizar venta",
            "7. Ver estadísticas",
            "8. Generar reporte de inventario",
            "9. Aplicar descuentos",
            "0. Salir",
        ]

        for opcion in opciones:
            menu_text.append(f"{opcion}\n", style="green")

        panel = Panel(
            menu_text,
            title="Opciones Disponibles",
            border_style="yellow",
            padding=(1, 2),
        )

        self.console.print(panel)

        try:
            opcion = IntPrompt.ask(
                "Selecciona una opción", choices=[str(i) for i in range(0, 10)]
            )
            return opcion
        except ValueError:
            self.console.print("[red]Opción inválida. Intenta de nuevo.[/red]")
            return self.mostrar_menu_principal()
