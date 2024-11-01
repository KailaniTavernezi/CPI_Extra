import pyqtgraph as pg #instalação da biblioteca mais eficiente que a matplotlib
from pyqtgraph.Qt import QtCore, QtWidgets
import serial
import time

# Configuração da conexão serial (ajuste a porta e a taxa de transmissão conforme necessário)
ser = serial.Serial('COM7', 115200, timeout=1) 

# Configuração da interface gráfica
app = QtWidgets.QApplication([]) #criação da instância de aplicação (gerencia a interface gráfica)
janela = pg.GraphicsLayoutWidget(show=True, title="Real-time Plotting") #criação da janela que plota os gráficos
janela.resize(1000, 600) #configura o tamanho da janela de plotagem
janela.setWindowTitle('Saída Real e Setpoint em Tempo Real') #define o título da janela de plotagem

# Criar o gráfico
plot = janela.addPlot(title="Saída Real (Actual) e Setpoint vs Tempo") #adiciona um novo gráfico a janela "janela" e atribui seu título
plot.setLabel('left', 'Valores') #determinação do título e do seu local no eixo X
plot.setLabel('bottom', 'Tempo (s)') #determinação do título e do seu local no eixo Y
plot.addLegend() #legenda da do gráfico plotado

# Curvas para "actual" e "setpoint"
actual_curve = plot.plot(pen=pg.mkPen('b', width=2), name="Actual") #adição de uma série de dados, no caso, os dados "Actual" que serão representados graficamente
setpoint_curve = plot.plot(pen=pg.mkPen('r', width=2, style=QtCore.Qt.DashLine), name="Setpoint") #adição de uma série de dados, no caso, os dados "Stepoint" que serão representados graficamente

# Inicialização dos dados
time_data = [] #inicialização da lista de armazenamento de dados de tempo coletados via porta serial
actual_data = [] #inicialização da lista de armazenamento de dados de saída coletados via porta serial
setpoint_data = [] #inicialização da lista de armazenamento de dados de setpoint coletados via porta serial

# Duração da coleta de dados (segundos)
total_duration = 40 #definição do tempo de coleta de dados
start_time = time.time() #definição do instante de inicio da coleta para futuro cálculo do tempo de coleta

#Se quiser coletar por tempo indefinido, substituir as linhas 30, 31 e 32 por:
#collecting = True
#além disso, adicionar na função "update" no lugar de "current_time..."
#     global collecting  # Acessar a variável global para controle da coleta
#     if collecting:  # Verifica se a coleta de dados deve continuar 
#por fim, após o início da atualização, trocas as linhas da execução da aplicação gráfica por:
#try:
    # Executar a aplicação gráfica
#    QtWidgets.QApplication.instance().exec_()
#except KeyboardInterrupt:
    # Captura de interrupção de teclado
#    collecting = False  # Define a variável de controle como False para interromper a coleta

# Função de atualização do gráfico
def update():
    current_time = time.time() - start_time #cálculo do tempo descorrido desde o início da coleta de dados
    
    # Ler dados da porta serial
    if ser.in_waiting > 0: #verificação da disponibilidade de dados para leitura na porta serial
        line = ser.readline().decode('utf-8').strip() #se houver dados, le uma linha de dados na porta
        if line: #se a linha não estiver vazia...
            # Supondo que os dados estão no formato "time,setpoint,actual"
            data = line.split(',') #a linha lida é definida como uma lista de dados
            if len(data) == 3:  # Verifica se há 3 valores (time,setpoint,actual)
                try: #tentativa de conversão dos dados lidos em float
                    elapsed_time = float(data[0])  # Primeiro valor é o tempo
                    setpoint = float(data[1])  # Segundo valor é o setpoint
                    actual = float(data[2])  # Terceiro valor é o valor atual
                    
                    # Atualização de dados às listas
                    time_data.append(elapsed_time)
                    actual_data.append(actual)
                    setpoint_data.append(setpoint)
                    
                    # Limitar os dados exibidos para melhorar o desempenho
                    if len(time_data) > 1000: #se os dados passarem de 1000, os mais antigos passam a ser removidos
                        time_data.pop(0)
                        actual_data.pop(0)
                        setpoint_data.pop(0)
                    
                    # Atualização das curvas com os novos dados
                    actual_curve.setData(time_data, actual_data)
                    setpoint_curve.setData(time_data, setpoint_data)

                except ValueError:
                    pass  # Ignorar erros de conversão de tipo

    # Continuar a atualização se o tempo de duração não foi alcançado
    if current_time < total_duration: # Se ainda estiver dentro do limite, a função update se agenda para ser chamada novamente após 50 milissegundos
        QtCore.QTimer.singleShot(50, update)
    else:
        print("Coleta de dados concluída.") #se tiver sido alcançado, a mensagem aparece o terminal
        ser.close()  # Fechar a porta serial quando a coleta estiver concluída

# Início do ciclo de atualização dos dados
update()

# Executar a aplicação gráfica, ou seja, o loop de eventos da aplicação Qt
QtWidgets.QApplication.instance().exec_()