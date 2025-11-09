# AR Airplane Shooter - Derriba Aviones

Un juego de realidad aumentada (WebXR/AR) donde puedes derribar aviones virtuales que vuelan a tu alrededor.

## Características

- **Realidad Aumentada**: Utiliza WebXR API para experiencias AR inmersivas
- **Gráficos 3D**: Aviones modelados en 3D con Three.js
- **Sistema de Puntuación**: Gana puntos por cada avión derribado
- **Modo Fallback**: Si AR no está disponible, funciona en modo 3D normal
- **Responsive**: Se adapta a diferentes tamaños de pantalla

## Cómo Jugar

1. Abre el archivo `index.html` en un navegador compatible con WebXR
2. Haz clic en "Iniciar AR" para comenzar
3. Apunta con la mira en el centro de la pantalla
4. Toca o haz clic para disparar
5. Derriba todos los aviones que puedas

## Requisitos

- Navegador compatible con WebXR (Chrome, Edge, Safari en iOS)
- Para AR: Dispositivo con soporte AR (Android ARCore o iOS ARKit)
- Conexión a internet (para cargar Three.js desde CDN)

## Tecnologías Utilizadas

- **WebXR API**: Para realidad aumentada
- **Three.js**: Motor de gráficos 3D
- **JavaScript ES6+**: Lógica del juego
- **HTML5/CSS3**: Interfaz de usuario

## Controles

- **Clic/Toque**: Disparar
- **Movimiento del dispositivo**: Apuntar (en modo AR)

## Puntuación

- Cada avión derribado: +100 puntos
- Intenta conseguir la mayor puntuación posible

## Compatibilidad

El juego funciona en dos modos:
1. **Modo AR**: Si tu dispositivo soporta WebXR
2. **Modo 3D Normal**: Si AR no está disponible

## Deploy

Simplemente sube el archivo `index.html` a cualquier servidor web o abre directamente en tu navegador.

Para GitHub Pages:
1. Ve a Settings > Pages
2. Selecciona la rama y guarda
3. Accede a tu juego en: `https://tu-usuario.github.io/tu-repo/`

## Licencia

MIT

## Autor

Creado con Claude Code
