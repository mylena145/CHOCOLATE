import customtkinter as ctk

class BaseFrame(ctk.CTkFrame):
    """Classe de base pour toutes les frames avec gestion responsive"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        
        # Lier le redimensionnement
        self.bind("<Configure>", self._on_frame_resize)
    
    def on_window_resize(self, width, height):
        """Méthode appelée quand la fenêtre est redimensionnée - à surcharger"""
        pass
    
    def _on_frame_resize(self, event):
        """Gère le redimensionnement du frame"""
        if event.width > 100 and event.height > 100:
            self.on_window_resize(event.width, event.height) 