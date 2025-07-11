# apps/core/views.py
from django.shortcuts import render, redirect
from ..forms import TipoUsuarioForm, PlanForm, BaseInfoForm


def home(request):
    search_query = request.GET.get('q', '').strip()
    return render(request, 'core/home.html', {
        'search_query': search_query,
    })


def ayuda(request): 
    return render(request, 'core/ayuda.html')

def pro(request):
    return render(request, 'core/pro.html')


def registro_profesional(request):
    """Registro profesional multipágina simple."""
    if not request.user.is_authenticated:
        return redirect('login')

    step = request.GET.get('step', '1')

    if step == '1':
        if request.method == 'POST':
            form = TipoUsuarioForm(request.POST)
            if form.is_valid():
                request.session['tipo_usuario'] = form.cleaned_data['tipo']
                return redirect('/pro/registro/?step=2')
        else:
            form = TipoUsuarioForm()
        return render(request, 'core/registro_pro_step1.html', {'form': form})

    if step == '2':
        if request.method == 'POST':
            form = PlanForm(request.POST)
            if form.is_valid():
                request.session['plan'] = form.cleaned_data['plan']
                return redirect('/pro/registro/?step=3')
        else:
            form = PlanForm()
        return render(request, 'core/registro_pro_step2.html', {'form': form})

    # Step 3
    if request.method == 'POST':
        form = BaseInfoForm(request.POST)
        if form.is_valid():
            request.session.pop('tipo_usuario', None)
            request.session.pop('plan', None)
            return render(request, 'core/registro_pro_success.html')
    else:
        form = BaseInfoForm()
    tipo = request.session.get('tipo_usuario')
    return render(request, 'core/registro_pro_step3.html', {'form': form, 'tipo': tipo})


def terminos(request):
    """Display terms and conditions page."""
    return render(request, 'core/terminos_condiciones.html')


def privacidad(request):
    """Display privacy policy page."""
    return render(request, 'core/politica_privacidad.html')


def cookies(request):
    """Display cookies policy page."""
    return render(request, 'core/politica_cookies.html')
 
 


