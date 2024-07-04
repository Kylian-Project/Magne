import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import numpy as np
import keyboard

file_saved = True

def saved_or_not():
    """
        Fonction pour savoir si le fichier a été sauvegardé.
        Cette fonction permet de savoir si le fichier a été sauvegardé ou non.
        precondition: un fichier doit être ouvert
        postcondition: True si le fichier a été sauvegardé, False sinon
    """
    global file_saved
    return file_saved

def save_file(file_name):
    """
        Fonction pour sauvegarder les données dans un fichier .paf.
        Cette fonction permet de sauvegarder les données dans un fichier .paf.
        Elle remplacera les None par 999999.00 pour éviter les erreurs lors de la lecture du fichier.
        precondition: un fichier doit être ouvert
        postcondition: les données sont sauvegardées dans un fichier .paf
    """
    global file_saved
    # Vérifier si times est défini
    if 'times' not in globals():
        return

    # Créer une liste de tuples à partir des données
    zip_data_to_save = list(zip(times, data_col2, data_col3, data_col4, data_col5))

    # Écrire les données dans le fichier
    with open(file_name, 'w') as file:

        file_saved = True

        for t, d2, d3, d4, d5 in zip_data_to_save:
            if d2 is None:
                d2 = 999999.00
            if d3 is None:
                d3 = 999999.00
            if d4 is None:
                d4 = 999999.00
            if d5 is None:
                d5 = 999999.00
            file.write(f'{t}\t{d2}\t{d3}\t{d4}\t{d5}\n')

def load_file(file_name):
    global index, times, zip_data_col2, zip_data_col3, zip_data_col4, zip_data_col5, data_col2, data_col3, data_col4, data_col5, times, undo_data_col2, undo_data_col3, undo_data_col4, undo_data_col5


    # -------------------- Données / Variables -------------------- #

    times = []
    data_col2 = []
    data_col3 = []
    data_col4 = []
    data_col5 = []

    index = None  # Index du graphique actuel (ouvert en pleine ecran)

    # Initialisation de la pile pour stocker les états
    undo_data_col2 = []
    undo_data_col3 = []
    undo_data_col4 = []
    undo_data_col5 = []


    # Lecture du fichier .paf et extraction des données
    with open(file_name, 'r') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.split('\t')
        times.append(int(parts[0]))
        data_col2.append(float(parts[1]) if float(parts[1]) != 999999.00 else None)
        data_col3.append(float(parts[2]) if float(parts[2]) != 999999.00 else None)
        data_col4.append(float(parts[3]) if float(parts[3]) != 999999.00 else None)
        data_col5.append(float(parts[4]) if float(parts[4]) != 999999.00 else None)


    # Rassembler en liste de tuples
    zip_data_col2 = list(zip(times, data_col2))
    zip_data_col3 = list(zip(times, data_col3))
    zip_data_col4 = list(zip(times, data_col4))
    zip_data_col5 = list(zip(times, data_col5))

    CalculDernierGraph()

# ----------------------- Graphiques ----------------------- #

def CalculDernierGraph():
    global data_col6
    data_col6 = []
    for i in range(len(data_col2)):
        if data_col2[i] is not None and data_col3[i] is not None and data_col4[i] is not None and data_col5[i] is not None:
            data_col6.append(np.sqrt(data_col2[i]**2 + data_col3[i]**2 + data_col4[i]**2)- data_col5[i]) # Racine carrée de graph 1 au carré + graph 2 au carré + graph 3 au carré - graph 4
        else:
            data_col6.append(None)

# Création des graphiques
fig, axs = plt.subplots(5, 1, figsize=(12, 10), sharex=True)

# Graphique pour la colonne 2
def graph1():
    axs[0].clear()  # Effacer l'axe
    # axs[0].scatter([t for i, t in enumerate(times) if data_col2[i] is not None], 
    #             [d for d in data_col2 if d is not None], marker='o', s=1, color='black')
    axs[0].plot([t for i, t in enumerate(times) if data_col2[i] is not None], 
                [d for d in data_col2 if d is not None], 'k-', linewidth=1)  # Relier les points
    axs[0].set_xlabel('Temps (secondes)')
    axs[0].set_ylabel('')
    axs[0].set_title('')
    plt.draw()

# Graphique pour la colonne 3
def graph2():
    axs[1].clear()  # Effacer l'axe
    # axs[1].scatter([t for i, t in enumerate(times) if data_col3[i] is not None], 
    #             [d for d in data_col3 if d is not None], marker='o', s=1, color='black')
    axs[1].plot([t for i, t in enumerate(times) if data_col3[i] is not None], 
                [d for d in data_col3 if d is not None], 'k-', linewidth=1)  # Relier les points
    axs[1].set_xlabel('Temps (secondes)')
    axs[1].set_ylabel('')
    axs[1].set_title('')
    plt.draw()

# Graphique pour la colonne 4
def graph3():
    axs[2].clear()  # Effacer l'axe
    # axs[2].scatter([t for i, t in enumerate(times) if data_col4[i] is not None], 
    #             [d for d in data_col4 if d is not None], marker='o', s=1, color='black')
    axs[2].plot([t for i, t in enumerate(times) if data_col4[i] is not None], 
                [d for d in data_col4 if d is not None], 'k-', linewidth=1)  # Relier les points
    axs[2].set_xlabel('Temps (secondes)')
    axs[2].set_ylabel('')
    axs[2].set_title('')
    plt.draw()

# Graphique pour la colonne 5
def graph4():
    axs[3].clear()  # Effacer l'axe
    # axs[3].scatter([t for i, t in enumerate(times) if data_col5[i] is not None], 
    #             [d for d in data_col5 if d is not None], marker='o', s=1, color='black')
    axs[3].plot([t for i, t in enumerate(times) if data_col5[i] is not None], 
                [d for d in data_col5 if d is not None], 'k-', linewidth=1)  # Relier les points
    axs[3].set_xlabel('Temps (secondes)')
    axs[3].set_ylabel('')
    axs[3].set_title('')
    plt.draw()

# Dernier graphique  qui fait la racine carrée de graph 1 au carré + graph 2 au carré + graph 3 au carré - graph 4
def graph5():
    axs[4].clear()  # Effacer l'axe
    # axs[4].scatter([t for i, t in enumerate(times) if data_col6[i] is not None], 
    #             [d for d in data_col6 if d is not None], marker='o', s=1, color='black')
    axs[4].plot([t for i, t in enumerate(times) if data_col6[i] is not None], 
                [d for d in data_col6 if d is not None], 'r-', linewidth=1)  # Relier les points
    axs[4].set_xlabel('Temps (secondes)')
    axs[4].set_ylabel('')
    axs[4].set_title('')
    plt.draw()

# ----------------------- Fonctions ----------------------- #

filled = False
def fill_graph(index, on_off):
    global filled

    if index == 4:
        color = 'red'
    else:
        color = 'black'

    filled = on_off
    if on_off:
        axs[index].fill_between([t for i, t in enumerate(times) if [data_col2, data_col3, data_col4, data_col5, data_col6][index][i] is not None], 
                [min(d for d in [data_col2, data_col3, data_col4, data_col5, data_col6][index] if d is not None)] * len([d for d in [data_col2, data_col3, data_col4, data_col5, data_col6][index] if d is not None]), 
                [d for d in [data_col2, data_col3, data_col4, data_col5, data_col6][index] if d is not None], alpha=0.3, color=color)
    else:
        for collection in axs[index].collections:
            collection.remove()
    plt.draw()

def zoom_graph(event):
    """
        Fonction pour afficher un graphique en plein écran en double-cliquant.
        Cette fonction permet d'afficher un graphique en plein écran en double-cliquant dessus.
        precondition: les graphiques principeux doivent être ouverts
        postcondition: le graphique est affiché en plein écran
    """
    global lasso, index, axsv2
    if event.dblclick and 'times' in globals():
        ax = event.inaxes
        if ax:
            fig, axsv2 = plt.subplots(1, 1, figsize=(12, 10), sharex=True)  # Obtenez l'axe (axsv2)

            index = np.where(axs == ax)[0][0]
            if index == 4:
                return
            axsv2.scatter(times, [data_col2, data_col3, data_col4, data_col5][index], marker='o', s=1)
            axsv2.set_xlabel('Temps (secondes)')
            axsv2.set_ylabel(f'Colonne {index+2}')
            axsv2.set_title(f'Graphique de la colonne {index+2}')

            # Ajouter la sélection de points
            lasso = LassoSelector(axsv2, lambda verts: rm_select_point(verts, axsv2))

            plt.tight_layout() # Optimise les marges
            plt.get_current_fig_manager().window.showMaximized()  # Maximise la fenêtre principale

            fig.canvas.mpl_connect('close_event', on_close)

def clear_graph():
    global index, data_col2, data_col3, data_col4, data_col5, axsv2
    """
        Nettoie le graphique en enlevant les point trop éloigné de la courbe.
        Cette fonction parcourt les point de la courbe puis vérifie si chaque point n'a pas une différence supérieur à 1 avec le point précédent.
        Si c'est le cas, on l'ajoute à une liste de point à supprimer sous la forme [[(1.0, -169.96)], [(2.0, -179.06)], ...].
        precondition: le graphique doit être ouvert
        postcondition: le graphique est nettoyé
    """
    previous = 0
    to_remove = []
    seuille = 0.2
    if index == 3:
        seuille = 2.0 # Pour le graph 4, on augmente le seuille car les valeurs sont plus éloignées 1 point sur 10
    
    for i in range(len([data_col2, data_col3, data_col4, data_col5][index])):
        if previous == 0 and [data_col2, data_col3, data_col4, data_col5][index][i] is not None:
            previous = [data_col2, data_col3, data_col4, data_col5][index][i]
        if [data_col2, data_col3, data_col4, data_col5][index][i] is not None:
            if abs(abs([data_col2, data_col3, data_col4, data_col5][index][i]) - abs(previous)) > seuille:
                if [(times[i], [data_col2, data_col3, data_col4, data_col5][index][i])][0] not in clear_undo(index):
                    to_remove+=[(times[i], [data_col2, data_col3, data_col4, data_col5][index][i])]
            else:
                previous = [data_col2, data_col3, data_col4, data_col5][index][i]
    
    if len(to_remove) == 0: return
    [undo_data_col2, undo_data_col3, undo_data_col4, undo_data_col5][index].append(to_remove)

    remove_point(axsv2, to_remove)

def clear_undo(index):
    """
        Fonction pour obtenir la liste des points supprimés pour éviter de supprimer des point déjà supprimer avec l'algo de nettoyage.
        Cette fonction permet de retourner la liste des points supprimés.
        precondition: le graphique doit être ouvert
        postcondition: la liste des points supprimés est retournée
    """
    temp_liste = [item for sublist in [undo_data_col2, undo_data_col3, undo_data_col4, undo_data_col5][index] for item in sublist]

    return temp_liste


def remove_point(ax, points_to_remove):
    """
        Fonction pour supprimer des points passé en paramètre.
        Cette fonction permet de supprimer n'importe quel point sur le graphique.
        precondition: le graphique doit être ouvert
        postcondition: les points sélectionnés sont supprimés
    """
    # Obtenez les données actuelles du scatter plot
    x_data, y_data = ax.collections[0].get_offsets().T

    # Créez un tableau booléen indiquant quels points doivent être supprimés
    to_remove = np.zeros(len(x_data), dtype=bool)
    for point in points_to_remove:
        mask = (x_data == point[0]) & (y_data == point[1])
        to_remove |= mask

    # Supprimez les points spécifiés
    x_data = np.delete(x_data, np.where(to_remove))
    y_data = np.delete(y_data, np.where(to_remove))

    # Mettez à jour les données du scatter plot
    ax.collections[0].set_offsets(np.column_stack((x_data, y_data)))

    # Rafraîchissez le graphique
    ax.figure.canvas.draw()
    

def rm_select_point(verts, ax):
    """
        Fonction pour supprimer les points sélectionnés avec le lasso.
        Cette fonction permet de supprimer les points sélectionnés en utilisant la fonction points_in_poly.
        precondition: le graphique doit être ouvert
        postcondition: les points sélectionnés sont supprimés
    """
    global undo_data_col2, undo_data_col3, undo_data_col4, undo_data_col5, scatter_plot, selected_points, index
    
    # Obtenir les données de points du graphique actuel
    scatter_plot = ax.collections[0]
    x, y = scatter_plot.get_offsets().T
    
    # Vérifier quels points sont dans le polygone

    ind = np.nonzero(points_in_poly(verts, x, y))[0]
    
    # Afficher les coordonnées des points sélectionnés
    selected_points = [(int(x[i]), y[i]) for i in ind]
    
    if len(selected_points) > 0:
        # Supprimer les points sélectionnés
        scatter_plot.set_offsets(np.delete(scatter_plot.get_offsets(), ind, axis=0))

        [undo_data_col2, undo_data_col3, undo_data_col4, undo_data_col5][index].append(selected_points)

    plt.draw()


def points_in_poly(verts, x, y):
    """
        Fonction pour vérifier quels points sont dans le polygone (lasso).
        Cette fonction vérifie si les points sont dans le polygone en utilisant la fonction contains_points de matplotlib.path.Path.
        precondition: le graphique doit être ouvert
        postcondition: les points dans le polygone sont retournés
    """
    path = Path(verts)
    return path.contains_points(np.column_stack((x, y)))

def cancel_point(points_a_ajouter):
    """
        Fonction pour annuler la dernière suppression de points.
        Cette fonction permet de réafficher les points supprimés précédemment.
        precondition: le graphique doit être ouvert
        postcondition: le graphique est mis à jour
    """
    # Obtenir les données de points du graphique actuel
    scatter_plot = axsv2.collections[0]

    scatter_plot.set_offsets(np.append(scatter_plot.get_offsets(), points_a_ajouter, axis=0))
    [undo_data_col2, undo_data_col3, undo_data_col4, undo_data_col5][index].pop()
    plt.draw()


def on_close(event):
    """
        Fonction appellé lorsque le graphique en plein écran est fermé.
        Cette fonction permet de mettre à jour les données du graphique principal.
        precondition: le graphique en plein écran doit être fermé
        postcondition: les données du graphique principal sont mises à jour
    """
    global file_saved, index, undo_data_col2, undo_data_col3, undo_data_col4, undo_data_col5, zip_data_col2, zip_data_col3, zip_data_col4, zip_data_col5, data_col2, data_col3, data_col4, data_col5
    
    undo_data = undo_data_col2 + undo_data_col3 + undo_data_col4 + undo_data_col5
    if not undo_data:
        return
    
    file_saved = False
    # Créer un ensemble des premiers éléments de chaque tuple
    liste_tuples_first = set(t[0] for sublist in undo_data for t in sublist)

    # Remplacer le deuxième élément de chaque tuple par None si le premier élément est déjà dans l'ensemble
    liste_tuples = [(t[0], None) if t[0] in liste_tuples_first else t for t in [zip_data_col2, zip_data_col3, zip_data_col4, zip_data_col5][index]]

    [undo_data_col2, undo_data_col3, undo_data_col4, undo_data_col5][index].clear()

    # Effacer et mettre à jour les listes de données zip et data
    zip_data, data = [zip_data_col2, zip_data_col3, zip_data_col4, zip_data_col5][index], [data_col2, data_col3, data_col4, data_col5][index]
    zip_data.clear()
    data.clear()
    for t in liste_tuples:
        zip_data.append(t)
        data.append(t[1])

    # Redessiner le graphique
    graph_functions = [graph1, graph2, graph3, graph4, graph5]

    # Appelez la fonction correspondant à l'index
    if index is not None and index < len(graph_functions):
        graph_functions[index]()

    CalculDernierGraph()
    graph5()
    
    if filled:
        fill_graph(index, True)
        fill_graph(4, True)

    fig.canvas.draw()
    index = None
    

def on_key_event(keyboard_event):
    """
        Fonction pour gérer les événements de clavier.
        Cette fonction permet de gérer les événements de clavier et donc détecter les touche ctrl+c et ctrl+z.
        precondition: le graphique doit être ouvert
        postcondition: les événements de clavier sont gérés
    """
    global index
    if keyboard_event.event_type == keyboard.KEY_DOWN:
        # Vérifier si Ctrl et Z sont pressées simultanément
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('z'):
            # Appeler la fonction pour annuler la dernière suppression de points
            if len([undo_data_col2, undo_data_col3, undo_data_col4, undo_data_col5][index]) > 0:
                cancel_point([undo_data_col2, undo_data_col3, undo_data_col4, undo_data_col5][index][-1])
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('c') and index is not None:
            clear_graph()


# Ajouter la fonction de rappel pour les événements de clavier
keyboard.hook(on_key_event)

# Connecte la fonction zoom_graph à l'événement de clic
fig.canvas.mpl_connect('button_press_event', zoom_graph)

if __name__ == "__main__":
    # Affiche les graphiques
    graph1()
    graph2()
    graph3()
    graph4()
    graph5()
    for i in range(4):
        fill_graph(i)

    # Affichage via matplotlib
    plt.tight_layout()
    plt.get_current_fig_manager().window.showMaximized()  # Maximise la fenêtre principale
    plt.show()