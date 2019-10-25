import eel

eel.init('web')


@eel.expose
def my_python_method(param1, param2):
    print(param1 + param2)


eel.start('index.html', mode='chrome-app', port=3000, cmdline_args=['--start-fullscreen', '--browser-startup-dialog'])
