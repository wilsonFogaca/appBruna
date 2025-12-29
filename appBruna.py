from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from datetime import datetime
import requests
import os
import certifi
import json
from datetime import datetime, timedelta
from kivy.core.window import Window


# importante para evitar erros de SSL no requests usar toda vez que fizer requisições HTTPS
# quando ha erro de conexao com internet ou certificado SSL inválido
os.inviron['SSL_CERT_FILE'] = certifi.where()

# Define a cor de fundo global: #F4998D (RGB: 244, 153, 141)
Window.clearcolor = (244/255, 153/255, 141/255, 1)  # (R, G, B, A)

# === Configuração do Firebase (Realtime Database - modo público para teste) ===
FIREBASE_URL = "https://bruna-hair-style-default-rtdb.firebaseio.com"


def salvar_agendamento_firebase(nome, procedimento, data_hora):
    url = f"{FIREBASE_URL}/agendamentos.json"
    dados = {
        "nome": nome,
        "procedimento": procedimento,
        "data_hora": data_hora,
        "timestamp": datetime.now().isoformat()
    }
    try:
        resp = requests.post(url, data=json.dumps(dados), timeout=10)
        return resp.status_code == 200
    except:
        return False

def buscar_agendamentos_firebase():
    url = f"{FIREBASE_URL}/agendamentos.json"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200 and resp.text != "null":
            return resp.json()
    except:
        pass
    return {}
class DatePicker(BoxLayout):
    def __init__(self, on_date_selected=None, popup=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 5
        self.on_date_selected = on_date_selected
        self.popup = popup
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.selected_day = None

        # Cabeçalho
        header = BoxLayout(size_hint_y=None, height=40)
        btn_prev = Button(text='<', size_hint_x=0.15)
        btn_prev.bind(on_press=self.mes_anterior)
        self.lbl_title = Label(text='', size_hint_x=0.7, halign='center')
        btn_next = Button(text='>', size_hint_x=0.15)
        btn_next.bind(on_press=self.mes_proximo)
        header.add_widget(btn_prev)
        header.add_widget(self.lbl_title)
        header.add_widget(btn_next)
        self.add_widget(header)

        # Dias da semana
        semana = BoxLayout(size_hint_y=None, height=30)
        for dia in ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']:
            semana.add_widget(Label(text=dia, bold=True, halign='center'))
        self.add_widget(semana)

        # Grid de dias
        self.grid_dias = GridLayout(cols=7, spacing=2, size_hint_y=None)
        self.grid_dias.bind(minimum_height=self.grid_dias.setter('height'))
        self.add_widget(self.grid_dias)

        # Botão Confirmar
        btn_confirm = Button(text='Confirmar', size_hint_y=None, height=45)
        btn_confirm.bind(on_press=self.confirmar)  # ← agora 'confirmar' EXISTE
        self.add_widget(btn_confirm)

        self.atualizar()

    def atualizar(self):
        self.lbl_title.text = f"{self.current_year} - {datetime(2000, self.current_month, 1).strftime('%B').capitalize()}"
        self.grid_dias.clear_widgets()

        primeiro = datetime(self.current_year, self.current_month, 1)
        offset = (primeiro.weekday() + 1) % 7

        if self.current_month == 12:
            prox_mes = datetime(self.current_year + 1, 1, 1)
        else:
            prox_mes = datetime(self.current_year, self.current_month + 1, 1)
        ultimo_dia = (prox_mes - timedelta(days=1)).day

        for _ in range(offset):
            self.grid_dias.add_widget(Label(text=''))

        for dia in range(1, ultimo_dia + 1):
            btn = Button(text=str(dia), size_hint_y=None, height=45)
            btn.bind(on_press=lambda x, d=dia: self.selecionar(d))
            self.grid_dias.add_widget(btn)

        total = 42
        preenchidas = offset + ultimo_dia
        for _ in range(total - preenchidas):
            self.grid_dias.add_widget(Label(text=''))

    def mes_anterior(self, _):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.atualizar()

    def mes_proximo(self, _):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.atualizar()

    def selecionar(self, dia):
        self.selected_day = dia
        for child in self.grid_dias.children:
            if isinstance(child, Button):
                child.background_color = (1, 1, 1, 1)
        for child in self.grid_dias.children:
            if isinstance(child, Button) and child.text == str(dia):
                child.background_color = (0.3, 0.7, 1, 1)
                break

    # ✅ MÉTODO CONFIRMAR — deve estar definido antes de ser usado!
    def confirmar(self, _):
        if self.selected_day is not None:
            data = f"{self.selected_day:02d}/{self.current_month:02d}/{self.current_year}"
            if self.on_date_selected:
                self.on_date_selected(data)
        if self.popup:
            self.popup.dismiss()
        
def show_date_picker(on_date_selected):
    popup = Popup(title="Escolha a data", size_hint=(0.95, 0.85))
    content = DatePicker(on_date_selected=on_date_selected, popup=popup)
    popup.content = content
    popup.open()


# === Telas ===

class TelaPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20

        # === LOGO CENTRALIZADO E DESTACADO ===
        logo_container = BoxLayout(
            size_hint=(1, 0.5),  # Ocupa metade da tela
            padding=[0, 20, 0, 20]
        )
        # Widget invisível para centralização vertical/horizontal
        logo_wrapper = BoxLayout(
            size_hint=(None, None),
            size=(280, 280),  # Ajuste conforme necessário
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        logo_img = Image(
            source='bruna_logo.png',
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=True
        )
        logo_wrapper.add_widget(logo_img)
        logo_container.add_widget(logo_wrapper)
        self.add_widget(logo_container)

        # Nome do salão
        nome_label = Label(
            text='Estúdio de Beleza Bruna Hair Style',
            font_size=22,
            bold=True,
            color=(0.2, 0.2, 0.2, 1),  # Cinza escuro
            
        )

        # WhatsApp
        whatsapp_label = Label(
            text='Agende pelo WhatsApp: (92) 99502-3688',
            font_size=16,
            color=(0.3, 0.3, 0.3, 1),  # Cinza médio
            
        )

                # Botão Agendamento — tom mais intenso
        btn_agendar = Button(
            text='📅 Agendamento',
            size_hint=(1, 0.12),
            background_color=(0.851, 0.420, 0.420, 1),  # #D96B6B
            color=(1, 1, 1, 1),  # Texto branco
            bold=True
        )
        btn_agendar.bind(on_press=self.ir_agendamento)
        self.add_widget(btn_agendar)

        # Botão Ver Agendamentos — verde sage
        btn_visualizar = Button(
            text='👁️ Ver Agendamentos',
            size_hint=(1, 0.12),
            background_color=(0.545, 0.659, 0.651, 1),  # #8BA8A6
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_visualizar.bind(on_press=self.ir_visualizar)
        self.add_widget(btn_visualizar)

    def ir_agendamento(self, _):
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(TelaAgendamento())

    def ir_visualizar(self, _):
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(TelaVisualizarAgendamentos())

class TelaAgendamento(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        self.add_widget(Label(text='Agendamento', font_size=22, size_hint=(1, 0.1)))

        # Nome
        self.nome_input = TextInput(hint_text='Nome completo', multiline=False, size_hint=(1, 0.1))
        self.add_widget(self.nome_input)

        # Procedimento
        self.spinner_proc = Spinner(
            text='Selecione o procedimento',
            values=('Corte', 'Escova progressiva (pequeno)', 'Escova progressiva (médio)',
                    'Escova progressiva (grande)', 'Hidratação', 'Coloração'),
            size_hint=(1, 0.1)
        )
        self.add_widget(self.spinner_proc)

        # Data (com botão de calendário)
        data_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.data_label = Label(text='Data: ---', size_hint_x=0.7)
        btn_calendar = Button(text='📅 Escolher Data', size_hint_x=0.3, on_press=self.abrir_calendario)
        data_layout.add_widget(self.data_label)
        data_layout.add_widget(btn_calendar)
        self.add_widget(data_layout)

        # Hora (Spinner com intervalos de 30 min)
        horarios = [f"{h:02d}:{m:02d}" for h in range(8, 20) for m in (0, 30)]  # 08:00 a 19:30
        self.spinner_hora = Spinner(
            text='Selecione o horário',
            values=horarios,
            size_hint=(1, 0.1)
        )
        self.add_widget(self.spinner_hora)

                # Exemplo de layout de botões (dentro do __init__ das telas secundárias)
        botoes = BoxLayout(size_hint=(1, 0.15), spacing=10)

        btn_salvar = Button(
            text='Salvar',
            background_color=(0.788, 0.490, 0.490, 1),  # #C97D7D
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_salvar.bind(on_press=self.salvar)

        btn_home = Button(
            text='Home',
            background_color=(0.910, 0.706, 0.706, 1),  # #E8B4B4
            color=(0.3, 0.3, 0.3, 1),  # Texto escuro para contraste
            bold=True
        )
        btn_home.bind(on_press=self.ir_home)

        btn_sair = Button(
            text='Sair',
            background_color=(0.722, 0.490, 0.490, 1),  # #B87D7D
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_sair.bind(on_press=self.sair)

        botoes.add_widget(btn_salvar)
        botoes.add_widget(btn_home)
        botoes.add_widget(btn_sair)
        self.add_widget(botoes)

    def abrir_calendario(self, _):
        show_date_picker(self.set_data_selecionada)

    def set_data_selecionada(self, data_str):
        self.data_label.text = f"Data: {data_str}"
        self.selected_date = data_str

    def salvar(self, _):
        nome = self.nome_input.text.strip()
        proc = self.spinner_proc.text
        hora = self.spinner_hora.text

        if proc == 'Selecione o procedimento':
            self.popup("Erro", "Escolha um procedimento.")
            return
        if not nome:
            self.popup("Erro", "Informe o nome.")
            return
        if not hasattr(self, 'selected_date'):
            self.popup("Erro", "Escolha uma data.")
            return
        if hora == 'Selecione o horário':
            self.popup("Erro", "Escolha um horário.")
            return

        data_hora = f"{self.selected_date} {hora}"

        # Verificar conflito no Firebase
        ags = buscar_agendamentos_firebase()
        if ags:
            for ag in ags.values():
                if ag.get("data_hora") == data_hora:
                    self.popup("Conflito", "Este horário já está agendado!")
                    return

        if salvar_agendamento_firebase(nome, proc, data_hora):
            self.popup("Sucesso", "Agendamento salvo!")
            self.nome_input.text = ""
            self.data_label.text = "Data: ---"
            delattr(self, 'selected_date')  # Limpa a data selecionada
            self.spinner_proc.text = "Selecione o procedimento"
            self.spinner_hora.text = "Selecione o horário"
        else:
            self.popup("Erro", "Falha ao conectar ao servidor.")

    def popup(self, titulo, texto):
        Popup(title=titulo, content=Label(text=texto), size_hint=(0.8, 0.4)).open()

    def ir_home(self, _):
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(TelaPrincipal())

    def sair(self, _):
        App.get_running_app().stop()

class TelaVisualizarAgendamentos(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10

        self.add_widget(Label(text='Agendamentos', font_size=22, size_hint=(1, 0.1)))

        # ScrollView para rolar a lista
        self.scroll = ScrollView(size_hint=(1, 0.75))
        self.lista_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.lista_layout.bind(minimum_height=self.lista_layout.setter('height'))
        self.scroll.add_widget(self.lista_layout)
        self.add_widget(self.scroll)

        # Botões
        botoes = BoxLayout(size_hint=(1, 0.15), spacing=10)
        botoes.add_widget(Button(text='Atualizar', on_press=self.carregar_agendamentos))
        botoes.add_widget(Button(text='Home', on_press=self.ir_home))
        botoes.add_widget(Button(text='Sair', on_press=self.sair))
        self.add_widget(botoes)

        # Carregar ao abrir
        self.carregar_agendamentos(None)

    def carregar_agendamentos(self, _):
        self.lista_layout.clear_widgets()
        agendamentos = buscar_agendamentos_firebase()

        if not agendamentos:
            self.lista_layout.add_widget(Label(text="Nenhum agendamento encontrado.", size_hint_y=None, height=40))
            return

        # Converter para lista e ordenar por data/hora
        lista = []
        for key, ag in agendamentos.items():
            try:
                dt = datetime.strptime(ag.get("data_hora", ""), "%d/%m/%Y %H:%M")
                lista.append((dt, ag))
            except:
                lista.append((datetime.min, ag))

        lista.sort(key=lambda x: x[0])

        for _, ag in lista:
            texto = f"[b]{ag.get('nome', '—')}[/b]\n" \
                    f"{ag.get('data_hora', '—')} • {ag.get('procedimento', '—')}"
            label = Label(text=texto, markup=True, size_hint_y=None, height=60, halign='left', valign='middle')
            label.bind(size=label.setter('text_size'))
            self.lista_layout.add_widget(label)

    def ir_home(self, _):
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(TelaPrincipal())

    def sair(self, _):
        App.get_running_app().stop()

class BrunaHairApp(App):
    def build(self):
        return TelaPrincipal()

if __name__ == '__main__':
    BrunaHairApp().run()