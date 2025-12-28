from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.metrics import dp # Para dimensionamento responsivo
import webbrowser

# Defina o número de WhatsApp (SUBSTITUA PELO NÚMERO CORRETO)
WHATSAPP_NUMBER = "5592999999999" # Formato com código do país e DDD, sem símbolos
SALON_NAME = "Estúdio de Beleza Bruna Hair Style"

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(30), dp(50), dp(30), dp(30)] # Padding nas laterais e topo/fundo
        self.spacing = dp(20) # Espaçamento entre os widgets

        # 1. LOGO
        try:
            logo = Image(source='logo.png', size_hint=(1, 0.4), allow_stretch=True, keep_ratio=True)
            self.add_widget(logo)
        except Exception as e:
            # Caso o arquivo não seja encontrado
            print(f"Erro ao carregar o logo: {e}")
            self.add_widget(Label(text="[Logo Placeholder]", font_size=dp(24)))

        # 2. NOME DO SALÃO
        name_label = Label(
            text=SALON_NAME,
            font_size=dp(28),
            bold=True,
            halign='center',
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1) # Branco, ajuste se necessário
        )
        self.add_widget(name_label)

        # Separador visual
        self.add_widget(Label(text="---", size_hint=(1, 0.05)))

        # 3. WHATSAPP PARA CONTATO E AGENDAMENTO (Botão)
        whatsapp_button = Button(
            text=f"📞 Agende pelo WhatsApp: +{WHATSAPP_NUMBER}",
            font_size=dp(20),
            size_hint=(1, 0.1),
            background_color=(0.18, 0.8, 0.44, 1), # Cor verde WhatsApp
            on_press=self.open_whatsapp
        )
        self.add_widget(whatsapp_button)

        info_label = Label(
            text="Toque acima para agendar seu horário.",
            font_size=dp(16),
            size_hint=(1, 0.1),
            color=(0.7, 0.7, 0.7, 1) # Cinza claro
        )
        self.add_widget(info_label)

    def open_whatsapp(self, instance):
        """Abre o aplicativo ou link do WhatsApp."""
        # Cria um link de clique para o WhatsApp
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}"

        # Tenta abrir o link no navegador padrão do sistema (celular)
        try:
            webbrowser.open(whatsapp_url)
        except Exception as e:
            print(f"Erro ao abrir o WhatsApp: {e}")
            # Em caso de erro, você pode adicionar um popup ou notificação

class BrunaHairStyleApp(App):
    def build(self):
        # Define o título do aplicativo
        self.title = SALON_NAME
        # Define o esquema de cores para o fundo da tela principal (Black Theme)
        self.root_window.clearcolor = (0, 0, 0, 1) # Preto
        return MainScreen()

if __name__ == '__main__':
    BrunaHairStyleApp().run()