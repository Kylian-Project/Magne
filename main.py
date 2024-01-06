import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenuBar, QAction, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from src.graph import *   # Importez fichier graph.py

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_name = None
        self.fill = True

        self.setWindowTitle("Magne EOST")
        self.showMaximized()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Utilisez la figure Matplotlib dans l'application PyQt5
        self.canvas = FigureCanvas(fig)

        # Ajustez les marges de la figure Matplotlib pour enlever les bordures
        fig.subplots_adjust(left=0.04, right=0.995, top=0.965, bottom=0.03)

        # Ajoutez la barre d'outils Matplotlib
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)

        self.layout.addWidget(self.canvas)

        # Créez un menu déroulant dans la barre de menu
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Menu Fichier
        menu = menu_bar.addMenu("Fichier")

        action_open_file = QAction("Ouvrir Fichier (.paf)", self)
        action_open_file.triggered.connect(self.open_file_dialog)

        sauvegarder = QAction("Sauvegarder", self)
        sauvegarder.setShortcut('Ctrl+S')  # Définir le raccourci clavier pour l'action de sauvegarde
        sauvegarder.triggered.connect(self.sav_file_name)

        action_quitter = QAction("Quitter", self)
        action_quitter.setShortcut('Ctrl+Q')
        action_quitter.triggered.connect(self.close)
        
        menu.addAction(action_open_file)
        menu.addAction(sauvegarder)
        menu.addAction(action_quitter)

        # Menu Affichage
        menu2 = menu_bar.addMenu("Affichage")

        action_fill = QAction("Remplir Graph", self)

        action_fill.setCheckable(True)
        action_fill.setChecked(True)

        action_fill.triggered.connect(self.remplissage)

        menu2.addAction(action_fill)

    def closeEvent(self, event):
        if not saved_or_not() and self.file_name:  # Supposons que self.file_saved est un booléen qui indique si le fichier a été sauvegardé ou non
            reply = QMessageBox.question(self, 'Message',
                                         "Attention, vous n'avez pas sauvegardé. Êtes-vous sûr de vouloir quitter ?", QMessageBox.Yes |
                                         QMessageBox.No | QMessageBox.Save, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            elif reply == QMessageBox.Save:
                self.sav_file_name()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def sav_file_name(self):
        """
            Cette fonction ouvre une boîte de dialogue pour sauvegarder le fichier ou l'on peut choisir le nom du fichier et le chemin.
        """
        if self.file_name:
            # Ouvrir la boîte de dialogue de sauvegarde
            self.sav_file_name, _ = QFileDialog.getSaveFileName(self, "Sauvegarder Fichier (.paf)", "", "Fichiers .paf (*.paf);;Tous les fichiers (*)")

            if self.sav_file_name:
                # Si un fichier a été sélectionné, appelez la fonction save_file avec le chemin du fichier
                save_file(self.sav_file_name)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Option pour ouvrir en lecture seule

        # Affichez la boîte de dialogue de sélection de fichier
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir Fichier (.paf)", "", "Fichiers .paf (*.paf);;Tous les fichiers (*)", options=options)

        if self.file_name:
            # Si un fichier a été sélectionné, appelez la fonction load_file avec le chemin du fichier
            self.setWindowTitle("Magne EOST - " + self.file_name)
            load_file(self.file_name)

            graph1()
            graph2()
            graph3()
            graph4()
            graph5()

            if self.fill:
                self.remplissage(True)
    
    def remplissage(self, checked):
        if self.file_name:
            if checked:
                for i in range(5):
                    fill_graph(i, True)
            else:
                for i in range(5):
                    fill_graph(i, False)
            self.fill = checked
            


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec_())