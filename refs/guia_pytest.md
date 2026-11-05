# Guía Completa de `pytest`

[`pytest`](https://docs.pytest.org/en/stable/) es un **framework de testing en Python** diseñado para facilitar la escritura, ejecución y mantenimiento de pruebas automatizadas. Se destaca por su **sintaxis simple y expresiva**, que permite crear desde **pruebas unitarias básicas** hasta **suites complejas de integración o funcionales** sin necesidad de código boilerplate.

Además de su facilidad de uso, `pytest` ofrece un **ecosistema robusto de plugins** que amplía sus capacidades —por ejemplo, para la generación de reportes, el manejo de pruebas parametrizadas, la ejecución paralela, la simulación de entornos, y la integración con herramientas de CI/CD.

# Características principales

## 1. Auto-descubrimiento de Tests

`pytest` cuenta con un potente mecanismo de **auto-descubrimiento**, que le permite **detectar y ejecutar automáticamente las pruebas** presentes en un proyecto **sin requerir configuración adicional**.

Por defecto, `pytest` busca y reconoce archivos, clases y funciones que sigan ciertas **convenciones de nomenclatura**:

* Los archivos de prueba deben tener nombres que comiencen o terminen con `test` (por ejemplo, `test_example.py` o `example_test.py`).
* Las funciones de prueba deben comenzar con `test_` (por ejemplo, `test_suma()` o `test_usuario_valido()`).
* Las clases de prueba deben comenzar con `Test` y no requerir herencia explícita de `unittest.TestCase`.

Cuando se ejecuta el comando `pytest`, el framework **recorre recursivamente el directorio actual**, identifica los archivos y funciones que cumplen con esas convenciones, y **construye automáticamente la suite de pruebas a ejecutar**.

Este comportamiento elimina la necesidad de mantener listas manuales de tests o archivos de configuración complicados, lo que **simplifica el proceso de desarrollo** y **favorece la escalabilidad** a medida que el proyecto crece.

### Ejemplo Detallado

```python
# tests/test_calculadora.py
def test_suma():
    """Esta función será descubierta automáticamente"""
    assert 1 + 1 == 2

class TestCalculadora:
    """Esta clase será descubierta automáticamente"""

    def test_multiplicacion(self):
        """Este método será descubierto automáticamente"""
        assert 2 * 3 == 6

    def test_division(self):
        assert 6 / 2 == 3

# ❌ Esto NO será descubierto como test
def helper_function():
    """Función auxiliar - no comienza con 'test_'"""
    return 42

class HelperClass:
    """Clase auxiliar - no comienza con 'Test'"""
    def some_method(self):
        pass
```

### Configuración Personalizada

Puedes personalizar el descubrimiento mediante `pytest.ini`:

```ini
# pytest.ini
[pytest]
python_files = check_*.py        # Cambia el patrón de archivos
python_classes = *Test           # Cambia el patrón de clases  
python_functions = *_test        # Cambia el patrón de funciones
```

### Ventajas del Auto-descubrimiento

- **Cero configuración**: Funciona inmediatamente después de la instalación
- **Convención sobre configuración**: Sigue estándares de la comunidad
- **Flexibilidad**: Permite personalización cuando es necesario
- **Consistencia**: Mismo comportamiento en todos los proyectos

## 2. Sintaxis Simple con Assertions Estándar

Una de las características más atractivas de `pytest` es su **sintaxis minimalista y expresiva**, que permite escribir pruebas claras utilizando el **`assert` estándar de Python**.

A diferencia de otros frameworks que requieren métodos específicos para verificar condiciones (como `self.assertEqual()` o `self.assertTrue()` en `unittest`), `pytest` **se integra directamente con el propio lenguaje**, lo que hace que las pruebas sean **más legibles, naturales y fáciles de mantener**, por ejemplo:

```python
def test_suma():
    resultado = 2 + 3
    assert resultado == 5
```

Sin embargo, `pytest` no se limita a ejecutar el `assert` como lo haría Python de forma nativa. Cuando una aserción falla, el framework **analiza automáticamente la expresión** y muestra un **mensaje de error enriquecido**, indicando los valores de cada parte de la comparación.

Esta **retroalimentación detallada** facilita la depuración y reduce el tiempo necesario para identificar la causa del fallo. En resumen, `pytest` combina la **simplicidad del `assert` nativo** con **diagnósticos inteligentes**, ofreciendo una experiencia de testing potente y fluida.

### Comparación: `unittest` vs. `pytest`

```python
# ❌ unittest - assertions verbosas
import unittest

class TestMath(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(1 + 1, 2)
        self.assertTrue(1 < 2)
        self.assertIn(1, [1, 2, 3])

# ✅ pytest - assertions simples y naturales
def test_equality():
    assert 1 + 1 == 2
    assert 1 < 2
    assert 1 in [1, 2, 3]
```

### Mejoras Inteligentes en Assertions

```python
def test_comparaciones_complejas():
    lista_obtenida = [1, 2, 3, 4, 5]
    lista_esperada = [1, 2, 4, 4, 5]  # Diferencia en el índice 2

    # pytest muestra una diff detallada automáticamente
    assert lista_obtenida == lista_esperada

def test_diccionarios():
    resultado = {"a": 1, "b": 2, "c": 3}
    esperado = {"a": 1, "b": 999, "c": 3}  # Diferencia en clave 'b'

    # pytest muestra diferencias específicas entre diccionarios
    assert resultado == esperado

def test_strings():
    texto_largo = "Este es un texto muy largo con algunas diferencias"
    texto_esperado = "Este es un texto muy LARGO con algunas diferencias"

    # pytest resalta diferencias en strings largos
    assert texto_largo == texto_esperado
```

### Assertions Avanzadas con Mensajes Personalizados

```python
def test_con_mensaje_error():
    resultado = calcular_precio(producto="laptop", impuestos=True)
    esperado = 1200

    assert resultado == esperado, f"Precio incorrecto. Esperado: {esperado}, Obtenido: {resultado}"

def test_condiciones_complejas():
    usuario = obtener_usuario_por_id(123)

    # Múltiples assertions con mensajes claros
    assert usuario is not None, "Usuario no debería ser None"
    assert usuario.activo, "Usuario debería estar activo"
    assert len(usuario.emails) > 0, "Usuario debería tener al menos un email"
```

### Soporte para Excepciones

```python
import pytest

def test_excepciones_especificas():
    with pytest.raises(ValueError) as exc_info:
        int("no_es_un_numero")

    # Puedes verificar el mensaje de error
    assert "invalid literal" in str(exc_info.value).lower()

def test_excepciones_con_mensaje_especifico():
    with pytest.raises(ValueError, match=".*invalid literal.*"):
        int("no_es_un_numero")
```

## 3. Fixtures para Configuración Reusable

Una *fixture* es una **función especial** y esuno de los componentes más potentes y distintivos de `pytest`. Se utiliza para **proveer datos, estado o configuraciones previas** a uno o varios tests, permitiendo así **reutilizar código de inicialización o limpieza** de manera estructurada y eficiente.

En lugar de repetir la misma preparación en cada prueba —por ejemplo, crear una conexión a base de datos, inicializar objetos o cargar datos de prueba—, las fixtures permiten **definir ese comportamiento una sola vez** y dejar que `pytest` se encargue de **inyectarlo automáticamente** en las pruebas que lo necesiten.

Por ejemplo:

```python
import pytest

@pytest.fixture
def usuario():
    return {"nombre": "Ana", "edad": 28}

def test_usuario_valido(usuario):
    assert usuario["edad"] > 18
```

En este ejemplo, la función `usuario()` actúa como una fixture. Al declarar el parámetro `usuario` en el test `test_usuario_valido`, `pytest` **detecta la dependencia y ejecuta la fixture antes de la prueba**, pasando su resultado como argumento.

Las fixtures pueden además:

* **Encadenarse** (una fixture puede depender de otra).
* Tener **alcance configurable** (`function`, `class`, `module`, `session`).
* Ejecutar **acciones de limpieza o teardown** mediante el uso de `yield`.
* Ser **compartidas globalmente** a través del archivo `conftest.py`.

En resumen, las fixtures permiten que las pruebas sean **más limpias, modulares y mantenibles**, al centralizar la lógica de configuración y aislar los tests del código repetitivo.

### Anatomía de una Fixture

```python
import pytest

@pytest.fixture
def usuario_activo():
    """Fixture simple - setup y return"""
    usuario = Usuario(nombre="Ana", activo=True)
    return usuario

@pytest.fixture
def base_datos():
    """Fixture con setup y teardown usando yield"""
    # Setup
    db = Database()
    db.conectar()
    db.inicializar_datos_prueba()

    # Proporcionar el recurso al test
    yield db

    # Teardown (siempre se ejecuta)
    db.limpiar()
    db.desconectar()

@pytest.fixture(scope="session")
def configuracion_global():
    """Fixture con alcance de sesión - se ejecuta una vez por ejecución"""
    config = cargar_configuracion_test()
    return config
```

### Alcances (Scopes) de Fixtures

```python
@pytest.fixture(scope="function")   # Por defecto - una por test function
def fixture_funcion():
    return "nueva_instancia_por_test"

@pytest.fixture(scope="class")      # Una por clase de test
def fixture_clase():
    return "misma_instancia_para_toda_la_clase"

@pytest.fixture(scope="module")     # Una por módulo
def fixture_modulo():
    return "misma_instancia_para_todo_el_archivo"

@pytest.fixture(scope="session")    # Una por ejecución completa
def fixture_sesion():
    return "misma_instancia_para_toda_la_sesión"
```

### Fixtures con Dependencias

```python
import pytest

@pytest.fixture
def configuracion():
    return {"host": "localhost", "puerto": 5432}

@pytest.fixture
def conexion_db(configuracion):  # Depende de la fixture 'configuracion'
    conn = connect_to_database(configuracion["host"], configuracion["puerto"])
    yield conn
    conn.close()

@pytest.fixture
def repositorio_usuarios(conexion_db):  # Depende de 'conexion_db'
    return UserRepository(conexion_db)

# Uso en tests
def test_crear_usuario(repositorio_usuarios):
    usuario = repositorio_usuarios.crear(nombre="Carlos")
    assert usuario.id is not None
```

### Fixtures Autouse (Automáticas)

```python
@pytest.fixture(autouse=True)
def log_test_ejecucion():
    """Se ejecuta automáticamente para cada test sin necesidad de declararlo"""
    print(f"\nIniciando test...")
    start_time = time.time()
    yield
    duration = time.time() - start_time
    print(f"Test completado en {duration:.2f}s")

def test_algo():
    # La fixture autouse se ejecuta automáticamente
    assert True
```

### Fixtures con Parámetros

```python
@pytest.fixture(params=["usuario1", "usuario2", "admin"])
def usuario_con_rol(request):
    """Se ejecuta una vez por cada parámetro"""
    return Usuario(nombre=request.param, rol=request.param)

def test_acceso_segun_rol(usuario_con_rol):
    # Este test se ejecutará 3 veces, una por cada usuario
    if usuario_con_rol.rol == "admin":
        assert usuario_con_rol.tiene_acceso_total()
    else:
        assert not usuario_con_rol.tiene_acceso_total()
```

## 4. Parametrización para Ejecutar Tests con Múltiples Datos

`pytest` permite **parametrizar pruebas**, es decir, ejecutar el mismo test varias veces con **diferentes conjuntos de datos** sin duplicar código.
Esta característica es especialmente útil para validar una misma función o comportamiento bajo múltiples condiciones o entradas.

La parametrización se realiza con el decorador `@pytest.mark.parametrize`, donde se especifican los nombres de los parámetros y los valores que se probarán:

```python
import pytest

@pytest.mark.parametrize("a, b, resultado", [
    (2, 3, 5),
    (1, 1, 2),
    (5, 5, 10)
])
def test_suma(a, b, resultado):
    assert a + b == resultado
```

En este ejemplo, `pytest` ejecutará el test **tres veces**, una por cada conjunto de valores.

Cada ejecución se reporta por separado, lo que facilita **identificar rápidamente qué combinación falló** en caso de error.

Gracias a la parametrización, las pruebas se vuelven **más compactas, expresivas y completas**, favoreciendo la cobertura de distintos escenarios con un esfuerzo mínimo.

### Parametrización Básica

```python
import pytest

@pytest.mark.parametrize("entrada,esperado", [
    (1, 2),    # Test case 1: entrada=1, esperado=2
    (5, 6),    # Test case 2: entrada=5, esperado=6  
    (-1, 0),   # Test case 3: entrada=-1, esperado=0
])
def test_incremento(entrada, esperado):
    assert entrada + 1 == esperado
```

### Parametrización con Múltiples Parámetros

```python
@pytest.mark.parametrize("a,b,operacion,resultado", [
    (2, 3, "suma", 5),
    (5, 3, "resta", 2),
    (4, 2, "multiplicacion", 8),
    (10, 2, "division", 5),
])
def test_operaciones_matematicas(a, b, operacion, resultado):
    if operacion == "suma":
        assert a + b == resultado
    elif operacion == "resta":
        assert a - b == resultado
    elif operacion == "multiplicacion":
        assert a * b == resultado
    elif operacion == "division":
        assert a / b == resultado
```

### Combinación de Fixtures y Parametrización

```python
@pytest.fixture(params=[1, 2, 3])
def numero(request):
    return request.param

@pytest.mark.parametrize("multiplicador", [10, 100])
def test_multiplicacion_combinada(numero, multiplicador):
    resultado = numero * multiplicador
    assert resultado == numero * multiplicador
    # Este test se ejecutará 3 (números) × 2 (multiplicadores) = 6 veces
```

### Parametrización con IDs Legibles

```python
@pytest.mark.parametrize(
    "entrada,esperado",
    [
        (0, "cero"),
        (1, "uno"),
        (5, "cinco"),
        (10, "diez")
    ],
    ids=["caso_cero", "caso_uno", "caso_cinco", "caso_diez"]
)
def test_convertir_numero_a_texto(entrada, esperado):
    # Los IDs aparecen en la salida de pytest para identificar cada caso
    resultado = convertir_numero(entrada)
    assert resultado == esperado
```

### Parametrización Indirecta

```python
@pytest.fixture
def usuario(request):
    # request.param viene de la parametrización
    return Usuario(nombre=request.param["nombre"], edad=request.param["edad"])

@pytest.mark.parametrize(
    "usuario,esperado",
    [
        ({"nombre": "Ana", "edad": 25}, True),
        ({"nombre": "Luis", "edad": 17}, False),
    ],
    indirect=["usuario"]  # Indica que estos parámetros van a la fixture
)
def test_usuario_es_mayor_de_edad(usuario, esperado):
    assert usuario.es_mayor_de_edad() == esperado
```

## 5. Extensible mediante Plugins

Una de las mayores fortalezas de `pytest` es su **arquitectura modular y extensible**, que permite **ampliar sus capacidades mediante plugins**.

Los plugins son componentes adicionales que pueden **modificar, complementar o automatizar** el comportamiento del framework sin alterar su núcleo.

Existen **cientos de plugins disponibles** en la comunidad que cubren múltiples necesidades, como:

* **Ejecución paralela de pruebas** (`pytest-xdist`)
* **Generación de reportes HTML** (`pytest-html`)
* **Simulación de entornos o dependencias externas** (`pytest-mock`, `pytest-django`, `pytest-flask`)
* **Control de tiempo de ejecución** (`pytest-timeout`)

Además, `pytest` permite **crear plugins personalizados**, ya sea para uso interno de un proyecto o para compartir con otros desarrolladores. Estos plugins se integran fácilmente a través del archivo `conftest.py` o como paquetes instalables.

La arquitectura de `pytest` se basa en un sistema de **hooks** (puntos de extensión), que ofrece a los desarrolladores **control total sobre el ciclo de vida de las pruebas**, desde su descubrimiento hasta la generación de resultados.

### Plugins Populares y sus Funcionalidades

#### pytest-cov - Cobertura de Código

```bash
# Instalación
pip install pytest-cov

# Uso
pytest --cov=mi_modulo tests/
pytest --cov-report=html --cov=mi_modulo tests/
```

#### pytest-xdist - Ejecución Paralela

```bash
# Instalación  
pip install pytest-xdist

# Ejecutar tests en paralelo
pytest -n 4 tests/           # 4 workers
pytest -n auto tests/        # Número automático de workers
```

#### pytest-mock - Integración con unittest.mock

```python
import pytest

def test_con_mock(mocker):  # Fixture proporcionada por pytest-mock
    # Mock de una función
    mocker.patch("modulo.funcion_externa", return_value=42)

    # Mock de un método de clase
    mock_instance = mocker.Mock()
    mocker.patch("modulo.Clase", return_value=mock_instance)

    # Verificaciones
    mock_instance.metodo.assert_called_once()
```

#### pytest-django - Soporte para Django

```python
# tests/test_views.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_vista_inicio(client):
    response = client.get(reverse('inicio'))
    assert response.status_code == 200
    assert 'Bienvenido' in str(response.content)

def test_modelo_usuario(usuario):  # Fixture proporcionada por pytest-django
    assert usuario.username == "testuser"
```

#### pytest-asyncio - Soporte para Async/Await

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_operacion_asincrona():
    resultado = await operacion_asincrona()
    assert resultado == "esperado"

@pytest.mark.asyncio  
async def test_multiple_async():
    resultado1, resultado2 = await asyncio.gather(
        tarea1(),
        tarea2()
    )
    assert resultado1 == "ok"
    assert resultado2 == "ok"
```

### Creación de Plugins Personalizados

```python
# conftest.py - Plugin personalizado para el proyecto

def pytest_configure(config):
    """Hook de configuración de pytest"""
    print("Configurando pytest...")

@pytest.fixture
def mi_fixture_personalizada():
    """Fixture disponible globalmente en el proyecto"""
    return "valor_personalizado"

def pytest_generate_tests(metafunc):
    """Hook para generar tests dinámicamente"""
    if "datos_dinamicos" in metafunc.fixturenames:
        metafunc.parametrize("datos_dinamicos", [
            "caso1", "caso2", "caso3"
        ])

# Ahora en cualquier test del proyecto:
def test_con_fixture_personalizada(mi_fixture_personalizada):
    assert mi_fixture_personalizada == "valor_personalizado"
```

### Hooks de pytest para Extensión

```python
# conftest.py
def pytest_runtest_setup(item):
    """Se ejecuta antes de cada test"""
    print(f"Preparando test: {item.name}")

def pytest_runtest_teardown(item, nextitem):
    """Se ejecuta después de cada test"""
    print(f"Finalizando test: {item.name}")

def pytest_collection_modifyitems(config, items):
    """Modifica la colección de tests recolectados"""
    # Reordenar tests, saltar algunos, etc.
    for item in items:
        if "lento" in item.nodeid:
            item.add_marker(pytest.mark.slow)
```

### Ventajas de la Arquitectura de Plugins

- **Modularidad**: Cada plugin se enfoca en una funcionalidad específica
- **Reutilización**: Los plugins pueden usarse en múltiples proyectos
- **Comunidad**: Gran ecosistema de plugins mantenidos por la comunidad
- **Personalización**: Fácil creación de plugins específicos para tu proyecto

# Mejores Prácticas

## 1. Organización de Tests

**Estructura recomendada:**

`pytest` busca automáticamente:

- Archivos que coincidan con: test_*.py o *_test.py
- Funciones que comiencen con: test_
- Clases que comiencen con: Test (y métodos que comiencen con test_)

✅ Serán descubiertos automáticamente:

```text
tests/
├── test_calculadora.py
├── database_test.py
├── test_models.py
└── test_services.py
```

## 2. Nombrado Descriptivo

```python
# ✅ Bueno
def test_calcular_impuesto_usuario_premium():
    ...

def test_login_con_credenciales_invalidas_lanza_excepcion():
    ...

# ❌ Evitar
def test1():
    ...

def test_thing():
    ...
```

## 3. Tests Aislados e Independientes

```python
# ✅ Cada test debe poder ejecutarse independientemente
def test_crear_usuario():
    usuario = Usuario.crear("test@example.com")
    assert usuario.email == "test@example.com"

def test_eliminar_usuario():
    usuario = Usuario.crear("eliminar@example.com")
    usuario.eliminar()
    assert not usuario.existe()
```

## 4. Usar Fixtures para Dependencias Comunes

```python
import pytest

@pytest.fixture
def configuracion_test():
    return {
        "api_url": "https://api.test.com",
        "timeout": 30,
        "intentos": 3
    }

@pytest.fixture
def cliente_api(configuracion_test):
    return APICliente(configuracion_test)

def test_api_llamada_exitosa(cliente_api):
    respuesta = cliente_api.obtener_datos()
    assert respuesta.estado == 200
```

## 5. Mantener Tests Simples y Legibles

```python
# ✅ Claro y legible
def test_procesar_pedido():
    # Setup
    pedido = Pedido(items=["item1", "item2"])
    inventario = Inventario.disponible()

    # Action
    resultado = pedido.procesar(inventario)

    # Assert
    assert resultado.estado == "completado"
    assert len(resultado.items_procesados) == 2

# ❌ Demasiado complejo
def test_pedido_complejo():
    # ... 50 líneas de código
```

## 6. Usar Marcadores (Markers)

```python
import pytest

@pytest.mark.slow
def test_procesamiento_masivo():
    # Test que tarda mucho tiempo
    ...

@pytest.mark.integration
def test_integracion_externa():
    # Test que requiere servicios externos
    ...

@pytest.mark.skip(reason="Bug #123 pendiente de fix")
def test_funcionalidad_rota():
    ...
```

## 7. Mocking de Dependencias Externas

```python
import pytest
from unittest.mock import Mock, patch

def test_envio_email():
    mock_smtp = Mock()

    with patch('modulo.email.SMTP', return_value=mock_smtp):
        enviar_email("test@example.com", "Hola")

    mock_smtp.enviar.assert_called_once()
```

# Ejemplos de Código

## Ejemplo 1: Fixture con Setup y Teardown

```python
import pytest
import tempfile
import os

@pytest.fixture
def archivo_temporal():
    # Setup
    archivo = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    archivo.write("contenido de prueba")
    archivo.close()

    yield archivo.name  # Proporciona el path al test

    # Teardown
    if os.path.exists(archivo.name):
        os.unlink(archivo.name)

def test_lectura_archivo(archivo_temporal):
    with open(archivo_temporal, 'r') as f:
        contenido = f.read()
    assert contenido == "contenido de prueba"
```

## Ejemplo 2: Parametrización Avanzada

```python
import pytest

def es_par(numero):
    return numero % 2 == 0

@pytest.mark.parametrize("numero,esperado", [
    (2, True),
    (3, False),
    (0, True),
    (-2, True),
    (-3, False),
])
def test_es_par(numero, esperado):
    assert es_par(numero) == esperado
```

## Ejemplo 3: Fixtures con Dependencias

```python
import pytest

@pytest.fixture
def usuario_base():
    return {"nombre": "usuario", "rol": "user"}

@pytest.fixture
def usuario_admin(usuario_base):
    usuario_base["rol"] = "admin"
    usuario_base["permisos"] = ["leer", "escribir", "eliminar"]
    return usuario_base

def test_usuario_admin(usuario_admin):
    assert usuario_admin["rol"] == "admin"
    assert "eliminar" in usuario_admin["permisos"]
```

## Ejemplo 4: Tests con Excepciones

```python
import pytest

class SaldoInsuficienteError(Exception):
    pass

class CuentaBancaria:
    def __init__(self, saldo_inicial=0):
        self.saldo = saldo_inicial

    def retirar(self, monto):
        if monto > self.saldo:
            raise SaldoInsuficienteError("Saldo insuficiente")
        self.saldo -= monto

def test_retiro_saldo_insuficiente():
    cuenta = CuentaBancaria(100)
    with pytest.raises(SaldoInsuficienteError) as exc_info:
        cuenta.retirar(200)

    assert "Saldo insuficiente" in str(exc_info.value)
    assert cuenta.saldo == 100  # El saldo no cambió
```

## Ejemplo 5: Configuración con pytest.ini

```ini
# pytest.ini
[tool:pytest]
addopts = -v --tb=short
markers =
    slow: tests que toman mucho tiempo
    integration: tests de integración
    smoke: tests críticos básicos
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

# Conclusiones

pytest es una herramienta poderosa que, cuando se usa siguiendo estas mejores prácticas, puede mejorar significativamente la calidad y mantenibilidad de tus tests:

1. **Sigue las convenciones** para minimizar configuración
2. **Organiza tus tests** lógicamente
3. **Usa fixtures** para código reusable
4. **Mantén los tests simples** y enfocados
5. **Parametriza** cuando sea posible
6. **Aísla los tests** entre sí
7. **Usa mocking** para dependencias externas

La inversión en escribir buenos tests con pytest se traduce en código más robusto, menos bugs y mayor confianza en los despliegues.

# Comandos Útiles

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests específicos
pytest tests/test_modulo.py::test_funcion_especifica

# Ejecutar con cobertura
pytest --cov=mi_modulo

# Ejecutar tests marcados como "slow"
pytest -m slow

# Ejecutar tests y generar reporte HTML
pytest --html=report.html
```
