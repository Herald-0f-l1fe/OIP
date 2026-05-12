import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize= (10,6))
    plt.plot(time, voltage)

    plt.title("Зависимость напряжения от времени", fontsize = 16, fontweight = "bold")
    plt.xlabel("Время, с", fontsize = 12)
    plt.ylabel("Напряжение, В", fontsize = 12)

    plt.xlim(0, max(time) + 1)
    plt.ylim(0, max(voltage))

    plt.grid(True, alpha = 0.3, linestyle = "--")

    plt.tight_layout()
    plt.show()

def plot_sampling_period_hist(time):
    sampling_periods = []

    sampling_periods.append(time[0])
    for i in range(1, len(time)):
        sampling_periods.append(time[i] - time[i-1])

    # print(sampling_periods)
    
    plt.figure(figsize= (10,6))
    plt.hist(sampling_periods)

    plt.title("Зависимость напряжения от времени", fontsize = 16, fontweight = "bold")
    plt.xlabel("Период измерения, с", fontsize = 12)
    plt.ylabel("Количество измерений", fontsize = 12)

    plt.xlim(0, max(sampling_periods))
    plt.show()
