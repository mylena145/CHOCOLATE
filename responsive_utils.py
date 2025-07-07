import customtkinter as ctk
from typing import Dict, Any, Optional
import json
import os
from datetime import datetime

class ResponsiveFrame(ctk.CTkFrame):
    """Classe de base pour les frames responsive"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.responsive_config = {}
        
        # Lier le redimensionnement
        self.bind("<Configure>", self._on_frame_resize)
        
        # Initialiser la configuration responsive
        self._update_responsive_config()
    
    def _update_responsive_config(self):
        """Met à jour la configuration responsive depuis le parent"""
        if hasattr(self.parent, 'get_responsive_config'):
            self.responsive_config = self.parent.get_responsive_config()
        else:
            # Configuration par défaut
            self.responsive_config = {
                'sidebar_width': 240,
                'card_columns': 3,
                'table_compact': False,
                'font_size_small': 12,
                'font_size_normal': 14,
                'font_size_large': 18,
                'padding_small': 10,
                'padding_normal': 15,
                'padding_large': 20
            }
    
    def on_window_resize(self, width: int, height: int):
        """Méthode appelée quand la fenêtre est redimensionnée"""
        self._update_responsive_config()
        self._adapt_layout_to_size(width, height)
    
    def _on_frame_resize(self, event):
        """Gère le redimensionnement du frame"""
        if event.width > 100 and event.height > 100:
            self._adapt_layout_to_size(event.width, event.height)
    
    def _adapt_layout_to_size(self, width: int, height: int):
        """Adapte la mise en page selon la taille - à surcharger dans les classes enfants"""
        pass
    
    def get_breakpoint(self, width: int) -> str:
        """Retourne le breakpoint actuel selon la largeur"""
        if width < 768:
            return 'mobile'
        elif width < 1024:
            return 'tablet'
        elif width < 1400:
            return 'desktop'
        else:
            return 'large'
    
    def configure_widget_responsive(self, widget, widget_type: str = 'normal'):
        """Configure un widget selon la configuration responsive"""
        if not self.responsive_config:
            return
        
        if widget_type == 'title':
            font_size = self.responsive_config.get('font_size_large', 18)
        elif widget_type == 'small':
            font_size = self.responsive_config.get('font_size_small', 12)
        else:
            font_size = self.responsive_config.get('font_size_normal', 14)
        
        if hasattr(widget, 'configure') and 'font' in widget.configure():
            widget.configure(font=ctk.CTkFont(size=font_size))

def create_responsive_grid(parent, widgets, columns: int = 3, padding: int = 10):
    """Crée une grille responsive avec les widgets donnés"""
    for i, widget in enumerate(widgets):
        row = i // columns
        col = i % columns
        widget.grid(row=row, column=col, sticky="ew", padx=padding, pady=padding)
    
    # Configurer les poids des colonnes
    for i in range(columns):
        parent.grid_columnconfigure(i, weight=1)

def create_responsive_cards_frame(parent, title: str = "", columns: int = 3):
    """Crée un frame pour les cartes avec titre responsive"""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    
    if title:
        title_label = ctk.CTkLabel(
            frame, 
            text=title, 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f2937"
        )
        title_label.pack(anchor="w", padx=20, pady=(20, 10))
    
    cards_frame = ctk.CTkFrame(frame, fg_color="transparent")
    cards_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Configurer la grille
    for i in range(columns):
        cards_frame.grid_columnconfigure(i, weight=1)
    
    return frame, cards_frame

def create_responsive_table(parent, headers: list, data: list, compact: bool = False):
    """Crée une table responsive"""
    table_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=8)
    
    # En-têtes
    header_frame = ctk.CTkFrame(table_frame, fg_color="#f8fafc", corner_radius=8)
    header_frame.pack(fill="x", padx=1, pady=1)
    
    for i, header in enumerate(headers):
        if compact and i > 2:  # Masquer certaines colonnes en mode compact
            continue
        label = ctk.CTkLabel(
            header_frame, 
            text=header, 
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#374151"
        )
        label.grid(row=0, column=i, sticky="ew", padx=15, pady=12)
        header_frame.grid_columnconfigure(i, weight=1)
    
    # Données
    for row_idx, row_data in enumerate(data):
        row_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=1, pady=1)
        
        for col_idx, cell_data in enumerate(row_data):
            if compact and col_idx > 2:  # Masquer certaines colonnes en mode compact
                continue
            label = ctk.CTkLabel(
                row_frame, 
                text=str(cell_data), 
                font=ctk.CTkFont(size=12),
                text_color="#6b7280"
            )
            label.grid(row=0, column=col_idx, sticky="ew", padx=15, pady=8)
            row_frame.grid_columnconfigure(col_idx, weight=1)
    
    return table_frame 

class ThemeToggleButton(ctk.CTkButton):
    """Bouton de basculement de thème réutilisable avec sauvegarde intelligente"""
    
    def __init__(self, parent, app_instance, **kwargs):
        self.app = app_instance
        self.settings_file = "theme_settings.json"
        self.current_theme = self._load_theme_state()
        
        # Icônes pour les thèmes
        self.light_icon = "☀️"
        self.dark_icon = "🌙"
        
        # Couleurs adaptatives
        self.light_colors = {
            "fg_color": "#f0f0f0",
            "hover_color": "#e0e0e0", 
            "text_color": "#333333",
            "border_color": "#cccccc"
        }
        
        self.dark_colors = {
            "fg_color": "#2d2d2d",
            "hover_color": "#3d3d3d",
            "text_color": "#ffffff", 
            "border_color": "#555555"
        }
        
        # Configuration du bouton
        button_config = {
            "text": f"{self.dark_icon if self.current_theme == 'light' else self.light_icon} Mode Sombre" if self.current_theme == 'light' else f"{self.light_icon} Mode Clair",
            "width": 140,
            "height": 32,
            "corner_radius": 16,
            "font": ctk.CTkFont(size=12, weight="bold"),
            "command": self._toggle_theme
        }
        
        # Appliquer les couleurs selon le thème actuel
        colors = self.dark_colors if self.current_theme == 'dark' else self.light_colors
        button_config.update(colors)
        
        super().__init__(parent, **button_config, **kwargs)
        
        # Appliquer le thème initial
        self._apply_current_theme()
    
    def _load_theme_state(self):
        """Charge l'état du thème depuis le fichier de sauvegarde"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    return settings.get('theme', 'light')
            return 'light'
        except Exception as e:
            print(f"Erreur lors du chargement du thème: {e}")
            return 'light'
    
    def _save_theme_state(self, theme):
        """Sauvegarde l'état du thème de manière intelligente"""
        try:
            settings = {}
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            
            settings['theme'] = theme
            settings['last_updated'] = datetime.now().isoformat()
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            print(f"Thème sauvegardé: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du thème: {e}")
    
    def _toggle_theme(self):
        """Bascule entre les thèmes clair et sombre"""
        try:
            # Déterminer le nouveau thème
            new_theme = 'dark' if self.current_theme == 'light' else 'light'
            
            # Mettre à jour l'état interne
            self.current_theme = new_theme
            
            # Mettre à jour l'apparence du bouton
            self._update_button_appearance()
            
            # Appliquer le thème à l'application
            self._apply_theme_to_app(new_theme)
            
            # Sauvegarder l'état
            self._save_theme_state(new_theme)
            
            # Afficher une notification
            self._show_theme_notification(new_theme)
            
        except Exception as e:
            print(f"Erreur lors du basculement de thème: {e}")
    
    def _update_button_appearance(self):
        """Met à jour l'apparence du bouton selon le thème"""
        if self.current_theme == 'dark':
            self.configure(
                text=f"{self.light_icon} Mode Clair",
                fg_color=self.dark_colors["fg_color"],
                hover_color=self.dark_colors["hover_color"],
                text_color=self.dark_colors["text_color"],
                border_color=self.dark_colors["border_color"]
            )
        else:
            self.configure(
                text=f"{self.dark_icon} Mode Sombre",
                fg_color=self.light_colors["fg_color"],
                hover_color=self.light_colors["hover_color"],
                text_color=self.light_colors["text_color"],
                border_color=self.light_colors["border_color"]
            )
    
    def _apply_theme_to_app(self, theme):
        """Applique le thème à toute l'application"""
        try:
            # Notifier l'application principale
            if hasattr(self.app, 'notify_theme_change'):
                self.app.notify_theme_change(theme)
            
            # Appliquer le thème global
            ctk.set_appearance_mode(theme)
            
            print(f"Thème appliqué à l'application: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de l'application du thème: {e}")
    
    def _apply_current_theme(self):
        """Applique le thème actuel au démarrage"""
        try:
            if self.current_theme == 'dark':
                ctk.set_appearance_mode("dark")
                if hasattr(self.app, 'notify_theme_change'):
                    self.app.notify_theme_change("dark")
            else:
                ctk.set_appearance_mode("light")
                if hasattr(self.app, 'notify_theme_change'):
                    self.app.notify_theme_change("light")
                    
        except Exception as e:
            print(f"Erreur lors de l'application du thème initial: {e}")
    
    def _show_theme_notification(self, theme):
        """Affiche une notification de changement de thème"""
        try:
            # Créer une fenêtre de notification temporaire
            notification = ctk.CTkToplevel()
            notification.title("")
            notification.geometry("300x80")
            notification.configure(fg_color="#1a1a1a" if theme == 'dark' else "#ffffff")
            notification.attributes('-topmost', True)
            
            # Positionner la notification
            x = self.winfo_rootx() + 50
            y = self.winfo_rooty() - 100
            notification.geometry(f"+{x}+{y}")
            
            # Contenu de la notification
            icon = "🌙" if theme == 'dark' else "☀️"
            text = f"Mode Sombre Activé" if theme == 'dark' else "Mode Clair Activé"
            
            ctk.CTkLabel(
                notification,
                text=f"{icon} {text}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#ffffff" if theme == 'dark' else "#333333"
            ).pack(pady=20)
            
            # Fermer automatiquement après 2 secondes
            notification.after(2000, notification.destroy)
            
        except Exception as e:
            print(f"Erreur lors de l'affichage de la notification: {e}")
    
    def get_current_theme(self):
        """Retourne le thème actuel"""
        return self.current_theme
    
    def set_theme(self, theme):
        """Force l'application d'un thème spécifique"""
        if theme in ['light', 'dark'] and theme != self.current_theme:
            self.current_theme = theme
            self._update_button_appearance()
            self._apply_theme_to_app(theme)
            self._save_theme_state(theme) 