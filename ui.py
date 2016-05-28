import gtk
from autoTransliterate.list_generator import *
from autoTransliterate.data import *

start = 0
cursorPosition = 0
run_once2 = 0
run_once = 0 
word = ''
final_length=0
string = []

w  = gtk.Window()
combobox = gtk.combo_box_new_text()
tv = gtk.TextView()
buffr = gtk.TextBuffer()

def keyPress_func(widget,event):
    keyname = gtk.gdk.keyval_name(event.keyval)
    if keyname not in {"space","Up","Down","BackSpace","Return","Right","Left"}:
        s=keyname
        string.append(s)
        del_combo(combobox)
    else:
        if keyname in "BackSpace":
            del string[-1]
        elif keyname in "space":
           
            global word
            word =''.join(string)
            global start
            end_length = start + len(word)+1
            final_length=end_length
            global run_once2
            run_once2 = 0
            global iters
            print "IN THE PRINT AREA START VALUE",start
            iters = buffr.get_iter_at_offset(start)
            itere = buffr.get_iter_at_offset(end_length)
            list_generated1 = search(word)
            list_generated2 = generate(word)
            Final_list = list_generated1 + list_generated2 
            buffr.delete(iters,itere)
            global string
            string =[] 
            combo_generate(combobox,Final_list)
        elif keyname in "Return":
            global cursorPosition
            global start 
            global string
            string = []
            start  =cursorPosition  +1
        else :
            combo_response(combobox)
           
def textview_response(tv):
    tv.grab_focus()
    
    
def combo_response(combobox):
    combobox.grab_focus()
    return
def combo_generate(combobox,list_generated):
    x="Devanagari_script... "
    
    combobox.append_text(x)
    combobox.append_text(word)
    for i in list_generated:
        combobox.append_text(i)
    if run_once == 0:
        combobox.connect('changed',changed_cb)
    combobox.set_active(0)
    combobox.show()
    combobox.popup()
    return 

def printScreen(devnagiri): 
    print "word to replace",word
    print "word to print ",devnagiri
    update_string(word, devnagiri)
    devprint = devnagiri+ '  ' 
    buffr.insert_at_cursor(devprint)
    strlist = devprint.decode("utf-8")
    len_dev = len(strlist)#length of devnagiri script
    print " in print screen ",len_dev
    global start
    start = start + len_dev 
    global run_once2
    run_once2=1
    textview_response(tv)
    return

def changed_cb(combobox):
    global run_once
    run_once = 1
    model = combobox.get_model()
    index = combobox.get_active()
    if index:
        daat = model[index][0]
        data_selected(daat)
    return
    
def data_selected(devnagiri):
    if run_once2 == 0:
        printScreen(devnagiri)
    return 
    
def del_combo(combobox):
    combobox.get_model().clear()
    return 	    

def on_cursor_position_changed(buffer, data=None):
    global cursorPosition
    cursorPosition =  buffer.props.cursor_position
    
def ui_begin():
    data_begin()
    w.connect('destroy',lambda x: gtk.main_quit())

    hbox=gtk.HBox()
    hbox.pack_start(tv)
    hbox.pack_start(combobox)

    buffr.connect("notify::cursor-position",on_cursor_position_changed)
    tv.set_buffer(buffr)
    tv.connect('key_press_event', keyPress_func)

    w.add(hbox)
    w.set_default_size(600, 400)
    w.move(200, 100)
    w.show_all()
    w.set_title('Offline Transliterator')

    combobox.hide()
    gtk.main()
