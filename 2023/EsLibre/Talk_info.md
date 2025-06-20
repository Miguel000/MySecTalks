# Introducción práctica a Runtime Security con Falco

## 🎯 Abstract

Este taller ofrece una introducción práctica a Falco, un proyecto de código abierto de la CNCF y la herramienta más empleada para la seguridad basada en llamadas al kernel. Se proporcionará a cada participante un sandbox (cluster de k3s) en el que aprenderán cómo instalar y configurar Falco para detectar y generar alertas de seguridad basadas en intrusiones en tiempo real.

La adopción de contenedores y sistemas de orquestación de los mismos - como Kubernetes - se ha incrementado considerablemente en los últimos años. La popularidad de estas plataformas las convierte en objetivos comunes para cibercriminales. Kubernetes incluye herramientas de prevención, como los Admission Controllers, control de permisos RBAC y Pod Security Admission. Sin embargo, ésto se centra en la prevención y no proporciona gran visibilidad sobre las aplicaciones en tiempo de ejecución. ¿Cómo implementar un sistema de seguridad para detectar intrusiones en tiempo real en Linux, contenedores y/o Kubernetes? En este tutorial, los instructores presentarán qué es Runtime Security y explicarán cómo detectar comportamientos sospechosos e intrusiones.

Este tutorial ofrece una introducción práctica a Falco, un proyecto de código abierto de la CNCF y la herramienta más empleada para la seguridad basada en llamadas al kernel. Se proporcionará a cada participante un sandbox (cluster de k3s) en el que aprenderán cómo instalar y configurar Falco para detectar y generar alertas de seguridad basadas en intrusiones en tiempo real.

El tutorial cubrirá los siguientes puntos, de forma eminentemente práctica:

- Runtime Security y Falco - qué son y para qué sirven.
- Instalación y configuración.
- Entrada de datos para Falco - llamadas al sistema y otros plugins.
- Filtros - Reglas de Falco.
- Alertas - Canales de notificación (Syslog, Slack, etc.).

Beneficios

Los asistentes pueden conocer Falco, pero tal vez no lo hayan usado en entornos en producción. Este tutorial está enfocado a aquellos que quieran dar sus primeros pasos con Falco para detectar amenazas en tiempo de ejecución y alertar sobre intrusiones en Linux, contenedores y Kubernetes. La estructura es la siguiente:

- Introducción a Runtime Security y conceptos básicos e instalación de Falco (teoría y lab, 30 minutos).
- Arquitectura de Falco y como activar, desactivar y extender reglas de detección (teoría y lab, 30 minutos).
- Notificaciones y visualización de alertas, integración con Slack (teoría y lab, 20 minutos)
- Cierre y preguntas (10 minutos).

Al final de esta sesión, los asistentes serán capaces de responder a las siguientes preguntas:

- ¿Qué es Runtime Security y por qué es importante?
- ¿Qué es Falco?
- ¿Cómo desplegar Falco en un cluster de Kubernetes para detectar amenazas?
- ¿Cómo emplear reglas de detección estándar para mi caso de uso particular?
- ¿Cómo detectar comportamientos sospechosos e intrusiones?
- ¿Cómo notificar sobre estos eventos de seguridad?

## 📚 Resources

- Related Blog Post: [Falco](https://falco.org/)
- Video: [Link](https://commons.wikimedia.org/wiki/File:EsLibre_2023_P46_-_Miguel_Hern%C3%A1ndez_Boza,_Vicente_J._Jim%C3%A9nez_Miras_-_Introducci%C3%B3n_pr%C3%A1ctica_a_Runtime_Security_con_Falco.webm)
