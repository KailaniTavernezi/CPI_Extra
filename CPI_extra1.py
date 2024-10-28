import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets  # Corrigir importação de QtWidgets para QApplication
import random
import time

# Configuração da interface gráfica
app = QtWidgets.QApplication([])  # Mudar para QtWidgets.QApplication
janela = pg.GraphicsLayoutWidget(show=True, title="Real-time Plotting")
janela.resize(1000, 600)
janela.setWindowTitle('Saída de Setpoint em Tempo Real')

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

# Duração da simulação (segundos)
total_duration = 40
start_time = time.time()

# Função de atualização do gráfico
def update():
    current_time = time.time() - start_time
    
    # Gerar dados simulados
    setpoint = 50  # Setpoint constante
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
    
    # Continuar a atualização se o tempo de duração não foi alcançado
    if current_time < total_duration:
        QtCore.QTimer.singleShot(50, update)
    else:
        print("Simulação concluída.")

# Iniciar a atualização
update()

# Executar a aplicação gráfica
QtWidgets.QApplication.instance().exec_()