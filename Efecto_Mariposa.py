import os
import flet as ft
import requests
import random
import time

API_KEY = os.environ.get("GROQ_API_KEY")

FRASES = [
    "ðŸ§žâ€â™‚ï¸ El OrÃ¡culo estÃ¡ brillando...",
    "ðŸ”® Las runas se estÃ¡n alineando...",
    "âœ¨ El destino estÃ¡ tejiendo tu respuesta...",
    "ðŸŒ™ La sabidurÃ­a ancestral se activa...",
    "âš¡ El OrÃ¡culo del DominÃ³ estÃ¡ respondiendo...",
    "ðŸŽ© Â¡El velo del futuro se levanta!...",
    "ðŸŒŸ Una visiÃ³n estÃ¡ por llegar...",
    "ðŸŒ€ Las consecuencias se despliegan...",
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
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "system", "content": "Eres el OrÃ¡culo del DominÃ³. Hablas con sabidurÃ­a ancestral. Tus respuestas son profundas, claras y visuales. Te gusta usar metÃ¡foras y conexiones entre eventos."},
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
        return f"Error de conexiÃ³n: {e}"

def main(page: ft.Page):
    page.title = "ðŸ¦‹ Efecto Mariposa"
    page.favicon = "icon.png"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.DEEP_PURPLE_900
    page.padding = 15
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def is_mobile():
        return page.width < 600 if page.width else True

    def get_width(base_width):
        return min(base_width, page.width - 30) if page.width else base_width

    def explorar(e):
        pregunta = txt_pregunta.value.strip()
        if not pregunta:
            txt_respuesta.value = "âš ï¸ Escribe una pregunta, amigo."
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
        frase_oraculo.value = "ðŸ§žâ€â™‚ï¸ El OrÃ¡culo ha hablado"
        page.update()

    def limpiar(e):
        txt_pregunta.value = ""
        txt_respuesta.value = ""
        frase_oraculo.value = "ðŸ§žâ€ï¸ El OrÃ¡culo estÃ¡ listo"
        page.update()

    # --- HEADER CENTRADO Y AJUSTADO (TÃ­tulo 22, Mariposas 26) ---
    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("ðŸ¦‹", size=26),
                ft.Text("EFECTO MARIPOSA", size=22, weight="bold", color=ft.Colors.AMBER_400, text_align="center", expand=True),
                ft.Text("ðŸ¦‹", size=26),
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Text("Explora el efecto de tus decisiones", size=13, color=ft.Colors.AMBER_200, text_align="center"),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
        padding=ft.padding.symmetric(horizontal=10, vertical=15),
        border_radius=20,
        gradient=ft.LinearGradient(begin=ft.Alignment(0, -1), end=ft.Alignment(0, 1), colors=[ft.Colors.PURPLE_800, ft.Colors.DEEP_PURPLE_900]),
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.AMBER_400, offset=ft.Offset(0, 0)),
    )

    # --- CAMPO DE PREGUNTA ---
    txt_pregunta = ft.TextField(
        label="ðŸ”® Â¿QuÃ© preguntas al OrÃ¡culo?",
        hint_text="Ej: Â¿QuÃ© pasarÃ­a si aprendiera a programar?",
        multiline=False,
        width=get_width(650 if not is_mobile() else page.width - 40),
        bgcolor=ft.Colors.PURPLE_800,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.AMBER_400,
        focused_border_color=ft.Colors.AMBER_200,
        border_radius=12,
        text_size=16 if is_mobile() else 18,
        content_padding=15 if is_mobile() else 20,
        on_submit=lambda e: explorar(e),
    )

    # --- BOTONES ---
    btn_explorar = ft.Button(
        "ðŸ”® CONSULTAR AL ORÃCULO",
        on_click=explorar,
        width=get_width(260 if not is_mobile() else page.width - 40),
        height=50 if is_mobile() else 55,
        bgcolor=ft.Colors.AMBER_400,
        color=ft.Colors.DEEP_PURPLE_900,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),
            text_style=ft.TextStyle(size=16 if is_mobile() else 18, weight="bold"),
        ),
    )

    btn_limpiar = ft.OutlinedButton(
        "ðŸ§¹ Nueva pregunta",
        on_click=limpiar,
        width=get_width(160 if not is_mobile() else page.width - 40),
        height=45 if is_mobile() else 50,
        style=ft.ButtonStyle(
            side=ft.BorderSide(2, ft.Colors.AMBER_400),
            color=ft.Colors.AMBER_400,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    # --- ÃREA DE RESPUESTA ---
    txt_respuesta = ft.TextField(
        label="ðŸ§žâ€â™‚ï¸ EL ORÃCULO RESPONDE",
        multiline=True,
        min_lines=5,
        max_lines=15,
        width=get_width(650 if not is_mobile() else page.width - 40),
        bgcolor=ft.Colors.PURPLE_800,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.AMBER_400,
        focused_border_color=ft.Colors.AMBER_200,
        border_radius=12,
        read_only=True,
        text_size=14 if is_mobile() else 15,
        content_padding=15 if is_mobile() else 20,
    )

    # --- INDICADORES ---
    spinner = ft.ProgressRing(visible=False, color=ft.Colors.AMBER_400, width=30, height=30)
    frase_oraculo = ft.Text("ðŸ§žâ€ï¸ El OrÃ¡culo estÃ¡ listo", size=12 if is_mobile() else 14, color=ft.Colors.AMBER_200, italic=True, text_align="center")
    progress_bar = ft.ProgressBar(width=get_width(600), color=ft.Colors.AMBER_400, bgcolor=ft.Colors.PURPLE_800, visible=False)

    # --- PIE DE PÃGINA ---
    footer = ft.Text(
        "ðŸ§žâ€â™‚ï¸ El OrÃ¡culo del DominÃ³ â€¢ Una pregunta puede cambiarlo todo",
        size=10 if is_mobile() else 12,
        color=ft.Colors.AMBER_200,
        text_align="center",
        italic=True,
    )

    # --- LAYOUT RESPONSIVE ---
    page.add(
        ft.Column([
            header,
            ft.Container(height=10),
            txt_pregunta,
            ft.Container(height=15),
            ft.Column([
                btn_explorar,
                ft.Container(height=10),
                btn_limpiar,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            ft.Container(height=15),
            frase_oraculo,
            ft.Container(height=5),
            ft.Row([spinner, progress_bar], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Container(height=15),
            txt_respuesta,
            ft.Container(height=20),
            footer,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
    )

if __name__ == '__main__':
    ft.run(main, port=int(os.environ.get('PORT', 8080)))

