
from kivymd.app import MDApp
from client_modbus import ClienteModbus
import os 
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window

class MyWidget(MDBoxLayout):
    pass

class BasicApp(MDApp):
    def build(self):
        self.evento = None
        Window.size=(800,600)
        Window.fullscreen = False
        return MyWidget()

    def conectar(self):
        txt_ip = self.txt_ip.txt.strip()
        txt_porta = self.txt_porta.txt.strip()
        self.cliente = ClienteModbus(host=txt_ip, port=int(txt_porta))
        if self.cliente.conectar():
            print("Conectado ao servidor Modbus")
            self.root.ids.valor_leitura.text = "Conectado!"
        else:
            print("Falha ao conectar ao servidor Modbus")
            self.root.ids.valor_leitura.text = "Falha de Conexão"

    def desconectar(self):
        self.cliente.desconectar()
        print("Desconectado do servidor Modbus")
        self.root.ids.valor_leitura.text = "Desconectado"

    def ler_dado(self):
        try:
            endereco = int(self.root.ids.registrador.txt.strip())
            valor = None
            if self.checkbox1.active:
                valor = self.cliente.ler_holding_register(endereco)
            elif self.checkbox2.active:
                valor = self.cliente.ler_coil(endereco)
            elif self.checkbox3.active:
                valor = self.cliente.ler_input_register(endereco)
            elif self.checkbox4.active:
                valor = self.cliente.ler_discrete_input(endereco)
            if valor is not None:
                self.root.ids.valor_leitura.text = str(valor)
            else:
                self.root.ids.valor_leitura.text = "Erro na leitura"
                print("Erro ao ler dado do servidor Modbus")
        except ValueError:
            self.root.ids.valor_leitura.text = "Endereço inválido"
            print("Endereço inválido para leitura")
    def escrever_dado(self):
        try:
            endereco = int(self.root.ids.registrador.txt.strip())
            valor_texto = self.root.ids.valor_escrita.txt
            sucesso = False
            if self.checkbox1.active:
                valor = int(valor_texto.strip())
                sucesso = self.cliente.escrever_holding_register(endereco, valor)
            elif self.checkbox3.active:
                valor = int(valor_texto.strip()) != 0
                sucesso = self.cliente.escrever_coil(endereco, valor)
            else:
                print("Apenas Holding Registers e Coils suportam escrita padrão neste app.")
                return
            if sucesso:
                self.root.ids.valor_leitura.text = "Escrita bem-sucedida"
                print(f"Valor {valor} escrito com sucesso no endereço {endereco} do servidor Modbus")
            else:
                self.root.ids.valor_leitura.text = "Erro na escrita"
                print("Erro ao escrever dado no servidor Modbus")
        except ValueError:
            self.root.ids.valor_leitura.text = "Endereço ou valor inválido"
            print("Endereço ou valor inválido para escrita")
    
if __name__ == '__main__':
    BasicApp().run()
