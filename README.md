# Playwright UI Testing

Framework de QA Automation para probar la interfaz de login de [Practice Test Automation](https://practicetestautomation.com/practice-test-login/) con Python, pytest y Playwright.

## Alcance y casos

La suite contiene 6 casos recopilables:

- **2 locales:** comprueban las marcas pytest y la presencia de archivos de configuración. No abren un navegador ni realizan solicitudes de red.
- **4 de integración:** verifican la carga del formulario, un login exitoso y dos variantes de credenciales inválidas. Requieren Chromium y acceso al sitio público.

El proyecto no prueba campos vacíos porque no hay un comportamiento esperado para esos campos especificado en el código o documentación disponible.

## Requisitos

- Python 3.10 o posterior.
- Python validado en el entorno local: **3.12.10**. GitHub Actions ejecuta con Python **3.12**.
- Chromium de Playwright para las pruebas de integración.
- Conexión a Internet para instalar dependencias y acceder al sitio durante integración.

Las versiones directas están fijadas en `requirements.txt`: pytest 8.4.2, Playwright 1.63.0, pytest-playwright 0.10.0 y pytest-html 4.2.0. pytest-playwright está fijado como dependencia directa, aunque estos tests conservan sus fixtures propios en `tests/conftest.py` y no usan los fixtures del plugin.

Las dependencias transitivas no están fijadas en un lockfile, así que estos pins no garantizan una instalación completamente reproducible.

## Instalación en Windows PowerShell

Desde la raíz del proyecto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
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
- `integration`: pruebas de navegador que acceden al sitio público externo.

## GitHub Actions

En cada `push` y `pull_request`, el workflow ejecuta solo las pruebas locales. Para ejecutar integración manualmente:

1. Abrí **Actions** en GitHub.
2. Elegí **UI tests**.
3. Seleccioná **Run workflow**.

La ejecución manual corre primero los tests locales y luego las pruebas de integración. El workflow instala dependencias y Chromium en Ubuntu con Python 3.12. Al finalizar, carga el reporte HTML y las capturas como artefacto `ui-test-evidence`, incluso si hay fallos. El token de Actions tiene permiso de solo lectura sobre el contenido del repositorio. No se usan secretos de GitHub en los tests.

## Evidencias y datos

Ante un fallo, `tests/conftest.py` intenta guardar una captura en `screenshots/`. La ejecución de integración en CI genera `reports/integration-report.html`. No están configuradas trazas ni grabación de video.

Se usan únicamente las credenciales públicas de demostración documentadas por el sitio (`student` / `Password123`). No uses credenciales privadas en estas pruebas: capturas, reportes o futuras trazas podrían revelar contenido visible en el navegador. `.gitignore` excluye archivos `.env`, estados de autenticación y artefactos generados.

## Limitaciones conocidas

- Las pruebas de integración dependen de un servicio público ajeno al proyecto; cambios, indisponibilidad o conectividad pueden afectar los resultados.
- Python 3.12 es la única versión ejecutada por CI; otras versiones no están validadas por el workflow.
- Los pins de dependencias directas no fijan sus dependencias transitivas.
- Los tests cubren el flujo de login de demostración, no autenticación de una aplicación bajo control del proyecto.
