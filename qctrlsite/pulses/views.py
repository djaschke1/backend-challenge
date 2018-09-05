from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .forms import PulseForm, PulseNameForm, UpdateForm, UploadForm
from .models import Pulse


# Create your views here.

def index(request):
    template = loader.get_template('pulses/index.html')
    context = {}

    return HttpResponse(template.render(context, request))
    #return HttpResponse('QCTRL pulses.')

# ---------------------------------------------------------------------

def single(request):
    """
    Option for a single pulse.
    """
    template = loader.get_template('pulses/single.html')
    context = {}

    return HttpResponse(template.render(context, request))
    #return HttpResponse('Manage pulses')


def manage_create(request):

    has_msg = False
    msg = ''

    if(request.method == "POST"):
        form = PulseForm(request.POST)

        if(form.is_valid):
            # Process data

            name = form['name'].value()
            ptype = form['ptype'].value()
            rabi = form['rabi'].value()
            angle = form['angle'].value()

            valid = True
            if(ptype.lower() not in get_all_ptypes()):
                # Pulse type not valid
                msg += 'Type not valid. '
                valid = False

            names = []
            for obj in Pulse.objects.all():
                names.append(obj.name)

            if(name in names):
                # Name already exists
                msg += 'Pulse name already exists.'
                valid = False

            if(valid):
                # Create and save object
                tmp = Pulse.objects.create(name=name, ptype=ptype,
                                           max_rabi_rate=rabi,
                                           polar_angle=angle)
                return HttpResponseRedirect('/pulses/single')
            else:
                has_msg = True
    else:
        form = PulseForm()

    #template = loader.get_template('pulses/create.html')
    context = {'form' : form, 'has_msg' : has_msg, 'msg' : msg}

    return render(request, 'pulses/create.html', context)
    #return HttpResponse(template.render(context, request))
    #return HttpResponse('Create new pulse')


def manage_list(request):
    all_pulses = Pulse.objects.all()
    is_empty = (len(all_pulses) == 0)

    context = {'all_pulses' : all_pulses, 'is_empty' : is_empty}
    
    return render(request, 'pulses/list.html', context)
    #return HttpResponse('List all pulses')


def manage_update(request, name=None):

    has_msg = False
    msg = ''

    if((request.method == "POST") and (name is None)):
        # Just got entry which entry to change
        form = PulseNameForm(request.POST)
        name = form['name'].value()
        names = get_all_names()

        if(name in names):
            return HttpResponseRedirect('/pulses/update/' + name)
        else:
            show_form = True
            name = ''
            form = PulseNameForm()
            has_msg = True
            msg = 'No pulse available with name ' + name + '.'

    elif(request.method == "POST"):
        Obj = list(Pulse.objects.filter(name=name))[0]
        form = UpdateForm(request.POST)

        nameu = form['name'].value()
        ptype = form['ptype'].value()
        rabi = form['rabi'].value()
        angle = form['angle'].value()

        names = get_all_names()

        if((nameu in names) and (nameu != name)):
            # Name conflict
            has_msg = True
            msg += 'Updated name is already assigned to another pulse. '
            nameu = name


        if(ptype.lower() not in get_all_ptypes()):
            # Type conflict
            has_msg = True
            msg += 'Updated pulse type is not valid.'
            ptype = Obj.ptype

        if(has_msg):
            rabi = Obj.max_rabi_rate
            angle = Obj.polar_angle
            show_form = False

            form = UpdateForm(initial_name=nameu, initial_ptype=ptype,
                              initial_rabi=rabi, initial_angle=angle)
            
        else:
            Obj.name = nameu
            Obj.ptype = ptype
            Obj.max_rabi_rate = rabi
            Obj.polar_angle = angle
            Obj.save()

            return HttpResponseRedirect('/pulses/')

    elif(name is None):
        show_form = True
        name = ''
        form = PulseNameForm()

    else:
        show_form = False

        Obj = list(Pulse.objects.filter(name=name))[0]
        name = Obj.name
        ptype = Obj.ptype
        rabi = Obj.max_rabi_rate
        angle = Obj.polar_angle

        form = UpdateForm(initial_name=name, initial_ptype=ptype,
                          initial_rabi=rabi, initial_angle=angle)

    context = {'show_form' : show_form, 'name' : name, 'form' : form,
               'has_msg' : has_msg, 'msg' : msg}

    return render(request, 'pulses/update.html', context)
    #return HttpResponse('Update one pulse')


def manage_get(request, name=None):
    has_msg = False
    msg = ''

    if((request.method == "POST") and (name is None)):
        form = PulseNameForm(request.POST)
        name = form['name'].value()
        names = get_all_names()

        if(name not in names):
            has_msg = True
            msg = 'No pulse available with name ' + name + '.'
        else:
            return HttpResponseRedirect('/pulses/get/' + name)

    elif(name is None):
        # Need form below
        pass

    else:
        Obj = list(Pulse.objects.filter(name=name))[0]

        csv_content = '"' + Obj.name + '",'
        csv_content += '"' + Obj.ptype + '",'
        csv_content += str(Obj.max_rabi_rate) + ','
        csv_content += str(Obj.polar_angle) + '\n'

        return HttpResponse(csv_content, content_type='text/plain')

    form = PulseNameForm()
    context = {'has_msg' : has_msg, 'msg' : msg, 'form' : form}

    return render(request, 'pulses/get.html', context)
    #return HttpResponse('Get one pulse')


def manage_delete(request, name=None):
    if((request.method == "POST") and (name is None)):
        form = PulseNameForm(request.POST)
        name = form['name'].value()

        names = get_all_names()

        if(name in names):
            return HttpResponseRedirect('/pulses/delete/' + name)
        else:
            return HttpResponseRedirect('/pulses/')


    elif(request.method == "POST"):
        Pulse.objects.filter(name=name).delete()
        return HttpResponseRedirect('/pulses/')

    if(name is None):
        # Display form
        show_form = True
        name = ''
        form = PulseNameForm()
        
    else:
        show_form = False
        form = ''


    context = {'show_form' : show_form, 'name' : name, 'form' : form}

    return render(request, 'pulses/delete.html', context)
    #return HttpResponse('Delete pulse')


def get_all_names():
    names = []
    for obj in Pulse.objects.all():
        names.append(obj.name)

    return names


def get_all_ptypes():
    return ['primitive', 'gaussian', 'corpse', 'cinbb', 'cinsk']


# ---------------------------------------------------------------------

def upload(request):
    if(request.method == "POST"):
        # Read file and go to default page
        form = UploadForm(request.POST, request.FILES)

        if(form.is_valid()):
            upfile = request.FILES['filea']

            # Assume no memory limitations
            content = upfile.read()
            content = content.decode("utf-8")
            print('Content utf-8', content)
            content = content.split('\n')
            print('Content split', content)

            names = get_all_names()

            for line in content:
                if(len(line) == 0): continue
                tmp = line.split(',')

                try:
                    name = tmp[0].replace('"', '')
                    ptype = tmp[1].replace('"', '')
                    rabi = float(tmp[2])
                    angle = float(tmp[3])

                    if(name in names):
                        print("Name duplicate")
                        continue

                    if(ptype not in get_all_ptypes()):
                        print("Ptype problem")
                        continue

                    if((rabi < 0.0) or (rabi > 100)):
                        print("Rabi rate problem")
                        continue

                    if((angle < 0.0) or (angle > 1.0)):
                        print("Angle problem")
                        continue

                    tmp = Pulse.objects.create(name=name, ptype=ptype,
                                               max_rabi_rate=rabi,
                                               polar_angle=angle)               
                except ValueError:
                    # String to float conversion failed - assume header
                    print('String to float failed.')
                    continue

            return HttpResponseRedirect('/pulses/')
        #else:
        #    print('form not valid')

    form = UploadForm()
    context = {'form' : form}
    
    return render(request, 'pulses/upload.html', context)


def download(request):
    csv_content = ''
    for obj in  Pulse.objects.all():
        csv_content += '"' + obj.name + '",'
        csv_content += '"' + obj.ptype + '",'
        csv_content += str(obj.max_rabi_rate) + ','
        csv_content += str(obj.polar_angle) + '\n'

    return HttpResponse(csv_content, content_type='text/plain')
