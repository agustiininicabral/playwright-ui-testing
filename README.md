# Playwright UI Testing

![UI tests](https://github.com/agustiininicabral/playwright-ui-testing/actions/workflows/ui-tests.yml/badge.svg)

Framework de QA Automation para probar la interfaz de login de [Practice Test Automation](https://practicetestautomation.com/practice-test-login/) con Python, pytest y Playwright.

## Alcance y casos

La suite contiene 10 tests:

- **2 locales de configuración:** comprueban los marcadores pytest y la presencia de archivos de configuración, sin navegador ni red.
- **4 locales de navegador:** prueban la carga del formulario, login exitoso y dos variantes de credenciales inválidas sobre una página fixture incluida en el repositorio. Requieren Chromium, pero no acceden a Internet.
- **4 de integración:** ejecutan los escenarios principales contra el sitio público Practice Test Automation. Requieren Chromium y acceso a Internet.

El proyecto no prueba campos vacíos porque no hay un comportamiento esperado para esos campos especificado en el código o documentación disponible.

## Requisitos

- Python 3.10 o posterior.
- Python validado en el entorno local: **3.12.10**. GitHub Actions ejecuta con Python **3.12**.
- Chromium de Playwright para las pruebas de navegador.
- Conexión a Internet para instalar dependencias y acceder al sitio durante integración.

Las dependencias directas están declaradas en `requirements.txt`; `requirements-dev.txt` agrega Ruff. `requirements-lock.txt` fija las versiones de las dependencias directas y transitivas observadas en la ejecución verificada de CI. El archivo fija versiones, pero no incluye hashes de artefactos. pytest-playwright está fijado como dependencia directa, aunque estos tests conservan sus fixtures propios en `tests/conftest.py` y no usan los fixtures del plugin.

## Instalación en Windows PowerShell

Desde la raíz del proyecto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt -c requirements-lock.txt
python -m playwright install chromium
```

## Ejecución local

Recopilar los casos sin ejecutarlos:

```powershell
python -m pytest --collect-only -q
```

Ejecutar únicamente los tests locales, sin navegador ni Internet:

```powershell
python -m pytest -m local -q
```

Ejecutar las pruebas de navegador deterministas (requiere Chromium, no Internet):

```powershell
python -m playwright install chromium
python -m pytest -m local_browser -q
```

Ejecutar solo integración (requiere Chromium e Internet):

```powershell
python -m pytest -m integration -q
```

La suite completa también incluye integración:

```powershell
python -m pytest -q
```

## Marcadores pytest

- `local`: verificaciones de estructura y configuración que no acceden al sitio.
- `local_browser`: pruebas de navegador deterministas contra la fixture local.
- `integration`: pruebas de navegador que acceden al sitio público externo.

## Checks de calidad

Ejecuta estos controles desde la raíz del repositorio:

```powershell
python -m pip check
python -m ruff format --check tests
python -m ruff check tests
```

La configuración de Ruff está en `pyproject.toml`.

## GitHub Actions

En cada `push` y `pull_request`, el workflow instala las versiones fijadas, comprueba dependencias, formato y lint, y ejecuta los tests locales y los cuatro escenarios de navegador contra la fixture incluida. Chromium se instala en CI para esas pruebas deterministas. La ejecución manual añade además los cuatro escenarios de integración contra el sitio público.

Para ejecutar integración manualmente:

1. Abrí **Actions** en GitHub.
2. Elegí **UI tests**.
3. Seleccioná **Run workflow**.

La ejecución manual corre primero los tests locales y luego las pruebas de integración. Al finalizar, carga los reportes HTML y las capturas como artefacto `ui-test-evidence`, incluso si hay fallos. El token de Actions tiene permiso de solo lectura sobre el contenido del repositorio. No se usan secretos de GitHub en los tests.

## Evidencia verificada de CI

- [Ejecución de GitHub Actions — 27 de octubre de 2026](https://github.com/agustiininicabral/playwright-ui-testing/actions/runs/40451073480): **success**.
- Pasaron los **2 tests locales** y los **4 tests de navegador deterministas** sobre la fixture incluida.
- `pip check`, formato y lint de Ruff finalizaron correctamente.
- Los 4 tests de integración contra el sitio público se ejecutan manualmente para evitar que la disponibilidad de un tercero vuelva inestable cada `push` o pull request.
- El artefacto `ui-test-evidence` incluye el reporte HTML de navegador de esa ejecución.

## Evidencias y datos

Ante un fallo, `tests/conftest.py` intenta guardar una captura en `screenshots/`. La ejecución de integración en CI genera `reports/integration-report.html`. No están configuradas trazas ni grabación de video.

Se usan únicamente las credenciales públicas de demostración documentadas por el sitio (`student` / `Password123`). No uses credenciales privadas en estas pruebas: capturas, reportes o futuras trazas podrían revelar contenido visible en el navegador. `.gitignore` excluye archivos `.env`, estados de autenticación y artefactos generados.

## Limitaciones conocidas

- Las pruebas de integración dependen de un servicio público ajeno al proyecto; cambios, indisponibilidad o conectividad pueden afectar los resultados.
- Python 3.12 es la única versión ejecutada por CI; otras versiones no están validadas por el workflow.
- Las dependencias están fijadas por versión, pero el lock no verifica hashes de artefactos.
- Los tests cubren el flujo de login de demostración, no autenticación de una aplicación bajo control del proyecto.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consultá el archivo [LICENSE](LICENSE).
