from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivy.properties import ObjectProperty
import webbrowser
from kivy.core.window import Window

# --- Configurações Globais ---
WHATSAPP_NUMBER = "5592999999999" # NÚMERO DE WHATSAPP (Ajustar)
SALON_NAME = "Estúdio de Beleza Bruna Hair Style"

# --- 1. TELA PRINCIPAL: MainScreen ---

class MainScreen(Screen):
    # Permite acesso ao ScreenManager e mudança de tela
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main_screen' # Nome da tela para referência no ScreenManager

        # Layout Principal da Tela
        layout = BoxLayout(orientation='vertical', padding=[dp(30), dp(50), dp(30), dp(30)], spacing=dp(20))

        # 1. LOGO
        try:
            logo = Image(source='logo.png', size_hint=(1, 0.4), allow_stretch=True, keep_ratio=True)
            layout.add_widget(logo)
        except Exception:
            layout.add_widget(Label(text="[Logo Bruna Hair Style]", font_size=dp(24)))

        # 2. NOME DO SALÃO
        name_label = Label(
            text=f"**{SALON_NAME}**",
            font_size=dp(28),
            markup=True, # Permite negrito (markdown)
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1)
        )
        layout.add_widget(name_label)

        # Separador visual
        layout.add_widget(Label(text="---", size_hint=(1, 0.05)))

        # BOTÃO PARA ACESSAR A TELA DE AGENDAMENTO
        schedule_button = Button(
            text="📅 Fazer um Agendamento",
            font_size=dp(20),
            size_hint=(1, 0.1),
            background_color=(0.1, 0.5, 0.8, 1), # Azul para Agendamento
            on_press=self.go_to_scheduling
        )
        layout.add_widget(schedule_button)

        # BOTÃO WHATSAPP
        whatsapp_button = Button(
            text=f"📞 Fale Conosco: +{WHATSAPP_NUMBER}",
            font_size=dp(20),
            size_hint=(1, 0.1),
            background_color=(0.18, 0.8, 0.44, 1), # Verde WhatsApp
            on_press=self.open_whatsapp
        )
        layout.add_widget(whatsapp_button)

        self.add_widget(layout)

    def open_whatsapp(self, instance):
        """Abre o link direto para o WhatsApp."""
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}"
        webbrowser.open(whatsapp_url)

    def go_to_scheduling(self, instance):
        """Muda para a tela de Agendamento."""
        if self.screen_manager:
            self.screen_manager.current = 'scheduling_screen'
            
# --- 2. TELA SECUNDÁRIA: Agendamento de Cliente ---

class SchedulingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'scheduling_screen'

        # Layout Principal (Vertical)
        layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(15))

        # Título da Tela
        title_label = Label(
            text="## Agendamento de Cliente",
            font_size=dp(26),
            bold=True,
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1)
        )
        layout.add_widget(title_label)
        
        # 1. NOME DO CLIENTE
        layout.add_widget(Label(text="Nome Completo do Cliente:", size_hint=(1, None), height=dp(30), halign='left'))
        self.name_input = TextInput(multiline=False, size_hint=(1, None), height=dp(40), hint_text="Seu nome", background_color=(1,1,1,1), foreground_color=(0,0,0,1))
        layout.add_widget(self.name_input)

        # 2. HORA
        layout.add_widget(Label(text="Horário Desejado (ex: 15:30):", size_hint=(1, None), height=dp(30), halign='left'))
        self.time_input = TextInput(multiline=False, size_hint=(1, None), height=dp(40), hint_text="HH:MM", input_filter='int', background_color=(1,1,1,1), foreground_color=(0,0,0,1))
        layout.add_widget(self.time_input)

        # 3. DATA
        layout.add_widget(Label(text="Data Desejada (ex: dd/mm/aaaa):", size_hint=(1, None), height=dp(30), halign='left'))
        self.date_input = TextInput(multiline=False, size_hint=(1, None), height=dp(40), hint_text="DD/MM/AAAA", input_filter='int', background_color=(1,1,1,1), foreground_color=(0,0,0,1))
        layout.add_widget(self.date_input)

        # 4. TIPO DE PROCEDIMENTO
        layout.add_widget(Label(text="Procedimento (ex: Corte, Coloração, Penteado):", size_hint=(1, None), height=dp(30), halign='left'))
        self.procedure_input = TextInput(multiline=False, size_hint=(1, None), height=dp(40), hint_text="Ex: Corte Feminino + Escova", background_color=(1,1,1,1), foreground_color=(0,0,0,1))
        layout.add_widget(self.procedure_input)
        
        # Espaço flexível para empurrar os botões para baixo
        layout.add_widget(Label(text="", size_hint=(1, 1)))

        # Botão para Enviar Agendamento
        submit_button = Button(
            text="✔️ Confirmar Agendamento",
            font_size=dp(20),
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.18, 0.8, 0.44, 1),
            on_press=self.submit_schedule
        )
        layout.add_widget(submit_button)
        
        # Botão para Voltar
        back_button = Button(
            text="↩️ Voltar",
            font_size=dp(16),
            size_hint=(1, None),
            height=dp(40),
            background_color=(0.5, 0.5, 0.5, 1),
            on_press=self.go_back
        )
        layout.add_widget(back_button)

        self.add_widget(layout)

    def submit_schedule(self, instance):
        """Função que será chamada ao confirmar o agendamento."""
        # 1. Obter os dados
        nome = self.name_input.text
        hora = self.time_input.text
        data = self.date_input.text
        procedimento = self.procedure_input.text

        # 2. Validação e Processamento (A ser implementado!)
        if not all([nome, hora, data, procedimento]):
            print("ERRO: Todos os campos são obrigatórios!")
            # Em um app real, você mostraria um popup de erro
            return

        # Ação Real do Sistema (por exemplo, enviar para um servidor ou salvar em um arquivo)
        print("\n--- Agendamento Recebido ---")
        print(f"Cliente: {nome}")
        print(f"Data/Hora: {data} às {hora}")
        print(f"Procedimento: {procedimento}")
        print("----------------------------\n")
        
        # Exemplo de feedback (pode ser substituído por um popup de sucesso)
        # Limpar os campos após o envio simulado
        self.name_input.text = ''
        self.time_input.text = ''
        self.date_input.text = ''
        self.procedure_input.text = ''

        # O ideal seria redirecionar para uma tela de sucesso
        if self.manager:
             self.manager.current = 'main_screen'


    def go_back(self, instance):
        """Muda de volta para a tela principal."""
        if self.manager:
            self.manager.current = 'main_screen'
            
# --- 3. CLASSE PRINCIPAL DO APLICATIVO (App) ---

# Define a cor de fundo da janela (preto)
Window.clearcolor = (0, 0, 0, 1)

class BrunaHairStyleApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Seu conteúdo...
        logo = Image(source='logo.png', size_hint=(None, None), size=(200, 200))
        layout.add_widget(logo)

        # Configura o ScreenManager
        sm = ScreenManager()

        # Cria as instâncias das telas
        main_screen = MainScreen(screen_manager=sm)
        scheduling_screen = SchedulingScreen()

        # Conecta o ScreenManager à MainScreen (para navegação)
        main_screen.screen_manager = sm

        # Adiciona as telas ao ScreenManager
        sm.add_widget(main_screen)
        sm.add_widget(scheduling_screen)

        # Retorna o ScreenManager como o widget raiz
        return sm

if __name__ == '__main__':
    BrunaHairStyleApp().run()