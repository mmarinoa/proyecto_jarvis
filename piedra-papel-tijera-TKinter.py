import tkinter as tk
from tkinter import messagebox
import random


class PiedraPapelTijera:
    def __init__(self, root):
        self.root = root
        self.root.title("Piedra, Papel o Tijera")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Variables del juego
        self.puntos_jugador = tk.IntVar(value=0)
        self.puntos_maquina = tk.IntVar(value=0)
        self.eleccion_jugador = tk.StringVar(value="Esperando...")
        self.eleccion_maquina = tk.StringVar(value="Esperando...")
        self.resultado_ronda = tk.StringVar(value="¡Haz tu elección!")
        self.juego_activo = True

        # Creamos la interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # titulo del juego
        titulo = tk.Label(main_frame, text="PIEDRA, PAPEL O TIJERA",
                          font=("Arial", 16, "bold"), fg="blue")
        titulo.pack(pady=10)

        # Marcador
        marcador_frame = tk.LabelFrame(main_frame, text="MARCADOR",
                                       font=("Arial", 12, "bold"), padx=10, pady=10)
        marcador_frame.pack(fill=tk.X, pady=10)

        tk.Label(marcador_frame, text="Jugador:", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        tk.Label(marcador_frame, textvariable=self.puntos_jugador,
                 font=("Arial", 12, "bold"), fg="green").grid(row=0, column=1, padx=20)

        tk.Label(marcador_frame, text="Máquina:", font=("Arial", 10)).grid(row=0, column=2, sticky="w")
        tk.Label(marcador_frame, textvariable=self.puntos_maquina,
                 font=("Arial", 12, "bold"), fg="red").grid(row=0, column=3, padx=20)

        # Elecciones
        elecciones_frame = tk.LabelFrame(main_frame, text="ELECCIONES",
                                         font=("Arial", 12, "bold"), padx=10, pady=10)
        elecciones_frame.pack(fill=tk.X, pady=10)

        tk.Label(elecciones_frame, text="Jugador:", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        tk.Label(elecciones_frame, textvariable=self.eleccion_jugador,
                 font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10, sticky="w")

        tk.Label(elecciones_frame, text="Máquina:", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
        tk.Label(elecciones_frame, textvariable=self.eleccion_maquina,
                 font=("Arial", 10, "bold")).grid(row=1, column=1, padx=10, sticky="w")

        # Resultado
        resultado_label = tk.Label(main_frame, textvariable=self.resultado_ronda,
                                   font=("Arial", 12, "bold"), fg="purple", height=2)
        resultado_label.pack(fill=tk.X, pady=10)

        # Botones de elección
        botones_frame = tk.LabelFrame(main_frame, text="ELEGIR JUGADA",
                                      font=("Arial", 12, "bold"), padx=10, pady=10)
        botones_frame.pack(fill=tk.X, pady=10)

        #botones de pieda papel tijera
        tk.Button(botones_frame, text="PIEDRA", font=("Arial", 10),
                  command=lambda: self.jugar("piedra"),
                  bg="lightgray", width=10).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(botones_frame, text="PAPEL", font=("Arial", 10),
                  command=lambda: self.jugar("papel"),
                  bg="lightblue", width=10).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(botones_frame, text="TIJERA", font=("Arial", 10),
                  command=lambda: self.jugar("tijera"),
                  bg="lightgreen", width=10).pack(side=tk.LEFT, padx=5, pady=5)

        # Botones de control
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=20)

        tk.Button(control_frame, text="Nuevo Juego", font=("Arial", 10),
                  command=self.nuevo_juego, bg="yellow").pack(side=tk.LEFT, padx=10)

        tk.Button(control_frame, text="Salir", font=("Arial", 10),
                  command=self.root.quit, bg="orange").pack(side=tk.RIGHT, padx=10)

    def jugar(self, eleccion_jugador):
        if not self.juego_activo:
            return

        # que escoge la máquina
        opciones = ["piedra", "papel", "tijera"]
        eleccion_maquina = random.choice(opciones)

        # Actualizamos las elecciones
        self.eleccion_jugador.set(eleccion_jugador.capitalize())
        self.eleccion_maquina.set(eleccion_maquina.capitalize())

        # Vemos quien gana
        if eleccion_jugador == eleccion_maquina:
            self.resultado_ronda.set(f"¡Empate! Ambos eligieron {eleccion_jugador}")
            return

        # Lógica del juego
        if ((eleccion_jugador == "piedra" and eleccion_maquina == "tijera") or
                (eleccion_jugador == "papel" and eleccion_maquina == "piedra") or
                (eleccion_jugador == "tijera" and eleccion_maquina == "papel")):

            # Cuando gana el jugador
            self.puntos_jugador.set(self.puntos_jugador.get() + 1)
            self.resultado_ronda.set(f"¡Ganaste! {eleccion_jugador.capitalize()} gana a {eleccion_maquina}")

        else:
            # Cuando gana la maquina
            self.puntos_maquina.set(self.puntos_maquina.get() + 1)
            self.resultado_ronda.set(f"¡Perdiste! {eleccion_maquina.capitalize()} gana a {eleccion_jugador}")

        # Verificamos si alguien ganó la partida
        self.verificar_fin_partida()

    def verificar_fin_partida(self):
        if self.puntos_jugador.get() >= 3:
            self.juego_activo = False
            messagebox.showinfo("¡Fin del Juego!", "¡Felicidades! ¡Has ganado la partida!")
        elif self.puntos_maquina.get() >= 3:
            self.juego_activo = False
            messagebox.showinfo("¡Fin del Juego!", "¡La máquina ha ganado la partida!")

    def nuevo_juego(self):
        # Reiniciar variables
        self.puntos_jugador.set(0)
        self.puntos_maquina.set(0)
        self.eleccion_jugador.set("Esperando...")
        self.eleccion_maquina.set("Esperando...")
        self.resultado_ronda.set("¡Haz tu elección!")
        self.juego_activo = True


def main():
    root = tk.Tk()
    app = PiedraPapelTijera(root)
    root.mainloop()


if __name__ == "__main__":
    main()