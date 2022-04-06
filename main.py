import json
from os import system

import dearpygui.dearpygui as dpg


country = ''
connected = False


def connect(server):    # Connects to the preferred server
    global connected

    system(f'nordvpn connect {server}')
    connected = True
    dpg.set_value('status', 'Status:\nConneted')


def disconnect():   # Disconnects from the server
    global connected

    system('nordvpn disconnect')
    connected = False
    dpg.set_value('status', 'Status:\nDisconnected')


def settings(sender, app_data): # Callbacks for the elements
    global country
    global connected

    if sender == 'combo_countries':
        country = app_data
    elif sender == 'button_connect':
        if not connected:
            connect(server=country)
        else:
            disconnect()

    elif sender == 'button_login':
        #proc = subprocess.Popen(['nordvpn login'], stdout=subprocess.PIPE, shell=True)
        #(out, err) = proc.communicate()
        #url = str(out).split('browser: ')[-1].strip().split('\\')[0]
        #webbrowser.open(url)
        #
        # Doesn't work at the moment because you don't stay logged in
        # That's why you have to register yourself via the terminal at the moment
        system('nordvpn login')
    elif sender == 'button_logout':
        system('nordvpn logout')
    elif sender == 'button_accountinfo':
        system('nordvpn account')

    else:
        with open('config.json', 'r+') as f:
            json_data = json.load(f)
            json_data[sender] = app_data
            f.seek(0)
            f.write(json.dumps(json_data))
            f.truncate()
        system(f'nordvpn set {sender} {app_data}')


def main(): # GUI (Graphical User Interface)
    countrylist = []

    with open('countries.json', 'r') as f:
        countries = json.load(f)

    for i in countries['countries']:
        countrylist.append(i['name'])

    dpg.create_context()
    dpg.create_viewport(title='NordVPN', width=680, height=420, resizable=False)

    with dpg.viewport_menu_bar():
        with dpg.menu(label='Account'):
            dpg.add_button(label='Login', tag='button_login', callback=settings)
            dpg.add_button(label='Logout', tag='button_logout', callback=settings)
            dpg.add_button(label='Account info', tag='button_accountinfo', callback=settings)

        with dpg.menu(label='Servers'):
            dpg.add_combo(countrylist, tag='combo_countries', callback=settings)
            dpg.add_button(label='(Dis-)Connect', tag='button_connect', callback=settings)
            dpg.add_text('Status:\nDisconnected', tag='status')

        with dpg.menu(label='Settings'):
            dpg.add_checkbox(label="autoconnect (automatically try to connect to VPN on operating system startup)", tag='autoconnect', callback=settings)
            dpg.add_checkbox(label="cybersec (automatically block suspicious websites: https://nordvpn.com/features/cybersec/)", tag='cybersec', callback=settings)
            dpg.add_input_text(label='dns1', default_value='1.1.1.1', tag='dns', callback=settings)
            dpg.add_checkbox(label="firewall (enables or disables use of the firewall)", default_value=True, tag='firewall', callback=settings)
            dpg.add_checkbox(label="ipv6 (nables or disables use of the ipv6)", tag='ipv6', callback=settings)
            dpg.add_checkbox(label="killswitch (blocks your device from accessing the Internet while not connected to the VPN)", tag='killswitch', callback=settings)
            dpg.add_checkbox(label="notify (Enables or disables notifications)", tag='notify', callback=settings)
            dpg.add_checkbox(label="obfuscate (bypass network traffic sensors which aim to detect usage of the protocol and log, throttle or block it)", tag='obfuscate', callback=settings)
            dpg.add_combo(['TCP', 'UDP'], label='Sets the protocol', default_value='UDP', tag='protocol', callback=settings)
            dpg.add_combo(['OpenVPN', 'NordLynx'], label='Sets the technology', default_value='OpenVPN', tag='technology', callback=settings)
            
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (24, 24, 24), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 7, category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (214, 214, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (214, 214, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (214, 214, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (214, 214, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (214, 214, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (214, 214, 0))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (24, 24, 24))

    dpg.bind_theme(global_theme)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == '__main__':
    main()
