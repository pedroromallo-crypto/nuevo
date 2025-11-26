from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

# ==========================================
# 🔑 CLAVES DESDE VARIABLES DE ENTORNO (.env)
# ==========================================
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

if not HEYGEN_API_KEY:
    raise ValueError("⚠️ HEYGEN_API_KEY no configurada. Crea un archivo .env con tus claves.")
if not CLAUDE_API_KEY:
    raise ValueError("⚠️ CLAUDE_API_KEY no configurada. Crea un archivo .env con tus claves.")

# ==========================================

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/get-heygen-key', methods=['GET'])
def get_heygen_key():
    try:
        resp = requests.post("https://api.heygen.com/v1/streaming.create_token", headers={"x-api-key": HEYGEN_API_KEY})
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    # Chat simple de prueba
    return jsonify({'success': True, 'response': "Hola. Si me escuchas, el navegador ya no me está bloqueando."})

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Avatar Desbloqueado</title>
    <meta charset="UTF-8">
    <style>
        body { background: #1a1a1a; color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }
        #video-container {
            width: 100%; max-width: 600px; height: 350px;
            background: #000; margin: 20px auto; border: 2px solid #444;
            position: relative;
        }
        video { width: 100%; height: 100%; object-fit: cover; }
        #logs {
            text-align: left; background: #000; border: 1px solid #333;
            padding: 10px; height: 150px; overflow-y: auto; color: #0f0;
            font-family: monospace; font-size: 12px; margin: 0 auto; max-width: 600px;
        }
        button {
            padding: 15px 30px; font-size: 18px; cursor: pointer;
            background: #007bff; color: white; border: none; border-radius: 5px;
            margin-top: 10px;
        }
        button:disabled { background: #555; cursor: not-allowed; }
        .permission-msg { color: yellow; font-weight: bold; margin-bottom: 10px; display: none; }
        .warning { color: #ff6b6b; padding: 10px; margin: 10px auto; max-width: 600px; border: 2px solid #ff6b6b; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🔓 PRUEBA CON PERMISOS</h1>

    <div id="https-warning" class="warning" style="display: none;">
        ⚠️ ADVERTENCIA: Debes acceder vía <strong>https://</strong> o <strong>http://localhost:5000</strong><br>
        Si accedes por IP (192.168.x.x), los permisos serán bloqueados por el navegador.
    </div>

    <div id="perm-alert" class="permission-msg">⚠️ POR FAVOR, DALE A "PERMITIR" CUANDO EL NAVEGADOR TE PREGUNTE</div>

    <button id="btn" onclick="startWithPermissions()">🔴 1. PEDIR PERMISOS Y CONECTAR</button>

    <div id="video-container">
        <video id="avatar-video" autoplay playsinline muted></video>
    </div>

    <div id="logs">Esperando...</div>

    <script type="module">
        import StreamingAvatar, { TaskType } from "https://cdn.jsdelivr.net/npm/@heygen/streaming-avatar@1.0.0/+esm";

        const logDiv = document.getElementById('logs');
        function log(msg) {
            const timestamp = new Date().toLocaleTimeString();
            logDiv.innerHTML += `<div>[${timestamp}] ${msg}</div>`;
            logDiv.scrollTop = logDiv.scrollHeight;
        }

        // Verificar si estamos en contexto seguro
        window.addEventListener('load', () => {
            const isSecure = window.isSecureContext;
            const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

            if (!isSecure && !isLocalhost) {
                document.getElementById('https-warning').style.display = 'block';
                log('⚠️ CONTEXTO NO SEGURO: Los permisos pueden ser bloqueados');
            } else {
                log('✅ Contexto seguro detectado');
            }
        });

        window.startWithPermissions = async () => {
            const btn = document.getElementById('btn');
            const alert = document.getElementById('perm-alert');

            btn.disabled = true;

            try {
                // PASO 1: VERIFICAR DISPONIBILIDAD
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    throw new Error("getUserMedia no está disponible en este navegador/contexto");
                }

                // PASO 2: PEDIR PERMISOS AL NAVEGADOR
                log("🔒 1. Solicitando acceso a Micrófono/Cámara...");
                alert.style.display = 'block';

                // Esto hará saltar la ventanita del navegador
                const stream = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: true
                });

                log(`🎤 Permisos obtenidos: ${stream.getTracks().length} tracks`);

                // Una vez nos da permiso, paramos nuestra cámara (no la necesitamos, solo queríamos el permiso)
                stream.getTracks().forEach(track => {
                    log(`🛑 Deteniendo ${track.kind}: ${track.label}`);
                    track.stop();
                });

                log("🔓 ¡PERMISO CONCEDIDO! El navegador ahora confía en nosotros.");
                alert.style.display = 'none';

                // PASO 3: CONECTAR CON HEYGEN
                await connectHeyGen();

            } catch (err) {
                log("❌ ERROR DE PERMISOS: " + err.name);
                log("Detalle: " + err.message);

                if (err.name === 'NotAllowedError') {
                    log("💡 Usuario denegó el permiso o navegador bloqueó la solicitud");
                } else if (err.name === 'NotFoundError') {
                    log("💡 No se encontró micrófono/cámara");
                } else if (err.name === 'NotSupportedError') {
                    log("💡 Contexto no seguro - usa HTTPS o localhost");
                }

                btn.disabled = false;
                alert.style.display = 'none';
            }
        };

        async function connectHeyGen() {
            try {
                log("🔑 2. Pidiendo token a HeyGen...");
                const r = await fetch('/api/get-heygen-key');
                const d = await r.json();

                if (d.error) {
                    throw new Error("Error del servidor: " + d.error);
                }

                if (!d.data || !d.data.token) {
                    throw new Error("Token no recibido. Respuesta: " + JSON.stringify(d));
                }

                log("📡 3. Iniciando conexión WebRTC con HeyGen...");
                const avatar = new StreamingAvatar({ token: d.data.token });

                avatar.on('STREAM_READY', (event) => {
                    log("🎥 ¡SEÑAL DE VIDEO RECIBIDA!");
                    const vid = document.getElementById('avatar-video');
                    vid.srcObject = event.detail;

                    // Quitar muted para escuchar audio
                    vid.muted = false;

                    vid.play()
                        .then(() => log("▶️ Video reproduciendo correctamente"))
                        .catch(e => {
                            log("⚠️ Error al reproducir: " + e.message);
                            log("💡 Clickea el vídeo para activar sonido");
                        });
                });

                avatar.on('STREAM_DISCONNECTED', () => {
                    log("📡 Conexión WebRTC cerrada");
                });

                avatar.on('ERROR', (error) => {
                    log("❌ Error del avatar: " + JSON.stringify(error));
                });

                // USAMOS EL AVATAR 'EXPRESSIVE' QUE SABEMOS QUE VA MEJOR
                log("🎭 4. Creando avatar...");
                await avatar.createStartAvatar({
                    quality: 'low',
                    avatarName: 'Abigail_expressive_2024112501',
                    voice: { voiceId: '1d86327d9e75485da258c3e5b868020e' }
                });

                log("✅ Avatar creado. Esperando stream de video...");

            } catch (e) {
                log("❌ Error en conexión HeyGen: " + e.message);
                log("Stack: " + (e.stack || 'No disponible'));
                document.getElementById('btn').disabled = false;
            }
        }

        // Permitir unmute con click en el video
        document.getElementById('avatar-video').addEventListener('click', (e) => {
            const vid = e.target;
            vid.muted = false;
            vid.play();
            log("🔊 Audio activado por click del usuario");
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    # IMPORTANTE: Para producción, usar certificado SSL
    app.run(debug=True, host='0.0.0.0', port=5000)
