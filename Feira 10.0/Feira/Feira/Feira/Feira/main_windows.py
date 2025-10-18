from PySide6.QtWidgets import QMainWindow, QStackedWidget, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
import os
import time
from menu import MenuWindow
from teste import TesteWindow
from camera_manager import CameraManager
from palavras import PalavrasWindow
from jogo import ForcaWindow
from loading_page import LoadingPage

# Verifica quando a camera ja foi iniciada!
class CameraInitThread(QThread):
    finished = Signal()  # Sinal que dispara quando a câmera estiver pronta

    def __init__(self, camera_manager):
        super().__init__()
        self.camera_manager = camera_manager

    def run(self):
        # Inicia a câmera (pode demorar)
        self.camera_manager.open_camera()

        # Mantém a tela de loading 1s a mais
        time.sleep(1.5)

        # Sinaliza que terminou
        self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        self.caminho_pasta = os.path.dirname(os.path.abspath(__file__)) # pega a pasta do script
        self.caminho_pasta = os.path.join(self.caminho_pasta, "img")
        # Cusor - Mãozinha
        self.cursor_label = QLabel(self)
        pixmap = QPixmap(os.path.join(self.caminho_pasta,"cursor.png")).scaled(
                80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.cursor_label.setPixmap(pixmap)
        self.cursor_label.resize(pixmap.size())
        self.cursor_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.cursor_label.setStyleSheet("background: transparent;")
        self.cursor_label.hide()
        self.cursor_label.raise_()

        # Gerenciador de câmera (controla cap + timer)
        self.camera_manager = CameraManager()

        # Cria as páginas
        self.first_window = MenuWindow(self.stacked, cursor_label = self.cursor_label, main_window = self, caminho_pasta = self.caminho_pasta)
        self.teste_window = TesteWindow(self.stacked, cursor_label = self.cursor_label, main_window = self, caminho_pasta = self.caminho_pasta)
        self.forca_window = ForcaWindow(self.stacked, cursor_label = self.cursor_label, main_window = self, caminho_pasta = self.caminho_pasta, camera_manager = self.camera_manager)
        self.palavras_window = PalavrasWindow(self.stacked, cursor_label = self.cursor_label, main_window = self, caminho_pasta = self.caminho_pasta)
        # Overlay de loading dentro da mesma janela
        self.loading_page = LoadingPage(caminho_pasta=self.caminho_pasta, parent=self)
        self.loading_page.showFullScreen # cobre toda a janela

        # Adiciona no stacked
        # Passa os parametros dessa forma pra garantir que o parametros cursor_label tenha o valor de self.cursor_label
        # Independente da posição do cursor_label
        self.stacked.addWidget(self.first_window) # Índice 0
        self.stacked.addWidget(self.teste_window) # Índice 1
        self.stacked.addWidget(self.forca_window) # índice 2
        self.stacked.addWidget(self.palavras_window) # Índice 3
        self.stacked.addWidget(self.loading_page) # Índice 4

        self.setStyleSheet("background-color: #5b6092")
        self.showFullScreen()

        # Começa no FirstPage
        self.stacked.setCurrentWidget(self.first_window)
        self.show_loading_overlay()

        # Conecta sinal para atualizar câmera ao trocar de página
        self.stacked.currentChanged.connect(self.on_page_changed)

        # 🔥 Força ativar a câmera já na primeira página
        self.on_page_changed(0)

    def on_page_changed(self, index):
        """Atualiza os callbacks da câmera quando troca de página"""
        # Garante que sempre reinicia do zero ao trocar de página
        self.camera_manager.stop()
        
        if index == 0:
            self.camera_manager.set_callback(self.first_window.process_frame)
        elif index == 1:
            self.camera_manager.set_callback(self.teste_window.process_frame)
        elif index == 2:
            self.camera_manager.set_callback(self.forca_window.process_frame)
        elif index == 3:
            self.camera_manager.set_callback(self.palavras_window.process_frame)
        
        self.camera_manager.start()
    
    def switch_to_page(self, page_index):
        """Mostra a tela de loading e espera a câmera inicializar"""
        
        self.loading_page.movie.stop()
        self.loading_page.movie.start()

        # Mostra a tela de loading imediatamente
        self.stacked.setCurrentWidget(self.loading_page)

        # Cria e inicia thread para abrir a câmera
        self.thread = CameraInitThread(self.camera_manager)
        
        # Quando a thread terminar, muda para a página real
        self.thread.finished.connect(lambda: (
            self.camera_manager.start(),  # <- só inicia na thread principal
            self.stacked.setCurrentIndex(page_index)
        ))

        self.thread.start()

    def show_loading_overlay(self):
        # Mostra overlay de loading
        self.loading_page.show()
        self.loading_page.raise_()  # garante que fique na frente
        self.cursor_label.hide()    # esconde cursor enquanto loading

        # Inicia câmera em thread
        self.thread = CameraInitThread(self.camera_manager)
        self.thread.finished.connect(self.hide_loading_overlay)
        self.thread.start()
    
    def hide_loading_overlay(self):
        # Remove overlay de loading e mostra cursor
        self.loading_page.setVisible(False)
        self.cursor_label.show()
        print("Loading Finalizado, cursor visível")