import control as ctrl

# Exemplo: Definindo a função de transferência do sistema
R = 470
C = 22e-6
tau = 1/(R*C)
num = [tau**2]  # Numerador
den = [1, (2*tau), (tau**2)]  # Denominador (primeira ordem)

H = ctrl.TransferFunction(num, den)
print(H)

# Parâmetros de sintonia
T_r = 1.0  # Tempo de resposta desejado
Kp = 1.2 * (tau**2) * (tau / T_r)
Ti = 2 * T_r  # Tempo integral
Ki = Kp / Ti
Td = 0.1  # Tempo de filtragem da derivada
Kd = Kp * (Td / tau)

#Implementação do controlador PID
class PIDController:
    def __init__(self, Kp, Ki, Kd, T_d=0.1, setpoint_weight=1.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.T_d = T_d
        self.setpoint_weight = setpoint_weight
        self.integral = 0.0
        self.prev_error = 0.0
        self.last_derivative = 0.0

    def update(self, setpoint, measurement, dt):
        error = setpoint - measurement
        
        # Anti-windup
        if abs(error) < 1.0:
            self.integral += error * dt
        else:
            self.integral = 0.0  # Reset integral

        # Derivada com filtragem
        derivative = (error - self.prev_error) / dt
        filtered_derivative = (self.last_derivative + derivative) / 2
        self.last_derivative = filtered_derivative

        # Controle PID
        output = (self.Kp * error +
                  self.Ki * self.integral +
                  self.Kd * filtered_derivative +
                  self.setpoint_weight * setpoint)

        self.prev_error = error
        return output

#Simulação do sistema
import numpy as np
import matplotlib.pyplot as plt

# Inicializando o controlador PID
pid = PIDController(Kp, Ki, Kd)

# Parâmetros de simulação
setpoint = 1
measurement = 0.0
dt = 0.1  # Intervalo de amostragem
times = np.arange(0, 10, dt)
outputs = []

for t in times:
    control_signal = pid.update(setpoint, measurement, dt)
    # Simulação do sistema: usando a função de transferência para obter a nova medição
    measurement += (control_signal * dt)  # Aqui você deve incluir a dinâmica do sistema real

    # Atualiza a saída
    outputs.append(measurement)
    print(f'Time: {times}, Setpoint: {setpoint}, Measurement: {measurement}')


# Gráfico dos resultados
plt.plot(times, outputs, label='Saída do Sistema')
plt.axhline(y=setpoint, color='r', linestyle='--', label='Setpoint')
plt.xlabel('Tempo (s)')
plt.ylabel('Saída')
plt.title('Resposta do Sistema com Controle PID')
plt.legend()
plt.grid()
plt.show()

