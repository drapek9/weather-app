from tkinter import *
import requests

# Window
window = Tk()
window.title("Počasí")
window.iconbitmap("img/Weather.ico")
window.geometry("550x300+700+100")
window.resizable(False, False)

# Fonty
date_font = ("Times New Roman", 15)
date_number_font = ("Times New Roman", 15)
button_font = ("Times New Roman", 10)
choose_font = ("Arial", 13)

# Barva pozadí
bg_color = "#b9c9d3"
window.config(bg=bg_color)


# Hlavní funkce - Změna města, údalů, aktulizace atd.
def count():

    # Města a jejich umístění
    cities = {
        "Chrast": ["49.9021", "15.934"],
        "Praha": ["50.088", "14.4208"],
        "Pardubice": ["50.0408", "15.7766"],
        "Chrudim": ["49.9511", "15.7956"],
        "Brno": ["49.1952", "16.608"],
        "Boskovice": ["49.4875", "16.66"],
        "Litoměřice": ["50.5335", "14.1318"],
        "Ponikev": ["49.6252", "16.8834"]
    }
    # Načtení vybraného města
    the_city = choose_city.get()

    # Město se uloží jako poslední a po dalším spuštění se nastaví znovu
    def remember_city():
        with open("Cities.txt", "w") as file:
            file.write(the_city)
    remember_city()
    # Cesta k webu na počasí
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={cities[the_city][0]}&longitude={cities[the_city][1]}&current=temperature_2m,apparent_temperature&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,daylight_duration,uv_index_max,rain_sum,snowfall_sum,precipitation_probability_max,wind_speed_10m_max&timezone=Europe%2FBerlin&forecast_days=3")
    # Přečtení cesty
    data = response.json()

    # datumy v listu, které slouží k informacím do dalších dnů (v listu kvůli cyklu)
    days_date = [first_day_date_label, second_day_date_label, third_day_date_label]

    # Nastavení teploty a pocitové teploty
    now_celsia = round(data["current"]["temperature_2m"])
    feel_now_celsia = round(data["current"]["apparent_temperature"])
    # Vypsání teploty a pocitové teploty
    right_now_number_label.config(text=f"{now_celsia} °C")
    feel_now_text_number_label.config(text=f"Pocitová teplota {feel_now_celsia} °C")

    # Vypsání 3 datumů
    for day_range in range(3):
        date = data["daily"]["time"][day_range]
        days_date[day_range].config(text=f"{date[-2:]}.{date[5:7]}.{date[:4]}")

    # Nastavení největších a nejmenšich teplot 3 datumů (zatím v listu)
    max_celsias = data["daily"]["temperature_2m_max"]
    min_celsias = data["daily"]["temperature_2m_min"]

    # Labely teplot pod 3 datumy
    days_numbers = [first_day_number_label, second_day_number_label, third_day_number_label]

    # Vypsání "nejmenších/největších" teplot
    for celsia_range in range(3):
        one_max_celsia = round(max_celsias[celsia_range])
        one_min_celsia = round(min_celsias[celsia_range])

        days_numbers[celsia_range].config(text=f"{one_max_celsia}/{one_min_celsia} °C")

    # Získání jakou další funkci chce uživatel vidět
    user_want = choose_you_wanna.get()

    # Uložení funkce pro načtení po novém spuštění
    def remember_choose():
        with open("Choose_stats.txt", "w") as file_2:
            file_2.write(user_want)
    remember_choose()

    # Texty funkcí v listu (pro cyklus)
    choose_info = [first_choose_info, second_choose_info, third_choose_info]
    # Nastavení co uživatel chce
    # Prav. srážek MAX
    if user_want == "Prav. srážek MAX":
        for info_index in range(3):
            choose_info[info_index].config(text=f"{data["daily"]["precipitation_probability_max"][info_index]}%",
                                           fg="#07195c")
    # Uv index
    elif user_want == "Uv index":
        for info_index in range(3):
            the_number = round(data["daily"]["uv_index_max"][info_index])
            choose_info[info_index].config(text=f"Uv {the_number}")
            # Barvy podle velikosti Uv indexu
            if the_number >= 0 and the_number <= 2:
                choose_info[info_index].config(fg="#286f1f")
            elif the_number > 2 and the_number <= 4:
                choose_info[info_index].config(fg="#ffff25")
            elif the_number > 4 and the_number <= 6:
                choose_info[info_index].config(fg="#e57400")
            elif the_number > 6 and the_number <= 9:
                choose_info[info_index].config(fg="#e12400")
            elif the_number > 9:
                choose_info[info_index].config(fg="#3e0b2f")

    # Východ slunce
    elif user_want == "Východ slunce":
        for info_index in range(3):
            choose_info[info_index].config(text=data["daily"]["sunrise"][info_index][-5:], fg="black")
    # Západ slunce
    elif user_want == "Západ slunce":
        for info_index in range(3):
            choose_info[info_index].config(text=data["daily"]["sunset"][info_index][-5:], fg="black")
    # Rychlost větru MAX
    elif user_want == "Rychl. větru MAX":
        for info_index in range(3):
            the_number = round(data["daily"]["wind_speed_10m_max"][info_index])
            choose_info[info_index].config(text=f"{the_number}km/h")
            # Barvy podle rychlosti větru
            if the_number >= 0 and the_number <= 7:
                choose_info[info_index].config(fg="#2988e2")
            elif the_number > 7 and the_number <= 11:
                choose_info[info_index].config(fg="#286f1f")
            elif the_number > 11 and the_number <= 19:
                choose_info[info_index].config(fg="#ffff25")
            elif the_number > 19 and the_number <= 38:
                choose_info[info_index].config(fg="#e57400")
            elif the_number > 38 and the_number <= 74:
                choose_info[info_index].config(fg="#e12400")
            elif the_number > 74 and the_number <= 117:
                choose_info[info_index].config(fg="#bf2391")
            elif the_number > 117:
                choose_info[info_index].config(fg="#3e0b2f")
    # Doba denního světla
    elif user_want == "Doba den. světla":
        for info_index in range(3):
            # Přepočítání na minuty - přepočítání na hodiny a jejich desetinná místa - zaokrouhlení
            first_number = float(data["daily"]["daylight_duration"][info_index]) / 60
            second_number = round(first_number / 60, 2)
            # aby se nestalo, že budeme mít délku 3 než čtyři a 4 místo 5
            second_number = str("{:.2f}".format(second_number))

            # Pokud je čas třeba 8.56
            if len(second_number) == 4:
                # Vypočítání minut po mocí (56 * 60) / 100 a zaokrouhlení
                last_numbers = round((int(second_number[2:]) * 60) / 100)
                choose_info[info_index].config(text=f"{second_number[0]}:{last_numbers}")
            # Pokud je čas třeba 12.89
            elif len(second_number) == 5:
                # Vypočítání minut po mocí (89 * 60) / 100 a zaokrouhlení
                last_numbers = round((int(second_number[3:]) * 60) / 100)
                choose_info[info_index].config(text=f"{second_number[:2]}:{last_numbers}")
            choose_info[info_index].config(fg="black")
    # Součet deště
    elif user_want == "Součet deště":
        for info_index in range(3):
            choose_info[info_index].config(text=f"{data["daily"]["rain_sum"][info_index]} mm", fg="#07195c")
    # Součet sněžení
    elif user_want == "Součet sněžení":
        for info_index in range(3):
            choose_info[info_index].config(text=f"{data["daily"]["snowfall_sum"][info_index]} cm", fg="black")


# Texty
# Text "aktuální teplota"
right_now_text_label = Label(window, font=("Times New Roman", 17), text="Aktuální teplota", bg=bg_color)
right_now_text_label.place(x=130, y=20)

# Aktuální teplota
right_now_number_label = Label(window, font=("Times New Roman", 30), bg=bg_color)
right_now_number_label.place(x=265, y=77, anchor="e")

# Pocitová teplota
feel_now_text_number_label = Label(window, font=("Times New Roman", 12), bg=bg_color, fg="#3b3b3b")
feel_now_text_number_label.place(x=270, y=72)

# 1. datum
first_day_date_label = Label(window, font=date_font, bg=bg_color)
first_day_date_label.place(x=95, y=170)

# 2.datum
second_day_date_label = Label(window, font=date_font, bg=bg_color)
second_day_date_label.place(x=225, y=170)

# 3. datum
third_day_date_label = Label(window, font=date_font, bg=bg_color)
third_day_date_label.place(x=360, y=170)

# Teplota 1. datumu
first_day_number_label = Label(window, font=date_number_font, bg=bg_color, fg="#3b3b3b")
first_day_number_label.place(x=143, y=215, anchor="center")

# Teplota 2. datumu
second_day_number_label = Label(window, font=date_number_font, bg=bg_color, fg="#3b3b3b")
second_day_number_label.place(x=273, y=215, anchor="center")

# Teplota 3. datumu
third_day_number_label = Label(window, font=date_number_font, bg=bg_color, fg="#3b3b3b")
third_day_number_label.place(x=408, y=215, anchor="center")

# 1. volitelná informace
first_choose_info = Label(window, font=choose_font, bg=bg_color)
first_choose_info.place(x=142, y=245, anchor="center")

# 2. volitelná informace
second_choose_info = Label(window, font=choose_font, bg=bg_color)
second_choose_info.place(x=272, y=245, anchor="center")

# 3. volitelná informace
third_choose_info = Label(window, font=choose_font, bg=bg_color)
third_choose_info.place(x=412, y=245, anchor="center")

# Text autora (Můj)
author_label = Label(window, text="Šimon Drápal 29.11.2023", bg=bg_color, font=("Times New Roman", 8))
author_label.place(x=420, y=280)

# Tlačítko pro aktualizaci
button_update = Button(window, font=button_font, text="Aktualizovat", command=count, bg="#000", fg="white",
                       activebackground="#65899f")
button_update.place(x=450, y=15)

# Pokud zmáčkneme enter, spuštění aktualizace
window.bind("<Return>", lambda event: count())

# Vyzkoušení otevření minulého města a volitelné informace
try:
    with open("Cities.txt", "r") as file:
        city = file.read()
    with open("Choose_stats.txt", "r") as file_2:
        stat = file_2.read()
# Jinak město = Chrast, volitelná = Prav. srážek MAX
except:
    city = "Chrast"
    stat = "Prav. srážek MAX"

# Výběry
# Výběr volitelné informace
choose_you_wanna = StringVar(window)
# Nastavení stat
choose_you_wanna.set(stat)
choose_you_wanna_options = OptionMenu(window, choose_you_wanna, "Prav. srážek MAX", "Uv index",
                                      "Rychl. větru MAX", "Součet deště", "Východ slunce", "Západ slunce",
                                      "Doba den. světla", "Součet sněžení")
choose_you_wanna_options.config(highlightthickness=0, bg="#d5d5d5")
choose_you_wanna_options.place(x=270, y=140, anchor="center")

# Výběr města
choose_city = StringVar(window)
# Nastavení city
choose_city.set(city)
choose_city_option = OptionMenu(window, choose_city, "Chrast", "Chrudim", "Pardubice", "Praha", "Boskovice",
                                "Ponikev", "Litoměřice", "Brno")
choose_city_option.config(font=button_font, highlightthickness=0, bg="#d5d5d5")
choose_city_option.place(x=451, y=50)

# Zavolání aktualizace při spuštění
count()

# Cyklus aplikace
window.mainloop()
