from django import forms
from django.contrib.auth.models import User
from .models import Evento

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')
    
    class Meta:
        model = User
        fields = ('username', 'email')
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ('titulo', 'descripcion', 'fecha', 'ubicacion', 'tipo', 'privado')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'privado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }