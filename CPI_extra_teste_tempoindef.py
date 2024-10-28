import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import random
import time

# Configuração da interface gráfica
app = QtWidgets.QApplication([])
janela = pg.GraphicsLayoutWidget(show=True, title="Real-time Plotting")
janela.resize(1000, 600)
janela.setWindowTitle('Saída Real e Setpoint em Tempo Real')

# Criar o gráfico
plot = janela.addPlot(title="Saída Real (Actual) e Setpoint vs Tempo")
plot.setLabel('left', 'Valores')
plot.setLabel('bottom', 'Tempo (s)')
plot.addLegend()

# Curvas para "actual" e "setpoint"
actual_curve = plot.plot(pen=pg.mkPen('b', width=2), name="Actual")
setpoint_curve = plot.plot(pen=pg.mkPen('r', width=2, style=QtCore.Qt.DashLine), name="Setpoint")

# Inicialização dos dados
time_data = []
actual_data = []
setpoint_data = []

# Variável para controle da coleta de dados
collecting = True

# Função de atualização do gráfico
def update():
    global collecting  # Acessar a variável global para controle da coleta
    if collecting:  # Verifica se a coleta de dados deve continuar
        # Simular dados
        current_time = time.time() - start_time
        setpoint = 50  # Valor constante para o setpoint
        actual = setpoint + random.uniform(-5, 5)  # Simulando variação do "actual"
        
        # Adicionar novos dados às listas
        time_data.append(current_time)
        actual_data.append(actual)
        setpoint_data.append(setpoint)

        # Limitar os dados exibidos para melhorar o desempenho
        if len(time_data) > 1000:
            time_data.pop(0)
            actual_data.pop(0)
            setpoint_data.pop(0)
        
        # Atualizar as curvas com os novos dados
        actual_curve.setData(time_data, actual_data)
        setpoint_curve.setData(time_data, setpoint_data)

        # Continuar a atualização
        QtCore.QTimer.singleShot(50, update)

# Marcar o tempo de início
start_time = time.time()

# Iniciar a atualização
update()

try:
    # Executar a aplicação gráfica
    QtWidgets.QApplication.instance().exec_()
except KeyboardInterrupt:
    # Captura de interrupção de teclado
    collecting = False  # Define a variável de controle como False para interromper a coleta
    print("Coleta de dados interrompida.")