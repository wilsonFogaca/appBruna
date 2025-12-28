# main.py
import locale
import sqlite3
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Configurar locale para português (com acentos)
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
    except:
        pass  # Fallback: sem acentos, mas não quebra

# Configurar cor de fundo preta
Window.clearcolor = (0, 0, 0, 1)

# ---------------------------
# Banco de dados
# ---------------------------
def init_db():
    conn = sqlite3.connect('agendamentos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            procedimento TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_agendamentos():
    conn = sqlite3.connect('agendamentos.db')
    c = conn.cursor()
    c.execute("SELECT cliente, data, hora, procedimento FROM agendamentos ORDER BY data, hora")
    rows = c.fetchall()
    conn.close()
    return rows

# ---------------------------
# Telas
# ---------------------------
class TelaPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        logo = Image(source='logo.png', size_hint=(None, None), size=(200, 200))
        layout.add_widget(logo)

        nome = Label(text="BRUNA HAIR STYLE", color=(1,1,1,1), font_size='24sp', bold=True, halign='center')
        nome.bind(size=nome.setter('text_size'))
        layout.add_widget(nome)

        sub = Label(text="ESTÚDIO DE BELEZA", color=get_color_from_hex('#B8860B'), font_size='16sp', halign='center')
        sub.bind(size=sub.setter('text_size'))
        layout.add_widget(sub)

        btn_whatsapp = Button(
            text="📞 Agendar via WhatsApp",
            background_color=get_color_from_hex('#25D366'),
            color=(1,1,1,1),
            size_hint=(0.8, None),
            height=60,
            bold=True
        )
        btn_whatsapp.bind(on_press=self.abrir_whatsapp)
        layout.add_widget(btn_whatsapp)

        btn_agenda = Button(
            text="📅 Ver Agendamentos",
            background_color=get_color_from_hex('#4A90E2'),
            color=(1,1,1,1),
            size_hint=(0.8, None),
            height=60,
            bold=True
        )
        btn_agenda.bind(on_press=self.ir_para_agenda)
        layout.add_widget(btn_agenda)

        self.add_widget(layout)

    import platform

def abrir_whatsapp(self, instance):
    phone = "+5511999999999"  # ← Substitua pelo número real (com DDD e país)
    message = "Olá! Gostaria de agendar um horário no Bruna Hair Style."

    if platform.system() == 'Android':
        self.abrir_whatsapp_android(phone, message)
    else:
        # Fallback para desktop/navegador
        import webbrowser
        url = f"https://wa.me/{phone.replace('+', '')}?text={message}"
        webbrowser.open(url)

    def abrir_whatsapp_android(self, phone, message):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')

            uri = Uri.parse(f"https://api.whatsapp.com/send?phone={phone.replace('+', '')}&text={message}")
            intent = Intent(Intent.ACTION_VIEW, uri)
            intent.setPackage("com.whatsapp")  # Força abrir no app do WhatsApp

            activity = PythonActivity.mActivity
            activity.startActivity(intent)
        except Exception as e:
            # Se falhar (ex: WhatsApp não instalado), abre no navegador
            import webbrowser
            webbrowser.open(f"https://wa.me/{phone.replace('+', '')}?text={message}")

    def ir_para_agenda(self, instance):
        self.manager.current = 'tela_agenda'

class TelaAgenda(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Botão voltar
        btn_voltar = Button(
            text="← Voltar",
            size_hint=(None, None),
            size=(100, 40),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        btn_voltar.bind(on_press=self.voltar)
        self.layout.add_widget(btn_voltar)

        # ScrollView para lista de agendamentos
        self.scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 100))
        self.grid = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)
        self.atualizar_lista()

    def voltar(self, instance):
        self.manager.current = 'tela_principal'

    def atualizar_lista(self):
        # Limpar lista atual
        self.grid.clear_widgets()

        agendamentos = get_agendamentos()

        if not agendamentos:
            self.grid.add_widget(Label(
                text="Nenhum agendamento registrado.",
                color=(1,1,1,1),
                size_hint_y=None,
                height=50
            ))
        else:
            for cliente, data_str, hora, procedimento in agendamentos:
                # Converter data para formato legível com acentos
                try:
                    data_obj = datetime.strptime(data_str, "%Y-%m-%d")
                    data_bonita = data_obj.strftime("%A, %d de %B de %Y")
                except:
                    data_bonita = data_str  # fallback

                info = f"[b]{cliente}[/b]\n" \
                       f"Data: {data_bonita}\n" \
                       f"Horário: {hora}\n" \
                       f"Procedimento: {procedimento}"

                label = Label(
                    text=info,
                    markup=True,
                    size_hint_y=None,
                    height=120,
                    color=(1,1,1,1),
                    halign='left',
                    valign='middle'
                )
                label.bind(size=label.setter('text_size'))
                self.grid.add_widget(label)

class GerenciadorTelas(ScreenManager):
    pass

# ---------------------------
# App principal
# ---------------------------
class BrunaHairStyleApp(App):
    def build(self):
        init_db()
        sm = GerenciadorTelas()
        sm.add_widget(TelaPrincipal(name='tela_principal'))
        sm.add_widget(TelaAgenda(name='tela_agenda'))
        return sm

    def on_start(self):
        pass

# ---------------------------
if __name__ == '__main__':
    BrunaHairStyleApp().run()