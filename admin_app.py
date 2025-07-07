import customtkinter as ctk
from admin_page import AdminFrame

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = ctk.CTk()
    app.title("Administration du Système")
    app.geometry("1400x900")
    app.minsize(1100, 700)
    user_info = {
        'prenom': 'Admin',
        'nom': 'Principal',
        'role': 'Admin',
        'email': 'admin@entreprise.com',
        'matricule': 'A00001'
    }
    admin_frame = AdminFrame(app, user_info)
    admin_frame.pack(fill="both", expand=True)
    app.mainloop() 