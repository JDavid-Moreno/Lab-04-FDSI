# Lab-04-FDSI

## Integrantes:

- Juan David Moreno D'Aleman
- Karol Ximena Rodriguez Reyes

aplicacion sencilla para el laboratorio 4 de fundamentos de seguridad, en el cual se explotan fallos de seguridad como SQL inyection, command inyection, etc.

## Repositorio Vulnerable para Pruebas SAST

Aplicación Flask con vulnerabilidades intencionales para análisis estático de código.

## Estructura del repositorio

```
lab-04-fdsi/
│
├── app.py              -- App de código vulnerable
├── requirements.txt    -- Dependencias con versión vulnerable fija (PyYAML 5.3.1 y Flask 1.0)
└── README.md           -- Documentación y descripción del laboratorio
```

## Triage de Hallazgos

Para verlo en Snyk, tenemos el siguiente enlace:

[Analisis Snyk](https://app.snyk.io/org/karol-reyes/project/001d89a5-c1cc-4eea-93c8-f8a809939e69)

se veían estas vulnerabilidades:

![pro1](/img/pro.png)
![pro2](/img/pro2.png)
![pro3](/img/pro3.png)

---

para ver los hallazgos con Bandit toca realizar en el CMD o en GitBash:

1. Instalar bandit de python (si aún no se tiene):

    ```
    pip install bandit
    ```

2. Ingresar a la raiz del repo (Lab-04-FDSI)
3. Ejecutar el bandit

    ```
    bandit -r app.py
    ```

Con ello, se verán todos los hallazgos vulnerables encontrados en la app que se clasificaron en el documento