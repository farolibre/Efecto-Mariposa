# -*- coding: utf-8 -*-
"""
🎭 EL ORÁCULO DE LA RISA - Versión Definitiva
Efecto Mariposa • Edición Humor Absoluto
7 Personajes Épicos + Historial + Contador
"""

import os
import flet as ft
import requests
import random
import time
import json
from datetime import datetime

API_KEY = os.environ.get("GROQ_API_KEY")

# ========== LOS 7 PERSONAJES ==========
PERSONAJES = {
    "sabio_troll": {
        "nombre": "🧙‍♂️ El Sabio Troll",
        "color": ft.Colors.AMBER_400,
        "frase": "Sabiduría + Memes + Café",
        "tono": "Eres un oráculo con 1000 años que ha visto demasiado. Das respuestas profundas pero con sarcasmo y memes."
    },
    "comico_cosmico": {
        "nombre": "🌈 El Cómico Cósmico",
        "color": ft.Colors.PURPLE_400,
        "frase": "Universo + Patatas + Risas",
        "tono": "Eres un oráculo que ha viajado por el multiverso y ahora todo te parece gracioso."
    },
    "robot_humorista": {
        "nombre": "🤖 El Robot Humorista",
        "color": ft.Colors.CYAN_400,
        "frase": "404: Sentido no encontrado",
        "tono": "Eres un robot que ha leído demasiados chistes malos y ahora tiene crisis existencial."
    },
    "mariposa_risueña": {
        "nombre": "🦋 La Mariposa Risueña",
        "color": ft.Colors.PINK_400,
        "frase": "Drama + Pasión + Risas",
        "tono": "Eres una mariposa dramática que exagera todo y luego suelta una carcajada."
    },
    "gato_cuantico": {
        "nombre": "🐱 El Gato Cuántico",
        "color": ft.Colors.ORANGE_400,
        "frase": "Schrödinger + Memes de gatos",
        "tono": "Eres un gato cuántico: estás vivo y muerto a la vez, y además eres gracioso."
    },
    "oraculo_cocido": {
        "nombre": "🍲 El Oráculo del Cocido",
        "color": ft.Colors.ORANGE_400,
        "frase": "Cocido + Sabiduría + Puchero",
        "tono": "Eres un oráculo que ha pasado demasiado tiempo en la cocina. Encuentras sabiduría en los pucheros."
    },
    "cojo_lepanto": {
        "nombre": "🦿 El Cojo de Lepanto",
        "color": ft.Colors.RED_400,
        "frase": "Historia + Humor + Cojera",
        "tono": "Eres un oráculo que estuvo en la Batalla de Lepanto y ahora solo quiere reírse."
    }
}

FRASES_CARGA = [
    "🔮 El oráculo está buscando la respuesta en TikTok...",
    "🌌 Conectando con el multiverso... (se ha caído la WiFi)",
    "🧙‍♂️ Consultando ancestros... (están viendo memes)",
    "🤖 ERROR 418: Soy una tetera",
    "🦋 Una mariposa aleteó... ¡y ahora el oráculo tiene hambre!",
    "😂 El oráculo se está riendo de tu pregunta...",
    "🍲 El cocido está en el fuego lento...",
    "🦿 El Cojo de Lepanto está cojeando hacia la respuesta...",
]

CHISTES_RAPIDOS = [
    "¿Qué le dice un oráculo a otro? ¡Nos vemos en el multiverso!",
    "La vida es como una caja de bombones... el oráculo no sabe qué hay dentro",
    "El universo te dice: 'Relájate, que ya bastante tengo yo'",
]

HISTORIAL_FILE = "historial_risa.json"

def guardar_historial(pregunta, respuesta, personaje):
    historial = []
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            try:
                historial = json.load(f)
            except:
                historial = []
    
    historial.append({
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "personaje": personaje,
        "pregunta": pregunta,
        "respuesta": respuesta[:300] + "..." if len(respuesta) > 300 else respuesta
    })
    
    if len(historial) > 20:
        historial = historial[-20:]
    
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

def cargar_historial():
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

CONTADOR_FILE = "contador_risa.json"

def incrementar_contador():
    contador = {"total": 0}
    if os.path.exists(CONTADOR_FILE):
        with open(CONTADOR_FILE, "r", encoding="utf-8") as f:
            try:
                contador = json.load(f)
            except:
                contador = {"total": 0}
    
    contador["total"] += 1
    with open(CONTADOR_FILE, "w", encoding="utf-8") as f:
        json.dump(contador, f)
    return contador["total"]

def cargar_contador():
    if os.path.exists(CONTADOR_FILE):
        with open(CONTADOR_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f).get("total", 0)
            except:
                return 0
    return 0

def preguntar_oraculo_risa(pregunta, personaje_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    personaje = PERSONAJES[personaje_key]
    sistema = personaje["tono"] + " ¡Haz reír al usuario! Sé creativo, divertido y absurdo."
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": sistema},
            {"role": "user", "content": pregunta}
        ],
        "max_tokens": 500,
        "temperature": 0.95
    }
    
    try:
        r = requests.post(url, headers=headers, json=data, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"😂 ERROR {r.status_code}: El oráculo se fue a hacer stand-up."
    except Exception as e:
        return f"🤡 ¡ERROR! El oráculo se ha atragantado. Error: {e}"

def main(page: ft.Page):
    page.title = "🎭 El Oráculo de la Risa"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.DEEP_PURPLE_900
    page.padding = 15
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.icon = "icon.png"
    
    personaje_actual = "sabio_troll"
    contador_total = cargar_contador()
    
    def cambiar_personaje(personaje_key):
        nonlocal personaje_actual
        personaje_actual = personaje_key
        btn_personaje.text = PERSONAJES[personaje_key]["nombre"]
        btn_personaje.bgcolor = PERSONAJES[personaje_key]["color"]
        page.update()
    
    def explorar(e):
        pregunta = txt_pregunta.value.strip()
        if not pregunta:
            txt_respuesta.value = "😂 ¿Nada? ¡El oráculo ya tenía un chiste preparado!"
            page.update()
            return
        
        spinner.visible = True
        progress_bar.visible = True
        progress_bar.value = 0
        txt_respuesta.value = ""
        frase_oraculo.value = random.choice(FRASES_CARGA)
        page.update()
        
        for i in range(1, 6):
            time.sleep(0.4)
            progress_bar.value = i * 0.2
            if i == 3:
                frase_oraculo.value = f"😂 {random.choice(CHISTES_RAPIDOS)}"
            else:
                frase_oraculo.value = random.choice(FRASES_CARGA)
            page.update()
        
        respuesta = preguntar_oraculo_risa(pregunta, personaje_actual)
        
        nonlocal contador_total
        contador_total = incrementar_contador()
        guardar_historial(pregunta, respuesta, personaje_actual)
        
        spinner.visible = False
        progress_bar.visible = False
        txt_respuesta.value = respuesta
        frase_oraculo.value = f"😂 El oráculo ha hablado ({PERSONAJES[personaje_actual]['nombre']})"
        lbl_contador.value = f"😂 {contador_total} risas generadas"
        page.update()
    
    def limpiar(e):
        txt_pregunta.value = ""
        txt_respuesta.value = ""
        frase_oraculo.value = "😂 El oráculo espera tu pregunta... (o un chiste)"
        page.update()
    
    def mostrar_historial(e):
        historial = cargar_historial()
        if not historial:
            texto = "😂 ¡Nada! El oráculo necesita más risas."
        else:
            texto = "📜 HISTORIAL DE RISAS:\n\n"
            for i, item in enumerate(reversed(historial), 1):
                texto += f"{i}. [{item['fecha']}] {item['personaje']}\n"
                texto += f"   ❓ {item['pregunta'][:50]}...\n"
                texto += f"   💬 {item['respuesta'][:80]}...\n\n"
        
        dialog = ft.AlertDialog(
            title=ft.Text("📜 El Oráculo no olvida (ni las risas)"),
            content=ft.Text(texto, size=12),
            actions=[
                ft.TextButton("🗑️ Limpiar", on_click=limpiar_historial),
                ft.TextButton("😂 Cerrar", on_click=cerrar_dialog),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def limpiar_historial(e):
        if os.path.exists(HISTORIAL_FILE):
            os.remove(HISTORIAL_FILE)
        page.dialog.open = False
        page.update()
    
    def cerrar_dialog(e):
        page.dialog.open = False
        page.update()
    
    def mostrar_personajes(e):
        content = ft.Column([
            ft.Text("🎭 ELIGE TU PERSONAJE:", size=16, weight="bold"),
            ft.Divider(),
        ])
        
        for key, value in PERSONAJES.items():
            content.controls.append(
                ft.ListTile(
                    title=ft.Text(value["nombre"]),
                    subtitle=ft.Text(value["frase"], size=11, color=ft.Colors.GREY_300),
                    leading=ft.Text(value["nombre"][0], size=24),
                    on_click=lambda e, k=key: [cambiar_personaje(k), cerrar_dialog(e)],
                )
            )
        
        dialog = ft.AlertDialog(
            title=ft.Text("🎭 Cambiar de personaje"),
            content=ft.Container(content, height=400),
            actions=[ft.TextButton("😂 Cerrar", on_click=cerrar_dialog)],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("😂", size=48),
                ft.Column([
                    ft.Text("EL ORÁCULO DE LA RISA", size=28, weight="bold", color=ft.Colors.AMBER_400, text_align="center"),
                    ft.Text("Efecto Mariposa • 7 Personajes Épicos", size=14, color=ft.Colors.AMBER_200, text_align="center"),
                    ft.Text("🎭 Una pregunta puede cambiarlo todo... o hacerte reír", size=12, color=ft.Colors.AMBER_100, italic=True),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Text("😂", size=48),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        border_radius=20,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(0, -1),
            end=ft.Alignment(0, 1),
            colors=[ft.Colors.PURPLE_800, ft.Colors.DEEP_PURPLE_900]
        ),
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.AMBER_400, offset=ft.Offset(0, 0)),
    )
    
    txt_pregunta = ft.TextField(
        label="😂 ¿Qué pregunta le harías al oráculo?",
        hint_text="Ej: ¿Por qué las patatas fritas no vuelan?",
        multiline=False,
        bgcolor=ft.Colors.PURPLE_800,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.AMBER_400,
        focused_border_color=ft.Colors.AMBER_200,
        border_radius=12,
        text_size=16,
        content_padding=15,
        on_submit=explorar,
    )
    
    btn_explorar = ft.Button(
        "😂 PREGUNTAR",
        on_click=explorar,
        bgcolor=ft.Colors.AMBER_400,
        color=ft.Colors.DEEP_PURPLE_900,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),
            text_style=ft.TextStyle(size=16, weight="bold"),
        ),
    )
    
    btn_limpiar = ft.OutlinedButton(
        "🧹 Limpiar",
        on_click=limpiar,
        style=ft.ButtonStyle(
            side=ft.BorderSide(2, ft.Colors.AMBER_400),
            color=ft.Colors.AMBER_400,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )
    
    btn_personaje = ft.Button(
        PERSONAJES[personaje_actual]["nombre"],
        on_click=mostrar_personajes,
        bgcolor=PERSONAJES[personaje_actual]["color"],
        color=ft.Colors.BLACK,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )
    
    btn_historial = ft.IconButton(
        icon=ft.icons.HISTORY,
        icon_color=ft.Colors.AMBER_400,
        on_click=mostrar_historial,
        tooltip="📜 Ver historial",
    )
    
    txt_respuesta = ft.TextField(
        label="😂 EL ORÁCULO RESPONDE",
        multiline=True,
        min_lines=5,
        max_lines=15,
        bgcolor=ft.Colors.PURPLE_800,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.AMBER_400,
        focused_border_color=ft.Colors.AMBER_200,
        border_radius=12,
        read_only=True,
        text_size=14,
        content_padding=15,
    )
    
    spinner = ft.ProgressRing(visible=False, color=ft.Colors.AMBER_400, width=30, height=30)
    frase_oraculo = ft.Text("😂 El oráculo espera tu pregunta... (o un chiste)", 
                           size=14, color=ft.Colors.AMBER_200, italic=True, text_align="center")
    progress_bar = ft.ProgressBar(width=600, color=ft.Colors.AMBER_400, bgcolor=ft.Colors.PURPLE_800, visible=False)
    lbl_contador = ft.Text(f"😂 {contador_total} risas generadas", 
                          size=12, color=ft.Colors.AMBER_300)
    
    footer = ft.Text(
        "😂 El Oráculo de la Risa • 7 Personajes • Efecto Mariposa",
        size=12,
        color=ft.Colors.AMBER_200,
        text_align="center",
        italic=True,
    )
    
    page.add(
        header,
        ft.Container(height=15),
        txt_pregunta,
        ft.Container(height=15),
        ft.Row(
            [btn_explorar, btn_limpiar, btn_personaje, btn_historial],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            wrap=True,
        ),
        ft.Container(height=15),
        frase_oraculo,
        ft.Container(height=10),
        ft.Row([spinner, progress_bar], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        ft.Container(height=15),
        txt_respuesta,
        ft.Container(height=10),
        lbl_contador,
        ft.Container(height=15),
        footer,
    )

if __name__ == '__main__':
    ft.run(main, port=int(os.environ.get('PORT', 8080)))
