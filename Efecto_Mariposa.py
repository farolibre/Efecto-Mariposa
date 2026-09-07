import os
import flet as ft
import requests
import random
import time

API_KEY = os.environ.get("GROQ_API_KEY")

FRASES = [
    "🧞‍♂️ El Oráculo está brillando...",
    "🔮 Las runas se están alineando...",
    "✨ El destino está tejiendo tu respuesta...",
    "🌙 La sabiduría ancestral se activa...",
    "⚡ El Oráculo del Dominó está respondiendo...",
    " ¡El velo del futuro se levanta!...",
    "🌟 Una visión está por llegar...",
    "🌀 Las consecuencias se despliegan...",
]

def obtener_frase_oraculo():
    return random.choice(FRASES)

def preguntar_a_ia(pregunta):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Eres el Oráculo del Dominó. Hablas con sabiduría ancestral. Tus respuestas son profundas, claras y visuales. Te gusta usar metáforas y conexiones entre eventos."},
            {"role": "user", "content": pregunta}
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }
    try:
        r = requests.post(url, headers=headers, json=data, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"Error de conexión: {e}"

def main(page: ft.Page):
    page.title = " Efecto Mariposa"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.DEEP_PURPLE_900
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO
    
    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("🦋", size=60),
                ft.Column([
                    ft.Text("EFECTO MARIPOSA", size=36, weight="bold", color=ft.Colors.AMBER_400, text_align="center"),
                    ft.Text("Explora el efecto de tus decisiones", size=16, color=ft.Colors.AMBER_200, text_align="center"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Text("🦋", size=60),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20, border_radius=20,
        gradient=ft.LinearGradient(begin=ft.Alignment(0, -1), end=ft.Alignment(0, 1), colors=[ft.Colors.PURPLE_800, ft.Colors.DEEP_PURPLE_900]),
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.AMBER_400, offset=ft.Offset(0, 0)),
    )

    txt_pregunta = ft.TextField(
        label="🔮 ¿Qué preguntas al Oráculo? - ¿Qué pasaría si?..",
        hint_text="Ej: ¿Qué pasaría si aprendiera a programar?",
        multiline=False, width=650, bgcolor=ft.Colors.PURPLE_800, color=ft.Colors.WHITE,
        border_color=ft.Colors.AMBER_400, focused_border_color=ft.Colors.AMBER_200,
        border_radius=12, text_size=18, content_padding=20, on_submit=lambda e: explorar(e),
    )

    txt_respuesta = ft.TextField(
        label="🧞‍♂️ EL ORÁCULO RESPONDE",
        multiline=True, min_lines=5, max_lines=15, width=650, bgcolor=ft.Colors.PURPLE_800,
        color=ft.Colors.WHITE, border_color=ft.Colors.AMBER_400, focused_border_color=ft.Colors.AMBER_200,
        border_radius=12, read_only=True, text_size=15, content_padding=20,
    )

    spinner = ft.ProgressRing(visible=False, color=ft.Colors.AMBER_400)
    frase_oraculo = ft.Text("🧞‍️ El Oráculo está listo", size=14, color=ft.Colors.AMBER_200, italic=True)
    progress_bar = ft.ProgressBar(width=600, color=ft.Colors.AMBER_400, bgcolor=ft.Colors.PURPLE_800, visible=False)

    def explorar(e):
        pregunta = txt_pregunta.value.strip()
        if not pregunta:
            txt_respuesta.value = "⚠️ Escribe una pregunta, amigo."
            page.update()
            return

        spinner.visible = True
        progress_bar.visible = True
        progress_bar.value = 0
        txt_respuesta.value = ""
        frase_oraculo.value = obtener_frase_oraculo()
        page.update()

        for i in range(1, 6):
            time.sleep(0.3)
            progress_bar.value = i * 0.2
            page.update()

        respuesta = preguntar_a_ia(pregunta)

        spinner.visible = False
        progress_bar.visible = False
        txt_respuesta.value = respuesta
        frase_oraculo.value = "🧞‍️ El Oráculo ha hablado"
        page.update()

    def limpiar(e):
        txt_pregunta.value = ""
        txt_respuesta.value = ""
        frase_oraculo.value = "‍♂️ El Oráculo está listo"
        page.update()

    btn_explorar = ft.ElevatedButton(
        "🔮 CONSULTAR AL ORÁCULO", on_click=explorar, width=260, height=55,
        bgcolor=ft.Colors.AMBER_400, color=ft.Colors.DEEP_PURPLE_900,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15), text_style=ft.TextStyle(size=18, weight="bold")),
    )

    btn_limpiar = ft.OutlinedButton(
        "🧹 Nueva pregunta", on_click=limpiar, width=160, height=45,
        style=ft.ButtonStyle(side=ft.BorderSide(2, ft.Colors.AMBER_400), color=ft.Colors.AMBER_400, shape=ft.RoundedRectangleBorder(radius=12)),
    )

    footer = ft.Text("🧞‍♂️ El Oráculo del Dominó • Una pregunta puede cambiarlo todo", size=12, color=ft.Colors.AMBER_200, text_align="center", italic=True)

    page.add(
        ft.Column([
            header, ft.Container(height=10), txt_pregunta, ft.Container(height=15),
            ft.Row([btn_explorar, btn_limpiar], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Container(height=15), frase_oraculo, ft.Container(height=5),
            ft.Row([spinner, progress_bar], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Container(height=15), txt_respuesta, ft.Container(height=20), footer,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.run(main, port=int(os.environ.get('PORT', 8080)))